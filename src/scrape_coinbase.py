import time

from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt, write_jobs


class ScrapeCoinbase(ScrapeIt):
    name = 'coinbase'

    def getJobs(self, driver, web_page, company='coinbase') -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        driver.implicitly_wait(9)
        time.sleep(5)
        # open all departments
        departments = driver.find_elements(By.CSS_SELECTOR, 'div[class*="Department__DepartmentHeader-"] svg')
        print(f'[{self.name}] Found {len(departments)} departments.')
        for department in departments:
            department.click()
        group_elements = driver.find_elements(By.CSS_SELECTOR, 'div[class*="Department__Job-"]')
        result = []
        for elem in group_elements:
            job_name_elem = elem.find_element(By.CSS_SELECTOR, 'a')
            location_elem = elem.find_element(By.CSS_SELECTOR, 'p')
            job_url = job_name_elem.get_attribute('href')
            job_name = job_name_elem.text
            location = location_elem.text
            job = {
                "company": company,
                "title": job_name,
                "location": location,
                "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        write_jobs(result)
        return result
