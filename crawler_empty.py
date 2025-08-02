from datetime import datetime
import time
from typing import Dict, List, Any

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from src.company_item import CompanyItem
from src.company_list_empty import get_company_list
from src.scrape_it import ScrapeIt
from src.companies import Companies

jobs_file: str = 'crypto_jobs_empty.json'
company_list: List[CompanyItem] = get_company_list()
print(f'[CRAWLER] Number of companies: {len(company_list)}')
Companies.write_companies('companies_empty.json', company_list)

with open(jobs_file, 'w') as f:
    f.write('{}')

# setup headless webdriver
chrome_options: webdriver.ChromeOptions = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-extensions')
driver: WebDriver = webdriver.Chrome(options=chrome_options)

n: int = 1
now: datetime.date = datetime.date(datetime.now())
start_time: float = time.time()
jobs_data: List[Dict[str, Any]] = []
for company in company_list:
    st: float = time.time()
    print(f'[CRAWLER] scrape {n} of {len(company_list)}')
    n = n + 1
    try:
        crawler_type: ScrapeIt = company.scraper_type()
        jobs_data: List[Dict[str, Any]] = crawler_type.getJobs(driver, company.jobs_url, company.company_name)
        ScrapeIt.write_jobs(jobs_data, jobs_file)
        ScrapeIt.write_current_jobs_number(company.company_name, len(jobs_data), file_name='current_jobs_empty.json')
        print(f'[CRAWLER] Company {company.company_name} has {len(jobs_data)} open positions on {now}')
        print('[CRAWLER] Execution time:', round(time.time() - st), 'seconds')
    except Exception as e:
        print(e)
        print(f'Company {company.company_name} failed to process...')
print('[CRAWLER] Execution time:', round((time.time() - start_time)/60), 'minutes')
driver.close()
