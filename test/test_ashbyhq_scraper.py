from selenium import webdriver
from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhq

import time 
start = time.time()

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
companies = [
    CompanyItem('kiln', 'https://jobs.ashbyhq.com/kiln.fi', ScrapeAshbyhq, 'https://www.kiln.fi', 'Staking'),
    CompanyItem('dune', 'https://jobs.ashbyhq.com/dune', ScrapeAshbyhq, 'https://dune.com',
                'Web3 data'),
    CompanyItem('conduit', 'https://jobs.ashbyhq.com/Conduit', ScrapeAshbyhq, 'https://conduit.xyz',
                'Infrastructure'),
    CompanyItem('paradigm.xyz', 'https://jobs.ashbyhq.com/paradigm', ScrapeAshbyhq, 'https://www.paradigm.xyz',
                'Web3 data'),
    CompanyItem('syndica', 'https://jobs.ashbyhq.com/syndica', ScrapeAshbyhq, 'https://www.sygnum.com',
                'Crypto bank'),
    CompanyItem('solana-foundation', 'https://jobs.ashbyhq.com/Solana%20Foundation', ScrapeAshbyhq,
                'https://www.sygnum.com',
                'Crypto bank'),
    CompanyItem('ellipsislabs', 'https://jobs.ashbyhq.com/ellipsislabs', ScrapeAshbyhq,
                'https://ellipsislabs.xyz', 'Trading Protocol')
]

for company in companies:
    data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in data:
        print(entry)

driver.close()

end = time.time()
print(f"Time: {end-start:.2f} sec")