from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


class ScrapeBase(ScrapeIt):
    name = 'Base'

    def getJobs(self, driver, web_page, company = 'base') -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.implicitly_wait(5)
        driver.get(web_page)
        # use reverse strategy from a link to a title
        group_elements = driver.find_elements(By.XPATH, '//div/a[contains(@href, "basejobs")]')
        result = []
        for elem in group_elements:
            job_name_elem = elem.find_element(By.XPATH, './/h6')
            job_name = job_name_elem.text
            job_url = elem.get_attribute('href')
            location = 'US or Canada - Remote'
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
