import time

from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt

# https://careers.robinhood.com
class ScrapeRobinhood(ScrapeIt):
    name = 'robinhood'

    def getJobs(self, driver, web_page, company='robinhood') -> list:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        driver.implicitly_wait(5)
        time.sleep(5)
        # open all departments
        acceptAll = driver.find_elements(By.XPATH, '//span[.="Accept all"]')
        if len(acceptAll) > 0:
            acceptAll[0].click()
            time.sleep(1)
        departments = driver.find_elements(By.XPATH, '//div[@data-filter and contains(@class, "accordion")]')
        print(f'[{self.name}] Found {len(departments)} departments.')
        for department in departments:
            department.click()
            time.sleep(1)
        group_elements = driver.find_elements(By.XPATH, '//div[@id="jobs-data"]//p[@class="job"]')
        result = []
        for elem in group_elements:
            job_elem = elem.find_element(By.XPATH, './a')
            location = elem.get_attribute('data-location')
            job_url = job_elem.get_attribute('href')
            job_name = job_elem.text
            job = {
                "company": company,
                "title": job_name,
                "location": location,
                "link": job_url
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
