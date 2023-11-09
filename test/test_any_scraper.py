import unittest

from selenium import webdriver

from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_tusd import ScrapeTusd
from src.scrape_enjin import ScrapeEnjin

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [
    CompanyItem('ethglobal', 'https://jobs.ashbyhq.com/ethglobal', ScrapeAshbyhq,
                'wip', 'wip'),
    CompanyItem('tusd', 'https://tusd.io/about', ScrapeTusd,
                'https://tusd.io', 'Web3 Stable-coin'),
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
