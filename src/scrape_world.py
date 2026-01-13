import time

from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt

# https://world.org/careers
class ScrapeWorld(ScrapeIt):
    name = 'Worldcoin'

    def getJobs(self, driver, web_page, company='worldcoin') -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.get(web_page)
        driver.implicitly_wait(5)
        time.sleep(4)
        group_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="job-card"]')
        result = []
        for elem in group_elements:
            job_url_elem = elem.find_element(By.CSS_SELECTOR, 'a')
            location_elem = elem.find_elements(By.CSS_SELECTOR, 'p')[1]
            job_name_elem = elem.find_elements(By.CSS_SELECTOR, 'p')[0]
            job_url = job_url_elem.get_attribute('href')
            job_name = job_name_elem.text
            location = location_elem.text
            job = {
                "company": company,
                "title": job_name,
                "location": location,
                "link": job_url
            }
            result.append(job)
        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_found=len(group_elements),
            jobs_scraped=len(result),
        )
        return result
