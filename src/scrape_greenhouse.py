from src.playwright_adapter import By, PlaywrightWait
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
    _next_page_selector = '//button[@aria-label="Next page" and @aria-disabled="false"]'
    _max_pages = 25

    @staticmethod
    def _page_signature(page):
        return page.execute_script(
            """
            return Array.from(document.querySelectorAll('div [class="job-post"]'))
              .map((card) => card.querySelector('a')?.href || '')
              .filter(Boolean)
              .join('|');
            """
        )

    def has_next_page(self, page, company=None):
        next_page = page.find_elements(By.XPATH, self._next_page_selector)
        if not next_page:
            return False

        previous_signature = self._page_signature(page)
        self.log_info("Pagination next", company=company or self.name)
        page.execute_script("arguments[0].click();", next_page[0])
        try:
            PlaywrightWait(page, 20).until(
                lambda current_page: (
                    (signature := self._page_signature(current_page))
                    and signature != previous_signature
                )
            )
        except TimeoutError:
            self.log_warning(
                "Pagination did not load a new Greenhouse job page",
                company=company or self.name,
            )
            return False
        return True

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
        result = []
        pages_scraped = 0
        while pages_scraped < self._max_pages:
            result += get_jobs(page, company)
            pages_scraped += 1
            if pages_scraped == self._max_pages:
                if page.find_elements(By.XPATH, self._next_page_selector):
                    self.log_warning(
                        "Greenhouse page limit reached; more jobs may be available",
                        company=company,
                        web_page=web_page,
                        pages_scraped=pages_scraped,
                    )
                break
            if not self.has_next_page(page, company):
                break
        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_scraped=len(result),
            pages_scraped=pages_scraped,
        )
        return result
