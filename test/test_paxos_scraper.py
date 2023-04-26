from selenium import webdriver
from src.scrape_paxos import ScrapePaxos


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
url1 = "https://paxos.com/job-posts/?_sft_department=compliance,engineering,finance-accounting,hr-talent,information-technology,legal,operations,product&_sft_office=us"
url2 = url1 + "&sf_paged=2"
jobs = ScrapePaxos().getJobs(driver, url1)
for job in jobs:
    print(job)

driver.close()
