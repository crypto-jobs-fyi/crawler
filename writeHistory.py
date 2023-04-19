from datetime import datetime
import json


def write_history(current_jobs: dict):
    now = f'{datetime.date(datetime.now())}'
    with open('history.json', 'r') as f:
        jobs_data = json.load(f)
    for job in current_jobs:
        it = jobs_data.get(job, {})
        it[now] = current_jobs[job]
        jobs_data[job] = it
    with open('history.json', 'w') as file:
        json.dump(jobs_data, file, indent=4)


with open('current.json') as json_file:
    data = json.load(json_file)
    write_history(dict(data))
