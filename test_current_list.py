import json

with open('current.json', 'r') as f:
    jobs_data = json.load(f)
    print(f'Number of records: {len(jobs_data)}')

for i in jobs_data:
    if jobs_data[i] == 0:
        print(i)
