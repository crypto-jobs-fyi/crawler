import time

from src.playwright_adapter import PlaywrightConditions as EC
from src.playwright_adapter import By
from src.playwright_adapter import PlaywrightWait
from src.playwright_adapter import PlaywrightElement

from src.scrape_it import ScrapeIt
from src.logging_utils import get_logger

module_logger = get_logger(__name__)


def show_more(page, locator: str) -> None:
    module_logger.info(
        "Workable show more",
        extra={"locator": locator},
    )
    show_more_button: list[PlaywrightElement] = page.find_elements(By.CSS_SELECTOR, locator)
    if len(show_more_button) > 0:
        page.execute_script("arguments[0].scrollIntoView(true);", show_more_button[0])
        time.sleep(5)
        page.execute_script("arguments[0].click();", show_more_button[0])
        time.sleep(5)
        show_more(page, locator)


def clean_location(location: str) -> str:
    return ' '.join(set(([x.strip() for x in location.split(',')])))


class ScrapeWorkable(ScrapeIt):
    name = 'workable'.upper()

    def getJobs(self, page, web_page, company) -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        page.get(web_page)
        page.implicitly_wait(5)
        time.sleep(4)
        acceptAll = page.find_elements(By.XPATH, '//*[contains(text(), "Accept")]')
        if len(acceptAll) > 0:
            acceptAll[0].click()
            time.sleep(3)
        clear_filters_locator: str = 'a[data-ui="clear-filters"]'
        clear_filters: list[PlaywrightElement] = page.find_elements(By.CSS_SELECTOR, clear_filters_locator)
        if len(clear_filters) > 0:
            self.log_info(
                "Clear filters",
                company=company,
                web_page=web_page,
            )
            page.execute_script("arguments[0].click();", clear_filters[0])
        page.implicitly_wait(15)
        wait: PlaywrightWait = PlaywrightWait(page, 10)
        result: list = []
        show_more_locator: str = 'button[data-ui="load-more-button"]'
        job_root_locator: str = 'li[data-ui^="job"]'
        show_more_buttons: list[PlaywrightElement] = page.find_elements(By.CSS_SELECTOR, show_more_locator)
        if len(show_more_buttons) > 0:
            self.log_info(
                "Show more button",
                company=company,
                web_page=web_page,
            )
            show_more(page, show_more_locator)
        # just try to find elements and exit if none
        temp_elements: list[PlaywrightElement] = page.find_elements(By.CSS_SELECTOR, job_root_locator)
        if len(temp_elements) == 0:
            self.log_info(
                "No jobs found",
                company=company,
                web_page=web_page,
            )
            return result
        group_elements: list[PlaywrightElement] = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, job_root_locator)))
        page.implicitly_wait(5)
        for elem in group_elements:
            link_elem: PlaywrightElement = elem.find_element(By.CSS_SELECTOR, 'a')
            remote_elem: list[PlaywrightElement] = elem.find_elements(By.CSS_SELECTOR, '[data-ui="job-remote"]')
            job_name_elem: PlaywrightElement = elem.find_element(By.CSS_SELECTOR, '[data-ui="job-title"],[data-id="job-item"]')
            location_elem: PlaywrightElement = elem.find_element(By.CSS_SELECTOR, 'span[data-ui="job-location"],span[data-ui="job-workplace"]')
            job_url: str = link_elem.get_attribute('href')
            job_name: str = job_name_elem.text
            location: str = location_elem.text
            if len(remote_elem) > 0:
                location = location + ' REMOTE'
            job: dict = {
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
