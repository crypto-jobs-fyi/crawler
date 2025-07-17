import time

from selenium.webdriver.common.by import By

from src.scrape_it import ScrapeIt

# https://www.gemini.com/careers#open-roles
class ScrapeGemini(ScrapeIt):
    name = 'gemini'

    def getJobs(self, driver, web_page, company='gemini') -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        time.sleep(5)
        driver.implicitly_wait(12)
        result = []
        view_button = driver.find_element(By.XPATH, '//button[.="View open roles"]')
        view_button.click()
        accept = driver.find_elements(By.CSS_SELECTOR, 'section[id="cookiePolicyAgreement"] button')
        if len(accept) > 0:
            accept[0].click()
        # open all departments
        departments = driver.find_elements(By.CSS_SELECTOR, 'section div[data-testid="collapse-header"]')
        print(f'[{self.name}] Found {len(departments)} departments.')
        for department in departments:
            department.click()
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
