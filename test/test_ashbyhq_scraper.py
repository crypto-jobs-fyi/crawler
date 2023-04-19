from selenium import webdriver
from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhq

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
companies = [CompanyItem('syndica', 'https://jobs.ashbyhq.com/syndica', ScrapeAshbyhq, 'https://www.sygnum.com',
                            'Crypto bank'),
             CompanyItem('solana-foundation', 'https://jobs.ashbyhq.com/Solana%20Foundation', ScrapeAshbyhq, 'https://www.sygnum.com',
                            'Crypto bank'),
             CompanyItem('ellipsislabs', 'https://jobs.ashbyhq.com/ellipsislabs', ScrapeAshbyhq, 'https://ellipsislabs.xyz', 'Trading Protocol')
             ]

for company in companies:
    print(company.jobs_url)
    data = company.scraper_type().getJobs(driver, company.jobs_url)
    for entry in data:
        print(entry)

driver.close()
