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
    CompanyItem('nethermind', 'https://jobs.ashbyhq.com/nethermind', Scrapers.ASHBYHQ, 'https://www.nethermind.io'),
    CompanyItem('uipath', 'https://jobs.ashbyhq.com/uipath', Scrapers.ASHBYHQ, 'https://www.uipath.com'),
    CompanyItem('chainlink-labs', 'https://jobs.ashbyhq.com/chainlink-labs', Scrapers.ASHBYHQ, 'https://chainlinklabs.com'),
    CompanyItem('llamaindex', 'https://jobs.ashbyhq.com/llamaindex', Scrapers.ASHBYHQ, 'https://www.llamaindex.ai'),
    CompanyItem('coderabbit', 'https://jobs.ashbyhq.com/coderabbit', Scrapers.ASHBYHQ, 'https://coderabbit.ai'),
    CompanyItem('kiln', 'https://jobs.ashbyhq.com/kiln.fi', Scrapers.ASHBYHQ, 'https://www.kiln.fi'),
    CompanyItem('dune', 'https://jobs.ashbyhq.com/dune', Scrapers.ASHBYHQ, 'https://dune.com'),
    CompanyItem('conduit', 'https://jobs.ashbyhq.com/Conduit', Scrapers.ASHBYHQ, 'https://conduit.xyz'),
    CompanyItem('paradigm.xyz', 'https://jobs.ashbyhq.com/paradigm', Scrapers.ASHBYHQ, 'https://www.paradigm.xyz'),
    CompanyItem('ellipsislabs', 'https://jobs.ashbyhq.com/ellipsislabs', Scrapers.ASHBYHQ,
                'https://ellipsislabs.xyz')
]

for company in companies:
    data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in data:
        print(entry)

driver.close()

end = time.time()
print(f"Time: {end - start:.2f} sec")
