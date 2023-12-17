import unittest

from selenium import webdriver

from src.company_item import CompanyItem
from src.scrape_lever import ScrapeLever
from src.scrape_greenhouse import ScrapeGreenhouse
from src.scrape_ashbyhq import ScrapeAshbyhq

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [
    CompanyItem('xlabs', 'https://boards.greenhouse.io/xlabs', ScrapeGreenhouse,
                'https://www.xlabs.xyz', 'Web3 Infra'),
    CompanyItem('auroralabs', 'https://jobs.lever.co/aurora-dev', ScrapeLever,
                'https://auroralabs.dev', 'EVM blockchain'),
    CompanyItem('linera.io', 'https://jobs.ashbyhq.com/linera.io', ScrapeAshbyhq,
                'https://linera.io', 'Layer-1 blockchain'),
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
