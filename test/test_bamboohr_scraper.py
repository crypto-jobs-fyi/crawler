from selenium import webdriver

from src.company_item import CompanyItem
from src.scrape_bamboohr import ScrapeBamboohr

driver = webdriver.Chrome()
company_list = [
    CompanyItem('iyield', 'https://iyield.bamboohr.com/careers', ScrapeBamboohr, 'https://iyield.com'),
    CompanyItem('iofinnet', 'https://iofinnethr.bamboohr.com/jobs/?source=bamboohr', ScrapeBamboohr,
                'https://www.iofinnet.com'),
    CompanyItem('web3', 'https://web3.bamboohr.com/jobs', ScrapeBamboohr, 'https://web3.foundation'),
    CompanyItem('dappradar', 'https://dappradar.bamboohr.com/careers', ScrapeBamboohr,
                'https://dappradar.com')
]

for company in company_list:
    print(company.jobs_url)
    data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in data:
        print(entry)

driver.close()
