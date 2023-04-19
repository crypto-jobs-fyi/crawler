import json


def write_jobs(jobs):
    with open('jobs.json', 'r') as f:
        jobs_json = json.load(f)
    jobs_data = jobs_json.get('data', [])
    for job in jobs:
        jobs_data.append(job)
    jobs_json['data'] = jobs_data
    with open('jobs.json', 'w') as file:
        json.dump(jobs_json, file, indent=4)


class ScrapeIt:
    def getJobs(self, driver, web_page, company):
        pass
