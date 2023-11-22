import unittest

from selenium import webdriver

from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_status import ScrapeStatus
from src.scrape_enjin import ScrapeEnjin

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [
    CompanyItem('nomic.foundation', 'https://jobs.ashbyhq.com/nomic.foundation', ScrapeAshbyhq,
                'https://nomic.foundation', 'Web3 Infra'),
    CompanyItem('status', 'https://status.app/jobs', ScrapeStatus,
                'https://status.app', 'Web3 Messanger'),
    CompanyItem('enjin', 'https://enjin.io/opportunities#positions', ScrapeEnjin,
                'https://enjin.io', 'Web3 Blockchain'),
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
