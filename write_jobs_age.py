from src.age_processor import update_job_ages

jobs_file = 'jobs.json'
current_json_file = 'current.json'
jobs_age_file = 'jobs_age.json'
history_file = 'history.json'

update_job_ages(jobs_file, jobs_age_file, current_json_file, history_file)

