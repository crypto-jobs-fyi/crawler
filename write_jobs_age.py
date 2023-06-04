import json

with open('jobs.json', 'r') as f:
    jobs_json = json.load(f)
    jobs_data = jobs_json.get('data', [])
    print(f'Number of jobs: {len(jobs_data)}')

with open('jobs_age.json', 'r') as age_file:
    age_data = json.load(age_file)

for job in jobs_data:
    link = job.get('link')
    num = age_data.get(link, 0)
    if num != 0:
        age_data[link] = num+1
    else:
        age_data[link] = 1

print(f'Number of jobs processed: {len(age_data)}')
with open('jobs_age.json', 'w') as file:
    json.dump(age_data, file, indent=4)
