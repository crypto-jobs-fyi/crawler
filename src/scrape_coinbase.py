import time

from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt

# https://www.coinbase.com/careers/positions
class ScrapeCoinbase(ScrapeIt):
    name = 'Coinbase'

    def getJobs(self, driver, web_page, company='coinbase') -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.get(web_page)
        driver.implicitly_wait(9)
        time.sleep(4)
        # open all departments
        acceptAll = driver.find_elements(By.XPATH, '//*[contains(text(), "Accept")]')
        if len(acceptAll) > 0:
            acceptAll[0].click()
            time.sleep(3)
        departments = driver.find_elements(By.XPATH, '//div[@data-testid="positions-department"]')
        self.log_info(
            "Departments found",
            company=company,
            department_count=len(departments),
            web_page=web_page,
        )
        for department in departments:
            department.click()
            time.sleep(3)
        group_elements = driver.find_elements(By.XPATH, '//div/a[contains(@href, "careers/positions")]')
        result = []
        for elem in group_elements:
            # job_name_elem = elem.find_element(By.CSS_SELECTOR, 'a')
            location_elem = elem.find_element(By.XPATH, './../p')
            job_url = elem.get_attribute('href')
            job_name = elem.text
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
