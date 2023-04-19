from selenium import webdriver
from src.company_item import CompanyItem
from src.scrape_workable import ScrapeWorkable


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
company_list = [CompanyItem('cryptofinance', 'https://apply.workable.com/cryptofinance', ScrapeWorkable,
                            'https://www.crypto-finance.com', 'Exchange'),
                CompanyItem('bitstamp', 'https://apply.workable.com/bitstamp/#jobs', ScrapeWorkable,
                            'https://www.bitstamp.net', 'Exchange'),
                CompanyItem('smart-token-labs', 'https://apply.workable.com/smart-token-labs', ScrapeWorkable,
                            'https://smarttokenlabs.com', 'Web3 bridge'),
                CompanyItem('avantgarde', 'https://apply.workable.com/avantgarde', ScrapeWorkable,
                            'https://avantgarde.finance', 'Asset Management'),
                CompanyItem('stably', 'https://apply.workable.com/stably', ScrapeWorkable, 'https://stably.io',
                            'Stable Coin')]
#company_list.append(CompanyItem('bitget', 'https://apply.workable.com/bitget', ScrapeWorkable, 'https://www.bitget.com/en', 'Exchange'))

for company in company_list:
    print(company.jobs_url)
    data = company.scraper_type().getJobs(driver, company.jobs_url)
    for entry in data:
        print(entry)

driver.close()
