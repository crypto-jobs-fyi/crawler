import unittest

from selenium import webdriver
from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_greenhouse import ScrapeGreenhouse
from src.scrape_workable import ScrapeWorkable
from src.scrape_lever import ScrapeLever

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [
    CompanyItem('theblock', 'https://jobs.lever.co/theblockcrypto', ScrapeLever,
                'https://www.theblock.co', 'Web3 Info'),
    CompanyItem('superfluid', 'https://apply.workable.com/superfluid/#jobs', ScrapeWorkable,
                'https://www.superfluid.finance', 'Web3'),
    CompanyItem('OpenSea', 'https://jobs.ashbyhq.com/OpenSea', ScrapeAshbyhq,
                'https://www.station.express', 'Web3 infra'),
    CompanyItem('shardeum', 'https://boards.greenhouse.io/shardeumfoundation', ScrapeGreenhouse,
                'https://shardeum.org', 'Web3 L1'),
]

for company in company_list:
    jobs_data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in jobs_data:
        print(entry)

driver.close()


class TestScraper(unittest.TestCase):
    def test_upper(self):
        self.assertGreater(len(jobs_data), 1)


if __name__ == '__main__':
    unittest.main()
