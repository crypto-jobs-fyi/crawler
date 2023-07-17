import json
import time
from datetime import datetime

from selenium import webdriver

from src.company_list import get_company, write_companies
from src.company_list import get_company_list

company_list = get_company_list()
print(f'[CRAWLER] Number of companies: {len(company_list)}')
write_companies('companies.json')

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


def write_numbers():
    now = datetime.date(datetime.now())
    global total_number_of_jobs
    print(f'[CRAWLER] In Total {total_number_of_jobs} of open positions on {now}')
    global current_jobs
    current_jobs["Total Jobs"] = total_number_of_jobs
    with open(f"current.json", "w") as file:
        json.dump(current_jobs, file, indent=4)


n = 1

for company in company_list:
    now = datetime.date(datetime.now())
    st = time.time()
    print(f'[CRAWLER] scrape {n} of {len(company_list)}')
    n = n + 1
    jobs_data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    print(f'[CRAWLER] Company {company.company_name} has {len(jobs_data)} open positions on {now}')
    print('[CRAWLER] Execution time:', (time.time() - st), 'seconds')

driver.close()

write_numbers()


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
print('^^^ No jobs found for the above companies: ^^^')
