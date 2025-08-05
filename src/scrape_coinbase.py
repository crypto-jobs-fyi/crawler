import time

from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt

# https://www.coinbase.com/careers/positions
class ScrapeCoinbase(ScrapeIt):
    name = 'coinbase'

    def getJobs(self, driver, web_page, company='coinbase') -> list:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        driver.implicitly_wait(7)
        time.sleep(5)
        # open all departments
        acceptAll = driver.find_elements(By.XPATH, '//span[.="Accept all"]')
        if len(acceptAll) > 0:
            acceptAll[0].click()
            time.sleep(1)
        departments = driver.find_elements(By.XPATH, '//div[@data-testid="positions-department"]')
        print(f'[{self.name}] Found {len(departments)} departments.')
        for department in departments:
            department.click()
            time.sleep(1)
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
                "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
