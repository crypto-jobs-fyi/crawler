import time
from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


class ScrapeCleo(ScrapeIt):
    name = 'Cleo'

    def clean_location(self, location: str) -> str:
        return location.strip().replace('United States', 'US').replace('United Kingdom', 'UK').replace('United Arab Emirates', 'UAE').replace('\n', ' ')

    def get_last_or_default_location(self, locations: list) -> str:
        if len(locations) > 0:
            return self.clean_location(locations[len(locations) - 1].text)
        return 'UK'

    def getJobs(self, driver, web_page, company = 'Cleo') -> list:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.implicitly_wait(5)
        driver.get(web_page)
        time.sleep(3)
        cookie_banners = driver.find_elements(By.XPATH, '//button/span[text()="Allow all cookies"]')
        if len(cookie_banners) > 0:
            print(f'[{self.name}] Accept cookies')
            cookie_banners[0].click()
            time.sleep(2)
        group_elements = driver.find_elements(By.CSS_SELECTOR, 'a[aria-label="position-link"]')
        result = []
        for elem in group_elements:
            job_name_elem = elem.find_element(By.CSS_SELECTOR, 'span span')
            job_name: str = job_name_elem.text.split('\n')[0]
            job_url: str = elem.get_attribute('href')
            locations: list = elem.find_elements(By.CSS_SELECTOR, 'div[data-testid="location-row"]')
            print('Locations for job: ', job_name, len(locations))
            location_text: str = self.get_last_or_default_location(locations)
            job = {
                "company": company,
                "title": job_name,
                "location": location_text,
                "link": job_url
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
