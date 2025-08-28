import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scrape_c3 import ScrapeC3
from selenium import webdriver

# python test/test_c3_scraper.py
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url1 = "https://c3.ai/careers"
jobs = ScrapeC3().getJobs(driver, url1)
for job in jobs:
    print(job)
print(f'Total jobs: {len(jobs)}')
driver.close()
