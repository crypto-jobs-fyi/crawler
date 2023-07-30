import unittest

from selenium import webdriver
from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_greenhouse import ScrapeGreenhouse
from src.scrape_workable import ScrapeWorkable

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [
    CompanyItem('center', 'https://jobs.ashbyhq.com/center', ScrapeAshbyhq,
                'https://center.app', 'Web3 NFT Data'),
    CompanyItem('Sui.Foundation', 'https://jobs.ashbyhq.com/Sui%20Foundation', ScrapeAshbyhq,
                'https://sui.io', 'Web3 blockchain'),
    CompanyItem('21co', 'https://boards.greenhouse.io/21co', ScrapeGreenhouse,
                'https://www.21.co', 'Web3 DeFi ETP'),
    CompanyItem('paraswap', 'https://apply.workable.com/paraswap', ScrapeWorkable,
                'https://www.paraswap.io', 'Web3 DeFi aggregator'),
    CompanyItem('stakefish', 'https://apply.workable.com/stakefish',
                ScrapeWorkable, 'https://stake.fish', 'Web3 ETH staking')
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
