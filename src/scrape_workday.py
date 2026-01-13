from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


class ScrapeWorkday(ScrapeIt):
    name = 'Workday'

    def getJobs(self, driver, web_page, company) -> []:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.implicitly_wait(15)
        driver.get(web_page)
        # use reverse strategy from a link to a title
        group_elements = driver.find_elements(By.XPATH, '//a[@data-uxi-element-id]')
        result = []
        for elem in group_elements:
            job_name_elem = elem
            job_name = job_name_elem.text
            locator = f"//li//a[.='{job_name}']/../../../../..//div[@data-automation-id='locations']//dd"
            location_elem = driver.find_element(By.XPATH, locator)
            job_url = job_name_elem.get_attribute('href')
            location = location_elem.text
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
