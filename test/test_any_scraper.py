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
    CompanyItem('Tenderly', 'https://jobs.lever.co/Tenderly', ScrapeLever,
                'https://tenderly.co', 'Web3 Infra'),
    CompanyItem('zodia-custody', 'https://apply.workable.com/zodia-custody', ScrapeWorkable,
                'https://zodia.io', 'Web3 Custody'),
    CompanyItem('cryptio', 'https://jobs.ashbyhq.com/cryptio', ScrapeAshbyhq,
                'https://cryptio.co', 'Web3 Back Office'),
    CompanyItem('dydx', 'https://boards.greenhouse.io/dydx', ScrapeGreenhouse,
                'https://dydx.exchange', 'Web3 Exchange'),
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
