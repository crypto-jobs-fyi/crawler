import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from src.scrape_avara import ScrapeAvara


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url1 = "https://avara.xyz/careers"
jobs = ScrapeAvara().getJobs(driver, url1)
for job in jobs:
    print(job)

driver.close()
