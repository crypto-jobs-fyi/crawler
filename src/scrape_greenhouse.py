from src.playwright_adapter import By
from src.scrape_it import ScrapeIt
import time
from src.logging_utils import get_logger

module_logger = get_logger(__name__)


def clean_location(location):
    location = location.replace('United States', 'US').replace('United Kingdom', 'UK').replace('United Arab Emirates', 'UAE').replace('Tel Aviv-Yafo, Tel Aviv District', 'Tel Aviv').replace('Hong Kong, Hong Kong SAR', 'Hong Kong')
    return location.strip().strip('-')

def get_jobs(page, company):
    group_elements = page.find_elements(By.CSS_SELECTOR, 'div [class="job-post"]')
    result = []
    module_logger.info(
        "Greenhouse jobs found",
        extra={"company": company, "jobs_found": len(group_elements)},
    )
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
            "link": job_url
        }
        result.append(job)
    return result


class ScrapeGreenhouse(ScrapeIt):
    name = 'GREENHOUSE'

    def has_next_page(self, page):
        next_page = page.find_elements(By.XPATH, '//button[@aria-label="Next page" and @aria-disabled="false"]')
        if len(next_page) > 0:
            self.log_info(
                "Pagination next",
                company=self.name,
            )
            page.execute_script("arguments[0].click();", next_page[0])
            time.sleep(3)
        return len(next_page) > 0

    def getJobs(self, page, web_page, company: str) -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        page.implicitly_wait(5)
        page.get(web_page)
        if company.lower() in ['bitcoin', 'okx']:
            time.sleep(5)
        iframe = page.find_elements(By.TAG_NAME, 'iframe')
        if len(iframe) > 0:
            self.log_info(
                "Iframe detected",
                company=company,
                web_page=web_page,
            )
            time.sleep(3)
            page.switch_to.frame(iframe[0])
            time.sleep(5)
        result = get_jobs(page, company)
        while self.has_next_page(page):
            result += get_jobs(page, company)
        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_scraped=len(result),
        )
        return result
