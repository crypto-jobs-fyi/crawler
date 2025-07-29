from selenium.webdriver.common.by import By
from selenium import webdriver
from src.scrape_it import ScrapeIt

CSS_SELECTOR = "css"  # for ChromeDriver


def clean_location(location):
    locations = list(filter(None, ([x.strip() for x in location.split('•')])))
    result = locations[1]
    return result.strip().replace('United States', 'US').replace('United Kingdom', 'UK').replace('United Arab Emirates', 'UAE')


class ScrapeAshbyhq(ScrapeIt):
    name = 'ashbyhq'

    def getJobs(self, driver: webdriver.Chrome, web_page: str, company: str) -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        driver.implicitly_wait(7)
        group_elements = driver.find_elements(By.CSS_SELECTOR, 'a[class*="container_"]')
        job_location_locator = 'div p'
        result = []
        for elem in group_elements:
            link_elem = elem
            job_name_elem = elem.find_element(By.CSS_SELECTOR, 'h3')
            location_elem = elem.find_element(By.CSS_SELECTOR, job_location_locator)
            job_url = link_elem.get_attribute('href')
            job_name = job_name_elem.text
            location = location_elem.text
            cleaned_location = location.replace('\n', ', ')
            job = {
                "company": company,
                "title": job_name,
                "location": clean_location(cleaned_location),
                "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
