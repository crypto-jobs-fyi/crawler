import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from src.scrape_gem import ScrapeGem


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url = "https://jobs.gem.com/soundhound"
jobs = ScrapeGem().getJobs(driver, url, "soundhound")
for job in jobs:
    print(job)

driver.close()
