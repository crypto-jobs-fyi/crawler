import json
from src.companies import Companies
from src.company_item import CompanyItem
from src.company_ai_list import get_company_list
from src.logging_utils import get_logger

company_list: list[CompanyItem] = get_company_list()
logger = get_logger(__name__)
logger.info(
    "Companies loaded",
    extra={"company_count": len(company_list), "jobs_file": 'ai_jobs.json'},
)
Companies.write_companies('ai_companies.json', company_list)
jobs_file = 'ai_jobs.json'

def write_jobs(jobs, file_name=jobs_file):
    with open(jobs_file, 'w') as f:
        json.dump({"data": jobs}, f, indent=4)

def read_jobs(file_name=jobs_file):
    with open(file_name, 'r') as f:
        jobs_json = json.load(f)
    logger.info(
        "Jobs loaded",
        extra={"file_name": file_name, "job_count": len(jobs_json.get("data", []))},
    )
    return jobs_json.get('data', [])

job_json_list = ['headed_ai_jobs.json', 'ai_jobs.json', 'ai_jobs_ashby.json', 'ai_jobs_greenhouse.json', 'ai_jobs_lever.json']

def read_jobs_from_files(file_list):
    all_jobs = []
    for job_json in file_list:
        jobs = read_jobs(file_name=job_json)
        all_jobs.extend(jobs)
    return all_jobs

all_jobs = read_jobs_from_files(job_json_list)
logger.info(
    "Jobs merged",
    extra={"job_count": len(all_jobs), "output_file": 'merged_ai_jobs.json'},
)
write_jobs(all_jobs, file_name='merged_ai_jobs.json')