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
    CompanyItem('ondofinance', 'https://jobs.lever.co/ondofinance', ScrapeLever, 'https://ondo.finance',
                'Web3 yield'),
    CompanyItem('Caldera', 'https://jobs.ashbyhq.com/Caldera', ScrapeAshbyhq, 'https://www.caldera.xyz',
                'L2 Rollups'),
    CompanyItem("ritual", "https://boards.greenhouse.io/ritual", ScrapeGreenhouse,
                "https://ritual.net", 'WEB3 AI'),
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
