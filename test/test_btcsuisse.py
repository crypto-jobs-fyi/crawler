import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from src.scrape_bitcoinsuisse import ScrapeBitcoinSuisse


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url = "https://bitcoin-suisse.onlyfy.jobs"
jobs = ScrapeBitcoinSuisse().getJobs(driver, url)
for job in jobs:
    print(job)

driver.close()
