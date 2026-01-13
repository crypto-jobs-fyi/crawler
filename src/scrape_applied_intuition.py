import time

from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt

class ScrapeAppliedIntuition(ScrapeIt):
    name = 'Applied Intuition'

    def clean_location(self, location: str) -> str:
        location = location.replace('United States', 'US').replace('United Kingdom', 'UK').replace('United Arab Emirates', 'UAE').replace('Tokyo Prefecture', 'Tokyo').replace('Stockholm, Stockholm', 'Stockholm')
        return location.strip().strip('-')

    def getJobs(self, driver, web_page, company='applied_intuition') -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.get(web_page)
        driver.implicitly_wait(9)
        time.sleep(3)
        # open all departments
        departments = driver.find_elements(By.CSS_SELECTOR, '.department-header-flex-wrapper')
        self.log_info(
            "Departments found",
            company=company,
            department_count=len(departments),
            web_page=web_page,
        )
        for department in departments:
            department.click()
            time.sleep(3)
        group_elements = driver.find_elements(By.CSS_SELECTOR, '.job-flex-wrapper')
        result = []
        for elem in group_elements:
            job_name_elem = elem.find_element(By.CSS_SELECTOR, '.job-title-text')
            location_elem = elem.find_element(By.CSS_SELECTOR, '.job-location')
            job_url = elem.get_attribute('href')
            job_name = job_name_elem.text
            location : str = location_elem.text
            job = {
                "company": company,
                "title": job_name,
                "location": self.clean_location(location),
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
