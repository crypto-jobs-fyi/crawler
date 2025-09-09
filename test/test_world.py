import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from src.scrape_world import ScrapeWorld


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url = "https://world.org/careers"
jobs = ScrapeWorld().getJobs(driver, url, 'worldcoin')
for job in jobs:
    print(job)

driver.close()
