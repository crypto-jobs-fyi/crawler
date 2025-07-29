import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from src.scrape_it import ScrapeIt


def clean_location(location):
    locations = set(filter(None, ([x.strip() for x in location.split(',')])))
    if len(locations) == 1:
        return next(iter(locations)).strip().lstrip('-').title()
    joined = ' '.join(locations).lower()
    if joined.count('remote') > 1:
        return joined.replace('remote', '', 1).strip().lstrip('-').title()
    return joined.replace('\u2014', '').strip().lstrip('-').title()


class ScrapeLever(ScrapeIt):
    name = 'LEVER'

    def getJobs(self, driver, web_page, company) -> list:
        print(f'[{self.name}] Scrap page: {web_page}')
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
                "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
