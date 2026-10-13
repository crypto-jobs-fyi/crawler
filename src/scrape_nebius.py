import time
from src.playwright_adapter import By
from src.scrape_it import ScrapeIt
from src.logging_utils import get_logger

module_logger = get_logger(__name__)


def to_records(page, company) -> list:
    group_elements = page.find_elements(By.CSS_SELECTOR, 'a[class*="JobsBlock_jobLink"]')
    result = []
    module_logger.info(
        "Nebius jobs found",
        extra={"company": company, "jobs_found": len(group_elements)},
    )
    for elem in group_elements:
        job_url = elem.get_attribute('href')
        title_elem = elem.find_element(By.CSS_SELECTOR, 'span[class*="header"]')
        location_elem = elem.find_element(By.CSS_SELECTOR, '[class*="jobInfo"] div:not([class*="jobDepartment"])>span')
        location = location_elem.text.strip().replace('United States', 'US').replace('United Kingdom', 'UK').replace('United Arab Emirates', 'UAE')
        job = {
            "company": company,
            "title": title_elem.text,
            "location": location,
            "link": job_url
        }
        result.append(job)
    return result


class ScrapeNebius(ScrapeIt):
    name = 'NEBIUS'

    def getJobs(self, page, web_page, company='nebius') -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        page.implicitly_wait(5)
        page.get(web_page)
        time.sleep(3)
        accept_cookies = page.find_elements(By.XPATH, '//button[.="Required only"]')
        for button in accept_cookies:
            button.click()
        result = to_records(page, company)
        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_scraped=len(result),
        )
        return result
