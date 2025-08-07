import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from src.scrape_nebius import ScrapeNebius


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url1 = "https://careers.nebius.com"
jobs = ScrapeNebius().getJobs(driver, url1)
for job in jobs:
    print(job)

driver.close()
