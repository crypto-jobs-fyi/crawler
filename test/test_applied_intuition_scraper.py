import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.scrape_applied_intuition import ScrapeAppliedIntuition
from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url = "https://www.appliedintuition.com/careers#job-listings"
jobs = ScrapeAppliedIntuition().getJobs(driver, url)
for job in jobs:
    print(job)

driver.close()
