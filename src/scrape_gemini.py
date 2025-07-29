import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.scrape_it import ScrapeIt

# https://www.gemini.com/careers#open-roles
class ScrapeGemini(ScrapeIt):
    name = 'gemini'

    def getJobs(self, driver, web_page, company='gemini') -> list:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        time.sleep(5)
        driver.implicitly_wait(9)
        accept: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, 'section[id="cookiePolicyAgreement"] button')
        if len(accept) > 0:
            accept[0].click()
        result = []
        
        # open all departments 1 by 1
        departments = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="team-dropdown"]')
        print(f'[{self.name}] Found {len(departments)} departments.')
        for department in departments:
            driver.execute_script("arguments[0].scrollIntoView();", department)
            time.sleep(2)
            department.click()
            time.sleep(1)
            group_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="job-element"]')
            for elem in group_elements:
                job_name_elem = elem.find_element(By.CSS_SELECTOR, 'a')
                location_elem = elem.find_element(By.CSS_SELECTOR, 'p[color="secondary"]')
                job_url = job_name_elem.get_attribute('href')
                job_name = job_name_elem.find_element(By.CSS_SELECTOR, 'span').text
                location = location_elem.text
                job = {
                    "company": company,
                    "title": job_name,
                    "location": location,
                    "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
                }
                result.append(job)
        filter_result = [item for item in result if item["location"] != ""]
        print(f'[{self.name}] Scraped {len(filter_result)} jobs from {web_page}')
        return result
