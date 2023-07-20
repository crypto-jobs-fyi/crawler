import json
from datetime import datetime

with open('jobs.json', 'r') as f:
    jobs_json = json.load(f)
    jobs_data = jobs_json.get('data', [])
    print(f'Number of jobs: {len(jobs_data)}')

with open('jobs_age.json', 'r') as age_file:
    age_data = json.load(age_file)
    print(f'Number of jobs ages stored: {len(age_data)}')

current_jobs = {"Total Jobs": len(jobs_data)}
for j in jobs_data:
    company_name = j.get('company')
    current_jobs[company_name] = current_jobs.get(company_name, 0) + 1

with open("current.json", "w") as file:
    json.dump(current_jobs, file, indent=4)

for job in jobs_data:
    link = job.get('link')
    num = age_data.get(link, 0)
    if num != 0:
        age_data[link] = num + 1
    else:
        age_data[link] = 1

print(f'Number of jobs processed: {len(age_data)}')
with open('jobs_age.json', 'w') as file:
    json.dump(age_data, file, indent=4)


def write_history(current_jobs_json: dict):
    now = f'{datetime.date(datetime.now())}'
    with open('history.json', 'r') as f:
        jobs_data_json = json.load(f)
    for c_job in current_jobs_json:
        it = jobs_data_json.get(c_job, {})
        it[now] = current_jobs_json[c_job]
        jobs_data_json[c_job] = it
    with open('history.json', 'w') as history_file:
        json.dump(jobs_data_json, history_file, indent=4)


with open('current.json', 'r') as current_json_file:
    c_data = json.load(current_json_file)
    write_history(dict(c_data))
with open('companies.json', 'r') as companies_file:
    companies_file_data = json.load(companies_file)
print('--- No jobs found for following companies: ---')
for c in companies_file_data:
    c_name = c.get('company_name')
    if c_data.get(c_name, 0) == 0:
        print(f'Company: {c_name} Jobs board: {c.get("jobs_url")}')

print('^^^ No jobs found for the above companies: ^^^')
