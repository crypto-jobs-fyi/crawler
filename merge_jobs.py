import json
from src.companies import Companies
from src.company_item import CompanyItem
from src.company_list import get_company_list

company_list: list[CompanyItem] = get_company_list()
print(f'[CRAWLER] Number of companies: {len(company_list)}')
Companies.write_companies('companies.json', company_list)

def write_jobs(jobs, file_name='jobs.json'):
    with open(file_name, 'r') as f:
        jobs_json = json.load(f)
    jobs_data = jobs_json.get('data', [])
    for job in jobs:
        jobs_data.append(job)
    jobs_json['data'] = jobs_data
    with open(file_name, 'w') as file:
        json.dump(jobs_json, file, indent=4)

def read_jobs(file_name='jobs.json'):
    with open(file_name, 'r') as f:
        jobs_json = json.load(f)
    return jobs_json.get('data', [])

job_json_list = ['headed_jobs.json', 'crypto_jobs.json', 'crypto_jobs_lever.json', 'crypto_jobs_greenhouse.json']

for job_json in job_json_list:
    jobs = read_jobs(file_name=job_json)
    write_jobs(jobs)
