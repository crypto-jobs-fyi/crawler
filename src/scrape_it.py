import json
from abc import ABC, abstractmethod
import os
from src.logging_utils import get_logger


class ScrapeIt(ABC):
    def __init__(self) -> None:
        logger_name = f"scraper.{getattr(self, 'name', self.__class__.__name__)}"
        self.logger = get_logger(logger_name)

    @abstractmethod
    def getJobs(self, driver, web_page, company) -> list:
        pass

    def log_info(self, message: str, **extra) -> None:
        self.logger.info(message, extra=extra)

    def log_warning(self, message: str, **extra) -> None:
        self.logger.warning(message, extra=extra)

    def log_error(self, message: str, *, exc_info: bool | BaseException | None = None, **extra) -> None:
        self.logger.error(message, extra=extra, exc_info=exc_info)

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
