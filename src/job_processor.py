import json

def get_new_jobs(jobs_file: str, jobs_age_file: str, jobs_new_file: str, job_age_number: int = 3):
    with open(jobs_file, 'r') as jobs:
        jobs_json = json.load(jobs)
        jobs_data = jobs_json['data']

    with open(jobs_age_file, 'r') as age:
        jobs_age_json = json.load(age)

    recent_jobs = []

    for job in jobs_data:
        link = job['link']
        if link in jobs_age_json and jobs_age_json[link] < job_age_number:
            recent_jobs.append(job)

    print(f"Found {len(recent_jobs)} new jobs.")
    for job in recent_jobs:
        print(f"{job['title']} @ {job['company'].capitalize()} -> {job['link']}")

    with open(jobs_new_file, 'w') as file:
        rj = {'data': recent_jobs}
        json.dump(rj, file, indent=4)
