import time

from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


class ScrapeConsensys(ScrapeIt):
    name = 'CONSENSYS'

    def getJobs(self, driver, web_page, company='consensys') -> list:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        driver.implicitly_wait(9)
        time.sleep(2)
        # scroll to bottom to load all jobs
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        group_elements = driver.find_elements(By.XPATH, '//a[contains(@class, "card-job")]')
        result = []
        for elem in group_elements:
            link_elem = elem
            job_name_elem = elem.find_element(By.CSS_SELECTOR, 'h5')
            job_url = link_elem.get_attribute('href')
            location_elem = elem.find_element(By.XPATH, './/div[contains(@class, "job-location")]')
            job = {
                "company": company,
                "title": job_name_elem.text,
                "location": location_elem.text.replace('UNITED STATES', 'US'),
                "link": job_url
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
