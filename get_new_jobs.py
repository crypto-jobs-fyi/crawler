from src.job_processor import get_new_jobs

jobs_file = 'jobs.json'
jobs_age_file = 'crypto_jobs_age.json'
jobs_new_file = 'jobs_new.json'
job_age_number = 3  # Number of days to consider a job as new

get_new_jobs(jobs_file, jobs_age_file, jobs_new_file, job_age_number)

