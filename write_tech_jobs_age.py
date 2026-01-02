from src.age_processor import update_job_ages

jobs_file = 'tech_jobs.json'
current_json_file = 'tech_current.json'
jobs_age_file = 'tech_jobs_age.json'
history_file = 'tech_history.json'

update_job_ages(jobs_file, jobs_age_file, current_json_file, history_file)
