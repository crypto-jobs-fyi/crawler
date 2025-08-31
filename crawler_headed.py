import tempfile
import time
from datetime import datetime

from selenium import webdriver

from src.scrapers import Scrapers
from src.company_item import CompanyItem
from src.scrape_it import ScrapeIt


user_data_dir = tempfile.mkdtemp()  # Creates a unique temp directory
jobs_file = 'headed_jobs.json'
current_jobs_file = 'headed_current_jobs.json'
with open(jobs_file, 'w') as f:
    f.write('{}')

with open(current_jobs_file, 'w') as cf:
    cf.write('{}')

# setup headless webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)

company_list = [
    CompanyItem('coinbase', 'https://www.coinbase.com/careers/positions', Scrapers.COINBASE.value, 'https://coinbase.com'),
    CompanyItem('sygnum', 'https://www.sygnum.com/careers-portal', Scrapers.SYGNUM.value, 'https://www.sygnum.com'),
]

n = 1
now = datetime.date(datetime.now())
start_time = time.time()
for company in company_list:
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
