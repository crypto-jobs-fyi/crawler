from selenium import webdriver
from src.company_item import CompanyItem
from src.scrape_workable import ScrapeWorkable

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
company_list = [
    CompanyItem('dydxopsdao', 'https://apply.workable.com/dydx-operations-trust', ScrapeWorkable,
                'https://dydxopsdao.com'),
    CompanyItem('almanak', 'https://apply.workable.com/almanak-blockchain-labs-ag', ScrapeWorkable,
                'https://almanak.co'),
    CompanyItem('walletconnect', 'https://apply.workable.com/walletconnect', ScrapeWorkable,
                'https://walletconnect.com'),
    CompanyItem('bitstamp', 'https://apply.workable.com/bitstamp/#jobs', ScrapeWorkable,
                'https://www.bitstamp.net'),
    CompanyItem('smart-token-labs', 'https://apply.workable.com/smart-token-labs', ScrapeWorkable,
                'https://smarttokenlabs.com'),
    CompanyItem('avantgarde', 'https://apply.workable.com/avantgarde', ScrapeWorkable,
                'https://avantgarde.finance'),
    CompanyItem('stably', 'https://apply.workable.com/stably', ScrapeWorkable, 'https://stably.io')
]
# company_list.append(CompanyItem('bitget', 'https://apply.workable.com/bitget', ScrapeWorkable, 'https://www.bitget.com/en', 'Exchange'))

for company in company_list:
    print(company.jobs_url)
    data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in data:
        print(entry)

driver.close()
