import unittest
from selenium import webdriver
from src.scrape_consensys import ScrapeConsensys

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

jobs_data = ScrapeConsensys().getJobs(driver, "https://consensys.net/open-roles")
for entry in jobs_data:
    print(entry)

driver.close()


class TestScraper(unittest.TestCase):
    def test_upper(self):
        self.assertGreater(len(jobs_data), 1)


if __name__ == '__main__':
    unittest.main()
