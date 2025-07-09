import json
jobs_file = 'ai_jobs.json'
jobs_age_file = 'ai_jobs_age.json'
jobs_new_file = 'ai_jobs_new.json'
job_age_number = 3  # Number of days to consider a job as new

with open(jobs_file, 'r') as jobs:
    jobs_json = json.load(jobs)
    jobs = jobs_json['data']

with open(jobs_age_file, 'r') as age:
    jobs_age_json = json.load(age)

recent_jobs = []

for job in jobs:
    link = job['link']
    if jobs_age_json[link] < job_age_number:
        recent_jobs.append(job)

print(f"Found {len(recent_jobs)} new jobs.")
for job in recent_jobs:
    print(f"{job['title']} @ {job['company'].capitalize()} -> {job['link'].split('href=')[1].split('target=')[0]}")

with open(jobs_new_file, 'w') as file:
    rj = {'data': recent_jobs}
    json.dump(rj, file, indent=4)
