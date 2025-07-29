from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt
import time


def clean_location(location):
    location = location.strip().strip('-').replace('United States', 'US').replace('United Kingdom', 'UK').replace('United Arab Emirates', 'UAE')
    return location

def get_jobs(driver, company):
    group_elements = driver.find_elements(By.CSS_SELECTOR, 'div [class="job-post"]')
    result = []
    print(f'[GREENHOUSE] Found {len(group_elements)} jobs. Scraping jobs...')
    for elem in group_elements:
        link_elem = elem.find_element(By.CSS_SELECTOR, 'a')
        location_elem = elem.find_element(By.CSS_SELECTOR, 'p[class*="body--metadata"]')
        job_url = link_elem.get_attribute('href')
        location = location_elem.text
        job_name = link_elem.find_element(By.CSS_SELECTOR, 'p[class*="body--medium"]').text
        job = {
            "company": company,
            "title": job_name,
            "location": clean_location(location),
            "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
        }
        result.append(job)
    return result


class ScrapeGreenhouse(ScrapeIt):
    name = 'GREENHOUSE'

    def has_next_page(self, driver):
        next_page = driver.find_elements(By.XPATH, '//button[@aria-label="Next page" and @aria-disabled="false"]')
        if len(next_page) > 0:
            print(f'[{self.name}] Next page found, click and scrape more jobs...')
            driver.execute_script("arguments[0].click();", next_page[0])
            time.sleep(3)
        return len(next_page) > 0

    def getJobs(self, driver, web_page, company) -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.implicitly_wait(5)
        driver.get(web_page)
        if company == 'bitcoin':
            time.sleep(5)
        iframe = driver.find_elements(By.TAG_NAME, 'iframe')
        if len(iframe) > 0:
            print(f'[{self.name}] iFrame detected..')
            time.sleep(3)
            driver.switch_to.frame(iframe[0])
            time.sleep(5)
        result = get_jobs(driver, company)
        while self.has_next_page(driver):
            result += get_jobs(driver, company)
        print(f'[{self.name}] Scraped {len(result)} jobs from {web_page}')
        return result
