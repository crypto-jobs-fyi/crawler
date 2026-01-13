import time
from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt
from src.logging_utils import get_logger

module_logger = get_logger(__name__)


def to_records(driver, company) -> list:
    group_elements = driver.find_elements(By.CSS_SELECTOR, 'h3 a[href]')
    result = []
    module_logger.info(
        "Circle jobs found",
        extra={"company": company, "jobs_found": len(group_elements)},
    )
    for elem in group_elements:
        job_url = elem.get_attribute('href')
        job = {
            "company": company,
            "title": elem.text,
            "location": 'US',
            "link": job_url
        }
        result.append(job)
    return result


class ScrapeCircle(ScrapeIt):
    name = 'CIRCLE'
    def has_next_page(self, driver):
        next_page = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')
        is_displayed = next_page.is_displayed()
        if is_displayed:
            self.log_info(
                "Pagination next",
                company=self.name,
            )
            driver.execute_script("arguments[0].click();", next_page)
            time.sleep(3)
        return is_displayed

    def getJobs(self, driver, web_page, company='circle') -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.implicitly_wait(5)
        driver.get(web_page)
        time.sleep(3)
        accept_cookies = driver.find_elements(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
        if len(accept_cookies) > 0:
            self.log_info(
                "Accept cookies",
                company=company,
                web_page=web_page,
            )
            accept_cookies[0].click()
        result = to_records(driver, company)
        while self.has_next_page(driver):
            result += to_records(driver, company)
        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_scraped=len(result),
        )
        return result
