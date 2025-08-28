import time
from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


class ScrapeGrog(ScrapeIt):
    name = 'grog'

    def clean_location(self, location: str) -> str:
        return location.strip().replace('United States', 'US').replace('United Kingdom', 'UK').replace('United Arab Emirates', 'UAE').replace('\n', ' ')


    def getJobs(self, driver, web_page, company = 'grog') -> list:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.implicitly_wait(5)
        driver.get(web_page)
        time.sleep(3)
        group_elements = driver.find_elements(By.CSS_SELECTOR, 'li a[class*=listing__link]')
        result = []
        for elem in group_elements:
            job_name_elem = elem.find_element(By.CSS_SELECTOR, 'p[class*=listing__title]')
            job_name: str = job_name_elem.text
            job_url: str = elem.get_attribute('href')
            location = elem.find_element(By.CSS_SELECTOR, 'p span[class*=listing__office]')
            location_text: str = self.clean_location(location.text)
            job = {
                "company": company,
                "title": job_name,
                "location": location_text,
                "link": job_url
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
