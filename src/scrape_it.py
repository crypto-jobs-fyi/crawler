import json
from abc import ABC, abstractmethod
import os


class ScrapeIt(ABC):
    @abstractmethod
    def getJobs(self, driver, web_page, company) -> list:
        pass

    @staticmethod
    def write_jobs(jobs, file_name='jobs.json'):
        with open(file_name, 'r') as f:
            jobs_json = json.load(f)
        jobs_data = jobs_json.get('data', [])
        for job in jobs:
            jobs_data.append(job)
        jobs_json['data'] = jobs_data
        with open(file_name, 'w') as file:
            json.dump(jobs_json, file, indent=4)

    @staticmethod
    def write_current_jobs_number(company, number_of_jobs, file_name):
        if file_name is None or file_name.strip() == '':
            raise ValueError("File name cannot be None or empty.")
        if not os.path.exists(file_name):
            jobs_json = {}
        else:
            with open(file_name, 'r') as f:
                jobs_json = json.load(f)
        jobs_json[company] = number_of_jobs
        total_jobs = jobs_json.get('total_jobs', 0)
        total_jobs += number_of_jobs
        jobs_json['total_jobs'] = total_jobs
        with open(file_name, 'w') as file:
            json.dump(jobs_json, file, indent=4)
