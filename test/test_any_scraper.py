import unittest

from selenium import webdriver

from src.company_item import CompanyItem
from src.scrape_lever import ScrapeLever
from src.scrape_bamboohr import ScrapeBamboohr

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

company_list = [
    CompanyItem('iyield', 'https://iyield.bamboohr.com/careers', ScrapeBamboohr, 'https://iyield.com',
                'Web3 Fin Planning'),
    CompanyItem('wirex', 'https://wirex.bamboohr.com/careers', ScrapeBamboohr, 'https://wirexapp.com',
                'Web3 card'),
    CompanyItem('sygnum', 'https://sygnum.bamboohr.com/careers', ScrapeBamboohr, 'https://www.sygnum.com',
                'Crypto bank'),
    CompanyItem("chainstack", "https://chainstack.bamboohr.com/careers", ScrapeBamboohr,
                "https://chainstack.com", "Infra"),
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
