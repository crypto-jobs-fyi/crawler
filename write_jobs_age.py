from src.age_processor import update_job_ages

jobs_file = 'crypto_jobs.json'
current_json_file = 'crypto_current.json'
jobs_age_file = 'crypto_jobs_age.json'
history_file = 'crypto_history.json'

update_job_ages(jobs_file, jobs_age_file, current_json_file, history_file)

