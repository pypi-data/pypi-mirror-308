from QualtricsAPI.Setup import Credentials
from QualtricsAPI.Survey import Responses
import os
import json

Credentials().qualtrics_api_credentials(token=os.environ['QUALTRICS_TOKEN'],data_center=os.environ['QUALTRICS_DC'])


def download_survey(sid, dest):
    if os.path.isdir(dest):
        dest = f"{dest}/{sid}"
    responses = Responses().get_survey_responses(survey=sid)
    questions = Responses().get_survey_questions(survey=sid)
    questions = questions.to_dict()['Questions']

    responses.iloc[2:].to_csv(f"{dest}-responses.tsv", sep='\t')
    with open(f"{dest}-questions.json", 'wt') as qf:
        json.dump(questions, qf, indent=4)

