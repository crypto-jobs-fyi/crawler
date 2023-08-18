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
    CompanyItem('blox-route', 'https://jobs.lever.co/blox-route', ScrapeLever,
                'https://bloxroute.com', 'Web3 MEV DeFi infra'),
    CompanyItem('Sui.Foundation', 'https://jobs.ashbyhq.com/Sui%20Foundation', ScrapeAshbyhq,
                'https://sui.io', 'Web3 blockchain'),
    CompanyItem('shardeum', 'https://boards.greenhouse.io/shardeumfoundation', ScrapeGreenhouse,
                'https://shardeum.org', 'Web3 L1'),
    CompanyItem('paraswap', 'https://apply.workable.com/paraswap', ScrapeWorkable,
                'https://www.paraswap.io', 'Web3 DeFi aggregator')
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
