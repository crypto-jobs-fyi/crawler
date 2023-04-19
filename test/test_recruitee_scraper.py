from selenium import webdriver
from src.company_item import CompanyItem
from src.scrape_recruitee import ScrapeRecruitee


companies = [
    CompanyItem("ramp.network", "https://metrika.recruitee.com", ScrapeRecruitee, "https://ramp.network", "Payments")]

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

for company in companies:
    print(company.jobs_url)
    data = company.scraper_type().getJobs(driver, company.jobs_url)
    for entry in data:
        print(entry)

driver.close()
