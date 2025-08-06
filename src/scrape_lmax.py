from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


class ScrapeLmax(ScrapeIt):
    name = 'LMAX'

    @staticmethod
    def clean_location(loc: str) -> str:
        loc = loc.replace('United States', 'US').replace('United Kingdom', 'UK').replace('United Arab Emirates', 'UAE')
        return loc.strip()

    def getJobs(self, driver, web_page, company='lmax') -> list:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        # use reverse strategy from a link to a title
        group_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-dept]')
        result = []
        for elem in group_elements:
            job_name_elem = elem.find_element(By.CSS_SELECTOR, 'div[class="JobTitle"] a')
            location_elem = elem.find_element(By.CSS_SELECTOR, 'div[class="Location"]')
            job_url = job_name_elem.get_attribute('href')
            job_name = job_name_elem.text
            location: str = self.clean_location(location_elem.text)
            job = {
                "company": company,
                "title": job_name,
                "location": location,
                "link": job_url
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
