import json
import time
from datetime import datetime

from selenium import webdriver

from src.company_list import get_company
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
chrome_options.add_argument('--disable-extensions')
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


def write_companies():
    result_list = []
    for com in company_list:
        company_item = {
            "company_name": com.company_name,
            "company_url": com.company_url,
            "jobs_url": com.jobs_url,
        }
        result_list.append(company_item)
    print(f'[CRAWLER] Number of Companies {len(result_list)}')
    with open('companies.json', 'w') as companies_file:
        json_string = json.dumps(result_list)
        companies_file.write(json_string)


for company in company_list:
    st = time.time()
    jobs_data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    print('[CRAWLER] Execution time:', (time.time() - st), 'seconds')
    print_and_collect_numbers(company.company_name, len(jobs_data))

driver.close()

write_numbers()
write_companies()


def write_history(current_jobs_json: dict):
    now = f'{datetime.date(datetime.now())}'
    with open('history.json', 'r') as f:
        jobs_data_json = json.load(f)
    for job in current_jobs_json:
        it = jobs_data_json.get(job, {})
        it[now] = current_jobs_json[job]
        jobs_data_json[job] = it
    with open('history.json', 'w') as file:
        json.dump(jobs_data_json, file, indent=4)


with open('current.json') as json_file:
    data = json.load(json_file)
    write_history(dict(data))


print('--- No jobs found for following companies: ---')
with open('current.json', 'r') as current_file:
    current_jobs_data = json.load(current_file)

for i in current_jobs_data:
    if current_jobs_data[i] == 0:
        print(f'Company: {i} Jobs board: {get_company(i).jobs_url}')
