import time

from selenium import webdriver

from src.company_list_empty import get_company_list
from src.company_list_empty import write_companies

company_list = get_company_list()
print(f'[CRAWLER] Number of companies: {len(company_list)}')
write_companies('companies_empty.json')

with open('jobs_empty.json', 'w') as f:
    f.write('{}')

# setup headless webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-extensions')
driver = webdriver.Chrome(options=chrome_options)

current_jobs = {}
n = 1
for company in company_list:
    st = time.time()
    print(f'[CRAWLER] scrape {n} of {len(company_list)}')
    n = n + 1
    jobs_data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    print('[CRAWLER] Execution time:', (time.time() - st), 'seconds')

driver.close()
