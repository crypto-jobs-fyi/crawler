from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from src.scrape_it import ScrapeIt


def clean_location(location: str) -> str:
    locations: list[str] = list(filter(None, ([x.strip() for x in location.split('•')])))
    result: str = locations[1]
    return result.strip().replace('United States', 'US').replace('United Kingdom', 'UK').replace('United Arab Emirates', 'UAE')


class ScrapeAshbyhq(ScrapeIt):
    name = 'ashbyhq'.upper()

    def getJobs(self, driver: webdriver.Chrome, web_page: str, company: str) -> list:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        driver.implicitly_wait(7)
        group_elements: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, 'a[class*="container_"]')
        job_location_locator: str = 'div p'
        result: list = []
        for elem in group_elements:
            link_elem: WebElement = elem
            job_name_elem: WebElement = elem.find_element(By.CSS_SELECTOR, 'h3')
            location_elem: WebElement = elem.find_element(By.CSS_SELECTOR, job_location_locator)
            job_url: str = link_elem.get_attribute('href')
            job_name: str = job_name_elem.text
            location: str = location_elem.text
            cleaned_location: str = location.replace('\n', ', ')
            job: dict = {
                "company": company,
                "title": job_name,
                "location": clean_location(cleaned_location),
                "link": job_url
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
