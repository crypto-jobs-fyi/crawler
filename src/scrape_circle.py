import time
from src.playwright_adapter import By
from src.scrape_it import ScrapeIt
from src.logging_utils import get_logger

module_logger = get_logger(__name__)


_LOCATION_MAP = {
    "United States of America": "US",
    "United Kingdom": "UK",
}


def shorten_location(location: str) -> str:
    for full, short in _LOCATION_MAP.items():
        if full in location:
            return short
    return location


def to_records(page, company) -> list:
    group_elements = page.find_elements(By.XPATH, '//div[@data-ph-at-id="jobs-list"]')
    result = []
    module_logger.info(
        "Circle jobs found",
        extra={"company": company, "jobs_found": len(group_elements)},
    )
    for elem in group_elements:
        job_elem = elem.find_element(By.XPATH, './/a[@data-ph-at-id="job-link"]')
        job_url = job_elem.get_attribute('href')
        location = shorten_location(elem.find_element(By.XPATH, './/div[@data-ph-at-id="job-country"]').text)
        job = {
            "company": company,
            "title": job_elem.text,
            "location": location,
            "link": job_url
        }
        result.append(job)
    return result


class ScrapeCircle(ScrapeIt):
    name = 'CIRCLE'
    def has_next_page(self, page):
        next_page = page.find_element(By.XPATH, '//a[@aria-label="Next"]')
        is_displayed = next_page.is_displayed()
        if is_displayed:
            self.log_info(
                "Pagination next",
                company=self.name,
            )
            page.execute_script("arguments[0].click();", next_page)
            time.sleep(3)
        return is_displayed

    def getJobs(self, page, web_page, company='circle') -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        page.implicitly_wait(5)
        page.get(web_page)
        time.sleep(3)
        accept_cookies = page.find_elements(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
        if len(accept_cookies) > 0:
            self.log_info(
                "Accept cookies",
                company=company,
                web_page=web_page,
            )
            accept_cookies[0].click()
        result = to_records(page, company)
        while self.has_next_page(page):
            result += to_records(page, company)
        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_scraped=len(result),
        )
        return result
