from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


class ScrapeHelsing(ScrapeIt):
    name = 'Helsing'

    def getJobs(self, driver, web_page, company) -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.implicitly_wait(15)
        driver.get(web_page)
        group_elements = driver.find_elements(By.XPATH, '//div[@data-label="Position"]/..')
        result = []
        for elem in group_elements:
            title_elem = elem.find_element(By.XPATH, './/div[@data-label="Position"]')
            location_elem = elem.find_element(By.XPATH, './/div[@data-label="Location"]')
            job_name = (title_elem.get_attribute('textContent') or '').strip()
            location = (location_elem.get_attribute('textContent') or '').strip()
            if not job_name:
                continue
            job_url = elem.get_attribute('href')
            job = {
                "company": company,
                "title": job_name,
                "location": location,
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
