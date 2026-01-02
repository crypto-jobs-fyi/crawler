import json
from datetime import datetime
import os

def update_job_ages(jobs_file, jobs_age_file, current_json_file, history_file):
    with open(jobs_file, 'r') as f:
        jobs_json = json.load(f)
        jobs_data = jobs_json.get('data', [])
        print(f'Number of jobs: {len(jobs_data)}')

    if not os.path.exists(jobs_age_file):
        with open(jobs_age_file, 'w') as file:
            json.dump({}, file)

    with open(jobs_age_file, 'r') as age_file:
        age_data = json.load(age_file)
        print(f'Number of jobs ages stored: {len(age_data)}')

    current_jobs = {"Total Jobs": len(jobs_data)}
    for j in jobs_data:
        company_name = j.get('company')
        current_jobs[company_name] = current_jobs.get(company_name, 0) + 1

    with open(current_json_file, "w") as file:
        json.dump(current_jobs, file, indent=4)

    for job in jobs_data:
        link = job.get('link')
        num = age_data.get(link, 0)
        if num != 0:
            age_data[link] = num + 1
        else:
            age_data[link] = 1

    print(f'Number of jobs processed: {len(age_data)}')
    with open(jobs_age_file, 'w') as file:
        json.dump(age_data, file, indent=4)

    def write_history(current_jobs_json: dict):
        now = f'{datetime.date(datetime.now())}'
        with open(history_file, 'r') as f:
            jobs_data_json = json.load(f)
        for c_job in current_jobs_json:
            it = jobs_data_json.get(c_job, {})
            it[now] = current_jobs_json[c_job]
            jobs_data_json[c_job] = it
        with open(history_file, 'w') as f:
            json.dump(jobs_data_json, f, indent=4)

    if not os.path.exists(history_file):
        with open(history_file, 'w') as file:
            json.dump({}, file)

    with open(current_json_file, 'r') as current_json_file_obj:
        c_data = json.load(current_json_file_obj)
        write_history(dict(c_data))
