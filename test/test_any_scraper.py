import unittest

from selenium import webdriver

from src.company_item import CompanyItem
from src.scrape_greenhouse import ScrapeGreenhouse
from src.scrape_workable import ScrapeWorkable
from src.scrape_ashbyhq import ScrapeAshbyhq

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [
    CompanyItem('mina-foundation', 'https://apply.workable.com/mina-foundation', ScrapeWorkable,
                'https://www.minafoundation.com', 'ZK blockchain'),
    CompanyItem('logos', 'https://boards.greenhouse.io/logos', ScrapeGreenhouse,
                'https://gate.io', 'Web3 Exchange'),
    CompanyItem('lido', 'https://jobs.ashbyhq.com/PML', ScrapeAshbyhq,
                'https://lido.fi', 'Web3 Staking'),
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
