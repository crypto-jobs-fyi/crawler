import unittest

from selenium import webdriver
from src.company_item import CompanyItem
from src.scrape_greenhouse import ScrapeGreenhouse

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [
    CompanyItem('21co', 'https://boards.greenhouse.io/21co', ScrapeGreenhouse,
                'https://www.21.co', 'Web3 DeFi ETP'),
    CompanyItem('xapo', 'https://boards.greenhouse.io/xapo61', ScrapeGreenhouse,
                'https://www.xapobank.com', 'Web3 bank')
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
