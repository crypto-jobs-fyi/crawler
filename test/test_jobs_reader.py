import json

with open('jobs.json', 'r') as f:
    jobs_json = json.load(f)
    jobs_data = jobs_json.get('data', [])
    print(len(jobs_data))

print(jobs_data[0])

data = list(filter(lambda jd: jd.get('company') == 'wintermute', jobs_data))
print(data)
