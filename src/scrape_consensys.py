import time

from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt, write_jobs


class ScrapeConsensys(ScrapeIt):
    name = 'CONSENSYS'

    def getJobs(self, driver, web_page, company='consensys') -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        driver.implicitly_wait(10)
        time.sleep(5)
        group_elements = driver.find_elements(By.XPATH, '//a[contains(@class, "card-job")]')
        result = []
        for elem in group_elements:
            link_elem = elem
            job_name_elem = elem.find_element(By.CSS_SELECTOR, 'h5')
            job_url = link_elem.get_attribute('href')
            job_name = job_name_elem.text
            job = {
                "company": company,
                "title": job_name,
                "location": 'USA - Remote',
                "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        write_jobs(result)
        return result
