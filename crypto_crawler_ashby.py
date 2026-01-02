import time
from datetime import datetime

from selenium import webdriver

from src.scrapers import Scrapers
from src.companies import Companies
from src.company_item import CompanyItem
from src.scrape_it import ScrapeIt
from src.company_list import get_company_list

company_list: list[CompanyItem] = get_company_list()
jobs_file = 'crypto_jobs_ashby.json'
current_jobs_file = 'crypto_current_ashby.json'
with open(jobs_file, 'w') as f:
    f.write('{}')

with open(current_jobs_file, 'w') as cf:
    cf.write('{}')

# setup headless webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-extensions')
driver: webdriver.Chrome = webdriver.Chrome(options=chrome_options)

filtered_companies = Companies.filter_companies(company_list, Scrapers.ASHBYHQ)
n = 1
now = datetime.date(datetime.now())
start_time = time.time()
for company in filtered_companies:
    st = time.time()
    print(f'[CRAWLER] scrape {n} of {len(filtered_companies)}')
    n = n + 1
    try:
        crawler_type: ScrapeIt = company.scraper_type()
        jobs_data = crawler_type.getJobs(driver, company.jobs_url, company.company_name)
        ScrapeIt.write_jobs(jobs_data, jobs_file)
        ScrapeIt.write_current_jobs_number(company.company_name, len(jobs_data), current_jobs_file)
        print(f'[CRAWLER] Company {company.company_name} has {len(jobs_data)} open positions on {now}')
        print('[CRAWLER] Execution time:', round(time.time() - st), 'seconds')
    except Exception:
        print(f'Company {company.company_name} failed to process...')
print('[CRAWLER] Execution time:', round((time.time() - start_time)/60), 'minutes')
driver.close()
