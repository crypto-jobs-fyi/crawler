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
    CompanyItem('safe.global', 'https://jobs.ashbyhq.com/safe.global', ScrapeAshbyhq,
                'https://safe.global', 'Web3 custody'),
    CompanyItem('RabbitHole', 'https://jobs.ashbyhq.com/RabbitHole', ScrapeAshbyhq,
                'https://rabbithole.gg', 'Web3 gaming'),
    CompanyItem('21co', 'https://boards.greenhouse.io/21co', ScrapeGreenhouse,
                'https://www.21.co', 'Web3 DeFi ETP'),
    CompanyItem('prepo', 'https://apply.workable.com/prepo', ScrapeWorkable,
                'https://prepo.io', 'Web3 pre-IPO trading'),
    CompanyItem('clockwork-labs', 'https://apply.workable.com/clockwork-labs',
                ScrapeWorkable, 'https://clockworklabs.io', 'Web3 gaming')
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
