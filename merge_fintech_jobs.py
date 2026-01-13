import json
from src.companies import Companies
from src.logging_utils import get_logger

company_list = Companies.filter_companies(category="fintech")
logger = get_logger(__name__)
logger.info(
    "Companies loaded",
    extra={"company_count": len(company_list), "jobs_file": 'fin_jobs.json'},
)
jobs_file = 'fin_jobs.json'

def write_jobs(jobs, file_name=jobs_file):
    # Fixed the bug from example where it hardcoded jobs_file instead of using file_name
    with open(file_name, 'w') as f:
        json.dump({"data": jobs}, f, indent=4)

def read_jobs(file_name=jobs_file):
    try:
        with open(file_name, 'r') as f:
            content = f.read().strip()
            if not content or content == '{}':
                return []
            jobs_json = json.loads(content)
        logger.info(
            "Jobs loaded",
            extra={"file_name": file_name, "job_count": len(jobs_json.get("data", []))},
        )
        return jobs_json.get('data', [])
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning(f"File not found or invalid: {file_name}")
        return []

job_json_list = ['headed_fintech_jobs.json', 'fin_jobs.json']

def read_jobs_from_files(file_list):
    all_jobs = []
    seen_links = set()
    for job_json in file_list:
        jobs = read_jobs(file_name=job_json)
        for job in jobs:
            # Simple deduplication by link
            if job.get('link') not in seen_links:
                all_jobs.append(job)
                seen_links.add(job.get('link'))
    return all_jobs

all_jobs = read_jobs_from_files(job_json_list)
logger.info(
    "Jobs merged",
    extra={"job_count": len(all_jobs), "output_file": 'fin_jobs.json'},
)
write_jobs(all_jobs, file_name='fin_jobs.json')
