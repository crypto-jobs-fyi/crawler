import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from src.scrape_cleo import ScrapeCleo


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url = "https://revolutpeople.com/cleo/public/careers"
jobs = ScrapeCleo().getJobs(driver, url)
for job in jobs:
    print(job)

driver.close()
