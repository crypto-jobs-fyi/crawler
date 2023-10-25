import unittest

from selenium import webdriver

from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_lever import ScrapeLever
from src.scrape_lmax import ScrapeLmax
from src.scrape_workable import ScrapeWorkable

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [
    CompanyItem('HQxyz', 'https://jobs.lever.co/HQxyz', ScrapeLever,
                'https://www.hq.xyz', 'Web3 Back Office'),
    CompanyItem('io-global', 'https://apply.workable.com/io-global/#jobs', ScrapeWorkable,
                'https://iohk.io', 'Web3 Blockchain'),
    CompanyItem('cointracker', 'https://jobs.ashbyhq.com/cointracker', ScrapeAshbyhq,
                'https://www.cointracker.io', 'Web3 Back Office'),
    CompanyItem('lmax', 'https://careers.lmax.com/job-openings', ScrapeLmax,
                'https://www.lmax.com', 'Web3 browser'),
]

for company in company_list:
    jobs_data = company.scraper_type().getJobs(driver, company.jobs_url, company.company_name)
    for entry in jobs_data:
        print(entry)

driver.close()


class TestScraper(unittest.TestCase):
    def test_jobs_data(self):
        self.assertGreater(len(jobs_data), 1, f"Empty list for {company.company_name}")


if __name__ == '__main__':
    unittest.main()
