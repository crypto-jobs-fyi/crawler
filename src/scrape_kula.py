from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt
import time

def clean_location(location):
    location = location.replace('United States', 'US').replace('United Kingdom', 'UK').replace('Singapore, Singapore', 'Singapore').replace('New York, New York', 'New York')
    return location.strip()


class ScrapeKula(ScrapeIt):
    name = 'Kula'

    def getJobs(self, driver, web_page, company) -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.implicitly_wait(5)
        driver.get(web_page)
        time.sleep(3)
        # use reverse strategy from a link to a title
        group_elements = driver.find_elements(By.CSS_SELECTOR, 'div[class*="chakra-card"]')
        result = []
        for elem in group_elements:
            job_name_elems = elem.find_elements(By.CSS_SELECTOR, 'div[class*="chakra-stack"] p[class*="chakra-text"]')
            job_name = job_name_elems[0].text if job_name_elems else "Unknown"
            job_url_elem = elem.find_element(By.CSS_SELECTOR, 'a[class*="chakra-link"]')
            job_url = job_url_elem.get_attribute('href')
            location = job_name_elems[1].text if job_name_elems else "Unknown"
            job = {
                "company": company,
                "title": job_name,
                "location": clean_location(location),
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
