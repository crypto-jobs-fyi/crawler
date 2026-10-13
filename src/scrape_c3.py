from src.playwright_adapter import By
from src.scrape_it import ScrapeIt
from src.logging_utils import get_logger

module_logger = get_logger(__name__)


def to_records(page, company) -> list:
    group_elements = page.find_elements(By.CSS_SELECTOR, 'a[href*="/job-"]')
    result = []
    module_logger.info(
        "C3 jobs found",
        extra={"company": company, "jobs_found": len(group_elements)},
    )
    for elem in group_elements:
        job_url = elem.get_attribute('href')
        title = elem.find_element(By.CSS_SELECTOR, 'h4').text
        location = elem.find_element(By.CSS_SELECTOR, 'h5').text
        if title != '':
            job = {
            "company": company,
            "title": title,
            "location": location,
            "link": job_url
            }
            result.append(job)
    return result


class ScrapeC3(ScrapeIt):
    name = 'c3.ai'

    def getJobs(self, page, web_page, company='c3.ai') -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        page.implicitly_wait(5)
        page.get(web_page)
        button = page.find_element(
            By.XPATH,
            '//button[@type="button" and normalize-space()="View all"]',
        )
        page.execute_script("arguments[0].click();", button)
        result = to_records(page, company)
        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_scraped=len(result),
        )
        return result
