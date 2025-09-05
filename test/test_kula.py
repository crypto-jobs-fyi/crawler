import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from src.scrape_kula import ScrapeKula


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url = "https://careers.kula.ai/paradigm"
jobs = ScrapeKula().getJobs(driver, url, 'paradigm')
for job in jobs:
    print(job)

driver.close()
