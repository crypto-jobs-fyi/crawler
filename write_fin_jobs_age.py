from src.age_processor import update_job_ages

jobs_file = 'fin_jobs.json'
current_json_file = 'fin_current.json'
jobs_age_file = 'fin_jobs_age.json'
history_file = 'fin_history.json'

update_job_ages(jobs_file, jobs_age_file, current_json_file, history_file)

