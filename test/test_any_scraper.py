import unittest

from selenium import webdriver

from src.company_item import CompanyItem
from src.scrape_phantom import ScrapePhantom
from src.scrape_greenhouse import ScrapeGreenhouse
from src.scrape_ashbyhq import ScrapeAshbyhq

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [
    CompanyItem('xlabs', 'https://boards.greenhouse.io/xlabs', ScrapeGreenhouse,
                'https://www.xlabs.xyz', 'Web3 Infra'),
    CompanyItem('phantom', 'https://phantom.app/jobs', ScrapePhantom,
                'https://gate.io', 'Web3 Exchange'),
    CompanyItem('linera.io', 'https://jobs.ashbyhq.com/linera.io', ScrapeAshbyhq,
                'https://linera.io', 'Layer-1 blockchain'),
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
