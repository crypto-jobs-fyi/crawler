import unittest

from selenium import webdriver

from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_lever import ScrapeLever
from src.scrape_coinbase import ScrapeCoinbase
from src.scrape_gemini import ScrapeGemini

options = webdriver.ChromeOptions()
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [
    CompanyItem('coinbase', 'https://www.coinbase.com/careers/positions', ScrapeCoinbase,
                'https://www.coinbase.com', 'Web3 Exchange'),
    CompanyItem('gemini', 'https://www.gemini.com/careers', ScrapeGemini,
                'https://www.gemini.com', 'Web3 Exchange'),
    #CompanyItem('HQxyz', 'https://jobs.lever.co/HQxyz', ScrapeLever,
    #            'https://www.hq.xyz', 'Web3 Back Office'),
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
        self.assertGreater(len(jobs_data), 1, f"Empty list for {company.company_name}")


if __name__ == '__main__':
    unittest.main()
