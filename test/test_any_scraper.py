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
    CompanyItem('fortress', 'https://jobs.lever.co/fortress', ScrapeLever,
                'https://fortress.io', 'Web3 Custody'),
    CompanyItem('zodia-custody', 'https://apply.workable.com/zodia-custody', ScrapeWorkable,
                'https://zodia.io', 'Web3 Custody'),
    CompanyItem('Bastion', 'https://jobs.ashbyhq.com/Bastion', ScrapeAshbyhq,
                'https://www.bastion.com', 'Web3 Infra and Wallet'),
    CompanyItem('osl', 'https://boards.eu.greenhouse.io/osl', ScrapeGreenhouse,
                'https://shardeum.org', 'Web3 Custody Exchange'),
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
