import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from src.scrape_paxos import ScrapePaxos


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url1 = "https://www.paxos.com/jobs"
jobs = ScrapePaxos().getJobs(driver, url1)
for job in jobs:
    print(job)

driver.close()
