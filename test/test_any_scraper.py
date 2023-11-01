import unittest

from selenium import webdriver

from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_lever import ScrapeLever

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [
    CompanyItem('swellnetwork', 'https://jobs.lever.co/swellnetwork.io', ScrapeLever,
                'https://www.swellnetwork.io', 'Web3 ETH LST'),
    #CompanyItem('cointracker', 'https://jobs.ashbyhq.com/cointracker', ScrapeAshbyhq,
    #            'https://www.cointracker.io', 'Web3 Back Office'),
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
