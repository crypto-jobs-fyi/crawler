import json
from src.companies import Companies
from src.logging_utils import get_logger

# Filter companies specifically for the Fintech category
company_list = Companies.filter_companies(category="fintech")
Companies.write_companies('fin_companies.json', company_list)
logger = get_logger(__name__)

# Main output file for Fintech jobs
jobs_file = 'fin_jobs.json'

logger.info(
    "Starting Fintech jobs merge",
    extra={"company_count": len(company_list), "output_file": jobs_file},
)

def write_jobs(jobs, file_name=jobs_file):
    """Write the merged jobs list to a JSON file."""
    with open(file_name, 'w') as f:
        json.dump({"data": jobs}, f, indent=4)

def read_jobs(file_name):
    """Read jobs from a JSON file with error handling."""
    try:
        with open(file_name, 'r') as f:
            content = f.read().strip()
            if not content or content == '{}':
                return []
            jobs_json = json.loads(content)
        
        jobs_data = jobs_json.get('data', [])
        logger.info(
            "Jobs loaded",
            extra={"file_name": file_name, "job_count": len(jobs_data)},
        )
        return jobs_data
    except (FileNotFoundError, json.JSONDecodeError):
        # We don't want to fail if one subset file is missing
        logger.warning(f"File not found or invalid JSON: {file_name}")
        return []

# List of files to merge into the main fin_jobs.json
job_json_list = [
    'fin_jobs.json',
    'headed_fintech_jobs.json'
]

def merge_jobs_from_files(file_list):
    """Combine jobs from multiple files and deduplicate by link."""
    all_jobs = []
    seen_links = set()
    
    for job_json in file_list:
        jobs = read_jobs(file_name=job_json)
        for job in jobs:
            link = job.get('link')
            if link and link not in seen_links:
                all_jobs.append(job)
                seen_links.add(link)
                
    return all_jobs

# Perform the merge and write the results
all_merged_jobs = merge_jobs_from_files(job_json_list)

logger.info(
    "Fintech jobs merge completed",
    extra={"total_merged_count": len(all_merged_jobs), "output_file": jobs_file},
)

write_jobs(all_merged_jobs, file_name=jobs_file)

