from src.playwright_adapter import By
from src.scrape_it import ScrapeIt
import time


class ScrapeAvara(ScrapeIt):
    name = 'Avara'

    def getJobs(self, page, web_page, company = 'avara') -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        page.implicitly_wait(9)
        page.get(web_page)
        time.sleep(3)
        cookie_buttons = page.find_elements(By.XPATH, '//button[.="Accept All"]')
        if cookie_buttons:
            cookie_buttons[0].click()
            time.sleep(1)
        # use reverse strategy from a link to a title
        group_elements = page.find_elements(By.XPATH, '//li/a[contains(@href, "/careers/")]')
        result = []
        for elem in group_elements:
            job_name_elem = elem.find_element(By.XPATH, './div')
            job_name = job_name_elem.text
            job_url = elem.get_attribute('href')
            location = 'Remote or Hybrid'
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
