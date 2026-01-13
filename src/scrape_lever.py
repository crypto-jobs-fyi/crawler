import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from src.scrape_it import ScrapeIt


def clean_location(location):
    location: str = location.strip().strip('-').replace('United States', 'US').replace('United Kingdom', 'UK').replace('United Arab Emirates', 'UAE').replace('HONG KONG, HONG KONG SAR', 'Hong Kong').replace('UNITED KINGDOM', 'UK').replace('UNITED STATES', 'US').replace('UNITED ARAB EMIRATES', 'UAE')
    return location.replace('\u2014', '').strip().strip(',')


class ScrapeLever(ScrapeIt):
    name = 'LEVER'

    def getJobs(self, driver, web_page, company) -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.implicitly_wait(7)
        driver.get(web_page)
        if company in ['binance', 'crypto']:
            time.sleep(5)
        group_elements: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, 'a[class="posting-title"]')
        result: list = []
        for elem in group_elements:
            link_elem: WebElement = elem.find_element(By.CSS_SELECTOR, '[data-qa="posting-name"]')
            location_elem: list[WebElement] = elem.find_elements(By.CSS_SELECTOR, '[class*="location"]')
            workplace_elem: list[WebElement] = elem.find_elements(By.CSS_SELECTOR, '[class*="workplaceTypes"]')
            job_url: str = elem.get_attribute('href')
            if len(location_elem) > 0:
                location: str = location_elem[0].text
            else:
                location: str = ''
            if len(workplace_elem) > 0:
                workplace: str = workplace_elem[0].text
                merge_location: str = f'{location},{workplace}'
            else:
                merge_location: str = location
            job = {
                "company": company,
                "title": link_elem.text,
                "location": clean_location(merge_location),
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
