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
    CompanyItem('clabs', 'https://jobs.lever.co/clabs', ScrapeLever, 'https://clabs.co',
                'Web3 Celo'),
    CompanyItem('succinct', 'https://jobs.ashbyhq.com/succinct', ScrapeAshbyhq, 'https://succinct.xyz',
                'Zero-knowledge proofs'),
    CompanyItem("wyndlabs", "https://boards.greenhouse.io/wyndlabs", ScrapeGreenhouse,
                "https://www.wyndlabs.ai", 'WEB3 AI'),
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
