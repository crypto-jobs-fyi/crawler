import json

with open('jobs.json', 'r') as f:
    jobs_json = json.load(f)
    jobs_data = jobs_json.get('data', [])
    print(len(jobs_data))

print(jobs_data[0])

data = list(filter(lambda jd: jd.get('company') == 'wintermute', jobs_data))
print(data)

# write age
with open('age.json', 'r') as age_file:
    age_data = json.load(age_file)
print(age_data)

for job in jobs_data:
    link = job.get('link')
    print(link)
    num = age_data.get(link, 0)
    if num != 0:
        age_data[link] = num+1
    else:
        age_data[link] = 1

with open('age.json', 'w') as file:
    json.dump(age_data, file, indent=4)
