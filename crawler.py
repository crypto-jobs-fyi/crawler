from selenium import webdriver
from datetime import datetime
import json
from src.company_list import get_company_list

company_list = get_company_list()
print(f'[CRAWLER] Number of companies: {len(company_list)}')

with open('jobs.json', 'w') as f:
    f.write('{}')

# setup headless webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

# count open positions
total_number_of_jobs: int = 0
current_jobs = {}


def print_and_collect_numbers(company_name: str, total: int):
    now = datetime.date(datetime.now())
    print(f'[CRAWLER] Company {company_name} has {total} open positions on {now}')
    global total_number_of_jobs
    total_number_of_jobs = total_number_of_jobs + total
    global current_jobs
    current_jobs[company_name] = total


def write_numbers():
    now = datetime.date(datetime.now())
    global total_number_of_jobs
    print(f'[CRAWLER] In Total {total_number_of_jobs} of open positions on {now}')
    global current_jobs
    current_jobs["Total Jobs"] = total_number_of_jobs
    with open(f"current.json", "w") as file:
        json.dump(current_jobs, file, indent=4)


for company in company_list:
    jobs_data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    print_and_collect_numbers(company.company_name, len(jobs_data))

driver.close()

write_numbers()
