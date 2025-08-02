import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time

from selenium import webdriver

from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhq

start = time.time()

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
companies = [
    CompanyItem('langchain', 'https://jobs.ashbyhq.com/langchain', ScrapeAshbyhq, 'https://www.langchain.com'),
    CompanyItem('rain', 'https://jobs.ashbyhq.com/rain', ScrapeAshbyhq, 'https://www.raincards.xyz'),
    CompanyItem('exponential', 'https://jobs.ashbyhq.com/exponential', ScrapeAshbyhq, 'https://exponential.fi'),
    CompanyItem('kiln', 'https://jobs.ashbyhq.com/kiln.fi', ScrapeAshbyhq, 'https://www.kiln.fi'),
    CompanyItem('dune', 'https://jobs.ashbyhq.com/dune', ScrapeAshbyhq, 'https://dune.com'),
    CompanyItem('conduit', 'https://jobs.ashbyhq.com/Conduit', ScrapeAshbyhq, 'https://conduit.xyz'),
    CompanyItem('paradigm.xyz', 'https://jobs.ashbyhq.com/paradigm', ScrapeAshbyhq, 'https://www.paradigm.xyz'),
    CompanyItem('syndica', 'https://jobs.ashbyhq.com/syndica', ScrapeAshbyhq, 'https://www.sygnum.com'),
    CompanyItem('solana-foundation', 'https://jobs.ashbyhq.com/Solana%20Foundation', ScrapeAshbyhq,
                'https://www.sygnum.com'),
    CompanyItem('ellipsislabs', 'https://jobs.ashbyhq.com/ellipsislabs', ScrapeAshbyhq,
                'https://ellipsislabs.xyz')
]

for company in companies:
    data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in data:
        print(entry)

driver.close()

end = time.time()
print(f"Time: {end - start:.2f} sec")
