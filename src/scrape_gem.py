import time
from src.playwright_adapter import By
from src.scrape_it import ScrapeIt


class ScrapeGem(ScrapeIt):
    name = 'GEM'

    def clean_location(self, location: str) -> str:
        return location.strip().replace('United States', 'US').replace('United Kingdom', 'UK').replace('United Arab Emirates', 'UAE').replace('\n', ' ')


    def getJobs(self, page, web_page, company) -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        page.implicitly_wait(9)
        page.get(web_page)
        time.sleep(5)
        group_elements = page.find_elements(By.CSS_SELECTOR, 'a[class*=jobPostingLink]')
        result = []
        for elem in group_elements:
            job_name_elem = elem.find_element(By.CSS_SELECTOR, 'div[class*=jobTitle]')
            job_name: str = job_name_elem.text
            location = elem.find_element(By.CSS_SELECTOR, 'div[class*=jobAttributes]')
            location_text: str = self.clean_location(location.text)
            job_url = elem.get_attribute('href')
            job = {
                "company": company,
                "title": job_name,
                "location": location_text,
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
