import json

with open('jobs.json', 'r') as jobs:
    jobs_json = json.load(jobs)
    jobs = jobs_json['data']

with open('jobs_age.json', 'r') as age:
    jobs_age_json = json.load(age)

recent_jobs = []

for job in jobs:
    link = job['link']
    if jobs_age_json[link] < 2:
        recent_jobs.append(job)

print(f"Found {len(recent_jobs)} new jobs.")
for job in recent_jobs:
    print(f"{job['title']} @ {job['company'].capitalize()} -> {job['link'].split('href=')[1].split('target=')[0]}")

with open('jobs_new.json', 'w') as file:
    rj = {'data': recent_jobs}
    json.dump(rj, file, indent=4)
