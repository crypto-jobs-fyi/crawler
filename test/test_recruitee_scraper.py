from selenium import webdriver
from src.company_item import CompanyItem
from src.scrape_recruitee import ScrapeRecruitee


companies = [
    CompanyItem("bitfinex", "https://bitfinex.recruitee.com", ScrapeRecruitee, "https://www.bitfinex.com",
                "Exchange"),
]

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

for company in companies:
    print(company.jobs_url)
    data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in data:
        print(entry)

driver.close()
