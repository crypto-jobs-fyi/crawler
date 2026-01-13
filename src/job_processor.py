import json
from datetime import datetime
from src.logging_utils import get_logger

logger = get_logger(__name__)

def get_new_jobs(jobs_file: str, jobs_age_file: str, jobs_new_file: str, job_age_number: int = 3):
    with open(jobs_file, 'r') as jobs:
        jobs_json = json.load(jobs)
        jobs_data = jobs_json['data']

    with open(jobs_age_file, 'r') as age:
        jobs_age_json = json.load(age)

    recent_jobs = []
    now = datetime.date(datetime.now())

    for job in jobs_data:
        link = job['link']
        if link in jobs_age_json:
            added_val = jobs_age_json[link]
            
            # Handle date strings (new format)
            if isinstance(added_val, str):
                try:
                    added_date = datetime.strptime(added_val, '%Y-%m-%d').date()
                    if (now - added_date).days < job_age_number:
                        recent_jobs.append(job)
                except ValueError:
                    pass

    logger.info(
        "Recent jobs identified",
        extra={"count": len(recent_jobs), "jobs_file": jobs_file},
    )
    for job in recent_jobs:
        logger.info(
            "Recent job",
            extra={
                "title": job['title'],
                "company": job['company'],
                "link": job['link'],
            },
        )

    with open(jobs_new_file, 'w') as file:
        rj = {'data': recent_jobs}
        json.dump(rj, file, indent=4)
