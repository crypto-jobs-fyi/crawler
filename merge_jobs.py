import json
from src.companies import Companies
from src.company_item import CompanyItem
from src.logging_utils import get_logger

company_list: list[CompanyItem] = Companies.load_companies()
logger = get_logger(__name__)
logger.info(
    "Companies loaded",
    extra={"company_count": len(company_list), "jobs_file": 'jobs.json'},
)
jobs_file = 'jobs.json'
with open(jobs_file, 'w') as f:
    f.write('{}')

def write_jobs(jobs, file_name=jobs_file):
    with open(file_name, 'r') as f:
        jobs_json = json.load(f)
    jobs_data = jobs_json.get('data', [])
    for job in jobs:
        jobs_data.append(job)
    jobs_json['data'] = jobs_data
    with open(file_name, 'w') as file:
        json.dump(jobs_json, file, indent=4)

def read_jobs(file_name=jobs_file):
    with open(file_name, 'r') as f:
        jobs_json = json.load(f)
    return jobs_json.get('data', [])

job_json_list = ['headed_crypto_jobs.json', 'crypto_jobs.json', 'crypto_jobs_lever.json', 'crypto_jobs_greenhouse.json', 'crypto_jobs_ashby.json']

for job_json in job_json_list:
    jobs = read_jobs(file_name=job_json)
    write_jobs(jobs)
