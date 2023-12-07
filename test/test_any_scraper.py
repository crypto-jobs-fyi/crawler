import unittest

from selenium import webdriver

from src.company_item import CompanyItem
from src.scrape_lever import ScrapeLever
from src.scrape_base import ScrapeBase
from src.scrape_ashbyhq import ScrapeAshbyhq

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [
    CompanyItem('base', 'https://base.org/jobs', ScrapeBase,
                'https://base.org', 'Web3 Infra'),
    CompanyItem('gate.io', 'https://jobs.lever.co/gate.io', ScrapeLever,
                'https://gate.io', 'Web3 Exchange'),
    CompanyItem('shadow', 'https://jobs.ashbyhq.com/shadow', ScrapeAshbyhq,
                'https://www.shadow.xyz', 'Web3 Infra'),
]

for company in company_list:
    jobs_data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in jobs_data:
        print(entry)

driver.close()


class TestScraper(unittest.TestCase):
    def test_jobs_data(self):
        self.assertGreater(len(jobs_data), 0, f"Empty list for {company.company_name}")


if __name__ == '__main__':
    unittest.main()
