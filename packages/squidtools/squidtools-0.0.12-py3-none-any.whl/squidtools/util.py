import csv
import sys

"""
Read delimited text data file (csv, tsv, etc) and return a list of dicts (if key is None)
or a dict with keys given by the 'key' argument.
Automatically detects delimiter based on the ending of the file path
"""
def read_delim(filename, key=None):
    with open(filename) as f:
        if filename.endswith('tsv'):
            reader = csv.DictReader(f, delimiter='\t')
        elif filename.endswith('csv'):
            reader = csv.DictReader(f, delimiter=',')
        else:
            print_err('Unrecognized file extension')
            raise Exception
        if key is None:
            return [row for row in reader]
        else:
            return {row[key]: row for row in reader}

def write_delim(records, filename):
    if filename.endswith('tsv'):
        write_tsv(records, filename)
    elif filename.endswith('csv'):
        write_csv(records, filename)
    else:
        print_err('Unrecognized file extension')
        raise Exception

def write_csv(records, filename, delimiter=',', verbose=True):
    if isinstance(records, dict):
        # Auto manage this common use case
        records = records.values()
        if verbose:
            print_err("[warning] write_csv: converting dict input to list")


    fieldnames = set()
    for r in records:
        fieldnames.update(r.keys())
    with open(filename, 'wt') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(records)

def write_tsv(records, filename, verbose=True):
    write_csv(records, filename, delimiter='\t', verbose=verbose)

def print_err(msg):
    sys.stderr.write(str(msg) + "\n")
    sys.stderr.flush()

# batch generator
def gen_batches(iterable, max_batch_size: int):
    """ Batches an iterable into lists of given maximum size, yielding them one by one. """
    batch = []
    for element in iterable:
        batch.append(element)
        if len(batch) >= max_batch_size:
            yield batch
            batch = []
    if len(batch) > 0:
        yield batch
    
