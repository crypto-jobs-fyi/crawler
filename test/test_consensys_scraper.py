from selenium import webdriver
from src.scrape_consensys import ScrapeConsensys


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
jobs = ScrapeConsensys().getJobs(driver, "https://consensys.net/open-roles")
for job in jobs:
    print(job)

driver.close()
