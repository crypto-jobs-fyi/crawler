import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.scrape_it import ScrapeIt

def clean_location(location):
    location = location.replace('United States', 'US').replace('United Kingdom', 'UK').replace('Singapore, Singapore', 'Singapore').replace('New York, New York', 'New York')
    return location.strip()

# https://www.gemini.com/careers#open-roles
class ScrapeGemini(ScrapeIt):
    name = 'gemini'

    def getJobs(self, driver, web_page, company='gemini') -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.get(web_page)
        time.sleep(5)
        driver.implicitly_wait(9)
        accept: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, 'button[data-testid="cookie-accept-all"]')
        if len(accept) > 0:
            accept[0].click()
        result = []
        
        # open all departments 1 by 1
        departments = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="team-dropdown"]')
        self.log_info(
            "Departments found",
            company=company,
            department_count=len(departments),
            web_page=web_page,
        )
        for department in departments:
            driver.execute_script("arguments[0].scrollIntoView();", department)
            time.sleep(2)
            department.click()
            time.sleep(1)
            group_elements = driver.find_elements(By.CSS_SELECTOR, 'div[aria-expanded="true"] div[data-testid="job-element"]')
            for elem in group_elements:
                job_name_elem = elem.find_element(By.CSS_SELECTOR, 'a')
                location_elem = elem.find_element(By.CSS_SELECTOR, 'p[color="secondary"]')
                job_url = job_name_elem.get_attribute('href')
                job_name = job_name_elem.find_element(By.CSS_SELECTOR, 'span').text
                location = location_elem.text
                job = {
                    "company": company,
                    "title": job_name,
                    "location": clean_location(location),
                    "link": job_url
                }
                result.append(job)
        filtered_result = [item for item in result if item["location"]]
        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_found=len(result),
            jobs_scraped=len(filtered_result),
        )
        return filtered_result
