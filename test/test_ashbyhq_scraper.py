import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time

from selenium import webdriver

from src.company_item import CompanyItem
from src.scrapers import Scrapers

start = time.time()

options = webdriver.ChromeOptions()
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
companies = [
    CompanyItem('nethermind', 'https://jobs.ashbyhq.com/nethermind', Scrapers.ASHBYHQ.value, 'https://www.nethermind.io'),
    CompanyItem('chainlink-labs', 'https://jobs.ashbyhq.com/chainlink-labs', Scrapers.ASHBYHQ.value, 'https://chainlinklabs.com'),
    CompanyItem('llamaindex', 'https://jobs.ashbyhq.com/llamaindex', Scrapers.ASHBYHQ.value, 'https://www.llamaindex.ai'),
    CompanyItem('coderabbit', 'https://jobs.ashbyhq.com/coderabbit', Scrapers.ASHBYHQ.value, 'https://coderabbit.ai'),
    CompanyItem('kiln', 'https://jobs.ashbyhq.com/kiln.fi', Scrapers.ASHBYHQ.value, 'https://www.kiln.fi'),
    CompanyItem('dune', 'https://jobs.ashbyhq.com/dune', Scrapers.ASHBYHQ.value, 'https://dune.com'),
    CompanyItem('conduit', 'https://jobs.ashbyhq.com/Conduit', Scrapers.ASHBYHQ.value, 'https://conduit.xyz'),
    CompanyItem('paradigm.xyz', 'https://jobs.ashbyhq.com/paradigm', Scrapers.ASHBYHQ.value, 'https://www.paradigm.xyz'),
    CompanyItem('ellipsislabs', 'https://jobs.ashbyhq.com/ellipsislabs', Scrapers.ASHBYHQ.value,
                'https://ellipsislabs.xyz')
]

for company in companies:
    data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in data:
        print(entry)

driver.close()

end = time.time()
print(f"Time: {end - start:.2f} sec")
