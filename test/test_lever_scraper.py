
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from selenium import webdriver

from src.company_item import CompanyItem
from src.scrape_lever import ScrapeLever

company_list = [
    CompanyItem("oxylabs", "https://jobs.lever.co/oxylabs", ScrapeLever, "https://www.oxylabs.io"),
    CompanyItem('ethenalabs', 'https://jobs.lever.co/ethenalabs', ScrapeLever,
                'https://www.ethena.fi'),
]

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

for company in company_list:
    data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in data:
        print(entry)

driver.close()
