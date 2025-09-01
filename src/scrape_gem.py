import time
from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


class ScrapeGem(ScrapeIt):
    name = 'GEM'

    def clean_location(self, location: str) -> str:
        return location.strip().replace('United States', 'US').replace('United Kingdom', 'UK').replace('United Arab Emirates', 'UAE').replace('\n', ' ')


    def getJobs(self, driver, web_page, company) -> list:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.implicitly_wait(7)
        driver.get(web_page)
        time.sleep(3)
        group_elements = len(driver.find_elements(By.CSS_SELECTOR, 'li[class*=jobPosting]'))
        result = []
        for i in range(group_elements):
            elem = driver.find_elements(By.CSS_SELECTOR, 'li[class*=jobPosting]')[i]
            job_name_elem = elem.find_element(By.CSS_SELECTOR, 'div[class*=jobTitle]')
            job_name: str = job_name_elem.text
            location = elem.find_element(By.CSS_SELECTOR, 'div[class*=jobAttributes]')
            location_text: str = self.clean_location(location.text)
            job_name_elem.click()
            time.sleep(3)
            job_url: str = driver.current_url
            driver.find_element(By.CSS_SELECTOR, 'a[class*=linkButton]').click()

            job = {
                "company": company,
                "title": job_name,
                "location": location_text,
                "link": job_url
            }
            result.append(job)
        print(f'[{self.name}] Found {group_elements} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
