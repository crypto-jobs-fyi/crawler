from selenium import webdriver
from src.company_item import CompanyItem
from src.scrape_bamboohr import ScrapeBamboohr

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
company_list = [
    CompanyItem('iyield', 'https://iyield.bamboohr.com/careers', ScrapeBamboohr, 'https://iyield.com',
                'Web3 Fin Planning'),
    CompanyItem('sygnum', 'https://sygnum.bamboohr.com/careers', ScrapeBamboohr, 'https://www.sygnum.com',
                'Crypto bank'),
    CompanyItem('iofinnet', 'https://iofinnethr.bamboohr.com/jobs/?source=bamboohr', ScrapeBamboohr,
                'https://www.iofinnet.com', 'Custody'),
    CompanyItem('web3', 'https://web3.bamboohr.com/jobs', ScrapeBamboohr, 'https://web3.foundation',
                'web3'),
    CompanyItem('dappradar', 'https://dappradar.bamboohr.com/careers', ScrapeBamboohr,
                'https://dappradar.com', 'Exchange & NFT')
]

for company in company_list:
    print(company.jobs_url)
    data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in data:
        print(entry)

driver.close()
