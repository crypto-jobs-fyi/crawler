import time
from datetime import datetime

from selenium import webdriver

from src.scrapers import Scrapers
from src.company_item import CompanyItem
from src.scrape_it import ScrapeIt
from src.company_ai_list import get_company_list
from src.companies import Companies


jobs_file = 'ai_jobs.json'
current_jobs_file = 'ai_current_jobs.json'
companies_file = 'ai_companies.json'

company_list: list[CompanyItem] = get_company_list()
print(f'[CRAWLER] Number of companies: {len(company_list)}')
Companies.write_companies(companies_file, company_list)

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
driver = webdriver.Chrome(options=chrome_options)
exclude = [Scrapers.ASHBYHQ, Scrapers.GREENHOUSE, Scrapers.LEVER]
filtered_companies = Companies.filter_companies_not(company_list, exclude)
n = 1
now = datetime.date(datetime.now())
start_time = time.time()
for company in filtered_companies:
    st = time.time()
    print(f'[CRAWLER] scrape {n} of {len(company_list)}')
    n = n + 1
    try:
        crawler_type: ScrapeIt = company.scraper_type()
        jobs_data = crawler_type.getJobs(driver, company.jobs_url, company.company_name)
        ScrapeIt.write_jobs(jobs_data, jobs_file)
        ScrapeIt.write_current_jobs_number(company.company_name, len(jobs_data), current_jobs_file)
        print(f'[CRAWLER] Company {company.company_name} has {len(jobs_data)} open positions on {now}')
        print('[CRAWLER] Execution time:', round(time.time() - st), 'seconds')
    except Exception as e:
        print(e)
        print(f'Company {company.company_name} failed to process...')
print('[CRAWLER] Execution time:', round((time.time() - start_time)/60), 'minutes')
driver.close()
