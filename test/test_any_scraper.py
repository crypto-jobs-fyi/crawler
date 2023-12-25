import unittest

from selenium import webdriver

from src.company_item import CompanyItem
from src.scrape_lever import ScrapeLever
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_tether import ScrapeTether

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [
    CompanyItem("tether", "https://tether.recruitee.com", ScrapeTether, "https://tether.to/en",
                        "Stable Coin"),
    CompanyItem('omni-network', 'https://jobs.lever.co/omni-network', ScrapeLever,
                'https://omni.network', 'Web3 interchain'),
    CompanyItem('windranger', 'https://jobs.ashbyhq.com/windranger', ScrapeAshbyhq,
                'https://windranger.io', 'DeFi Development'),
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
