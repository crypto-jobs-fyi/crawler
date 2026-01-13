from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


class ScrapeRipple(ScrapeIt):
    name = 'RIPPLE'

    def getJobs(self, driver, web_page, company='ripple') -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.get(web_page)
        # use reverse strategy from a link to a title
        group_elements = driver.find_elements(By.XPATH, '//div/a[contains(@class, "body3")]')
        result = []
        for elem in group_elements:
            link_elem = elem
            job_name_elem = elem.find_element(By.XPATH, './../../../div[contains(@class, "heading3")]')
            location_elem = elem
            job_url = link_elem.get_attribute('href')
            job_name = job_name_elem.text
            location_text : str = location_elem.text
            job = {
                "company": company,
                "title": job_name,
                "location": location_text.replace('United States', 'US').replace('United Kingdom', 'UK').replace('United Arab Emirates', 'UAE'),
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
