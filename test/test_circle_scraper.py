import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from src.scrape_circle import ScrapeCircle


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url1 = "https://careers.circle.com/us/en/search-results"
jobs = ScrapeCircle().getJobs(driver, url1)
for job in jobs:
    print(job)

driver.close()
