import time
from datetime import datetime

from selenium import webdriver

from src.scrape_it import write_jobs
from src.company_list import get_company_list
from src.company_list import write_companies

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

n = 1
now = datetime.date(datetime.now())
start_time = time.time()
for company in company_list:
    st = time.time()
    print(f'[CRAWLER] scrape {n} of {len(company_list)}')
    n = n + 1
    try:
        jobs_data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
        write_jobs(jobs_data)
        print(f'[CRAWLER] Company {company.company_name} has {len(jobs_data)} open positions on {now}')
        print('[CRAWLER] Execution time:', round(time.time() - st), 'seconds')
    except Exception:
        print(f'Company {company.company_name} failed to process...')
print('[CRAWLER] Execution time:', round((time.time() - start_time)/60), 'minutes')
driver.close()
