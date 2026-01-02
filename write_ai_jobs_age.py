from src.age_processor import update_job_ages

jobs_file = 'ai_jobs.json'
current_json_file = 'ai_current.json'
jobs_age_file = 'ai_jobs_age.json'
history_file = 'ai_history.json'

update_job_ages(jobs_file, jobs_age_file, current_json_file, history_file)

