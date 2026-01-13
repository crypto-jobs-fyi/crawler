from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt
from src.logging_utils import get_logger

module_logger = get_logger(__name__)


def to_records(driver, company) -> list:
    group_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-dept_id] > a[href*="c3"]')
    result = []
    module_logger.info(
        "C3 jobs found",
        extra={"company": company, "jobs_found": len(group_elements)},
    )
    for elem in group_elements:
        job_url = elem.get_attribute('href')
        title = elem.find_element(By.CSS_SELECTOR, 'h4[class="title"]').text
        location = elem.find_element(By.CSS_SELECTOR, 'h6[class="location"]').text
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

    def getJobs(self, driver, web_page, company='c3.ai') -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.implicitly_wait(5)
        driver.get(web_page)
        button = driver.find_element(By.XPATH, '//div[@id="jobBtnHolder"]/button')
        driver.execute_script("arguments[0].click();", button)
        result = to_records(driver, company)
        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_scraped=len(result),
        )
        return result
