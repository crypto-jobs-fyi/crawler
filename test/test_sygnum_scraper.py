import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from src.scrape_sygnum import ScrapeSygnum


options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url1 = "https://www.sygnum.com/careers-portal"
jobs = ScrapeSygnum().getJobs(driver, url1)
for job in jobs:
    print(job)

driver.close()
