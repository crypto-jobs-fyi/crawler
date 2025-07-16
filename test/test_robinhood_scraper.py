import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from src.scrape_robinhood import ScrapeRobinhood


options = webdriver.ChromeOptions()
# Coinbase may not work with headless mode, uncomment the next line to test
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url1 = "https://careers.robinhood.com"
jobs = ScrapeRobinhood().getJobs(driver, url1)
for job in jobs:
    print(job)

driver.close()
