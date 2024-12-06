import json
import uuid
import pandas

from .robust_task import async_robust_task
from .gpt_utils_async import json_prompt_system, DEFAULT_MODEL
from .util import read_delim, write_delim, print_err

DEFAULT_CONFIG = {
    "model": DEFAULT_MODEL,
    "key": None,
    "input_columns": None,
    "filename_columns": [],
    "delay": 0,
    "retry_errs": 3,
    "cache_filename": None,
    "output_columns": None,
    "temp": 1,
    "timeout": 30,
}

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def make_input_text(obj, config):
    input_columns = config['input_columns']
    input_obj = {}
    if input_columns is not None:
        input_obj = {k: obj[k] for k in input_columns}
    file_columns = config['filename_columns']
    for fc in file_columns:
        with open(obj[fc]) as f:
            text = "\n".join(f.readlines())
            input_obj[obj[fc]] = text
    if not input_obj:
        input_obj = obj

    return json.dumps(input_obj)


def simple_hash(input_string):
    namespace = uuid.NAMESPACE_OID
    return str(uuid.uuid5(namespace, input_string))

def make_schema(config):
    if config['output_columns'] is None:
        return None
    # Basic json schema!
    def schema(obj):
        for col in config['output_columns']:
            if col not in obj:
                print_err(f"{col} not found!")
                return 0
        return 1
    return schema

def make_config_hash(config):
    return f"{simple_hash(config['prompt'])}.{config['model']}.t{config['temp']}"

def export_config(config):
    ch = make_config_hash(config) 
    name = ch + '.json'
    config['hash'] = ch
    json.dump(config, open(name, 'wt'))
    print_err(f"Config exported to {config}")

def apply_files(infile, outfile, config):
    records = read_delim(infile)
    new_records = apply(records, config)
    if outfile is None:
        outfile = infile + '.' + make_config_hash(config) + '.tsv'

    write_delim(new_records, outfile)
    print_err(f"Output written to {outfile}")

def apply_R(df, config):
    # df comes in as dict of vectors is dict, reshape
    data = df.values.tolist()
    columns = df.columns.tolist() 
    records = [
        dict(zip(columns, datum))
        for datum in data
    ]
    print(records)
    new_records = apply(records, config)
    print("Dict records:")
    print(new_records)
    pd_records = pandas.DataFrame.from_records(new_records)
    print("PD records:")
    print(pd_records)
    return pd_records


def apply(records, config):
    # Set defaults and validate config
    for k in DEFAULT_CONFIG:
        if k not in config:
            config[k] = DEFAULT_CONFIG[k]
    for k in config:
        if k not in DEFAULT_CONFIG and k != 'prompt':
            print_err(f"Unrecognized config entry {k}")
            raise Exception
    if isinstance(config['output_columns'], str):
        config['output_columns'] = [config['output_columns']]

    if 'prompt' not in config:
        print_err('Prompt not in config!')
        raise Exception
    if 'json' not in config['prompt'].lower():
        prompt_mod = "\nFormat your response as JSON."
        if config['output_columns']:
            prompt_mod += f" Use keys {', '.join(config['output_columns'])}"
        print_err(f"Automodding prompt: {color.BOLD}{prompt_mod.strip()}{color.END}")
        config['prompt'] += prompt_mod

    if config['cache_filename'] is None:
        config_hash = make_config_hash(config)
        config['cache_filename'] = f"{config_hash}.progress.jsonl"
        print_err(f"Using autonamed cache {config['cache_filename']}")


    # Set up records as a dict with the primary keys provided by a user specified column be keyed
    # If no primary key is specified then we use the hash of the constructed input string object
    # This guarantees unique key for each call with different input to LLM API
    key = config["key"]
    if key:
        record_dict = {r[key]: r for r in records}
    else:
        record_dict = {
            simple_hash(make_input_text(r, config)): r
            for r in records
        }

    async def prompt(key, obj):
        input_text = make_input_text(obj, config)
        schema = make_schema(config)
        result, cost = await json_prompt_system(
            config["prompt"], input_text, config["model"], schema
        )
        result['cost'] = cost
        return result

    return_records = async_robust_task(
        record_dict,
        prompt,
        progress_name=config["cache_filename"],
        delay=config["delay"],
        retry_errs=config["retry_errs"],
        timeout=config['timeout'],
    )

    # At the very end, use the original list of records
    # Note if the input had duplicate texts and no primary key
    # was specified then |record_dict| == |return_records| != |original_records|
    # So when we construct the return dataset we use a "left join" logic.
    # where we iterate through the original list of records and update each record
    # based on the record_id found in the return_records dict
    for r in records:
        record_id = r[key] if key else simple_hash(make_input_text(r, config))
        if record_id in return_records:
            r.update(return_records[record_id])
            if config['key'] != "_pkey":
                del r['_pkey']
        
    return records
 
