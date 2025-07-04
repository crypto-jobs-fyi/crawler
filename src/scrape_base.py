from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


class ScrapeBase(ScrapeIt):
    name = 'Base'

    def getJobs(self, driver, web_page, company) -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.implicitly_wait(15)
        driver.get(web_page)
        # use reverse strategy from a link to a title
        group_elements = driver.find_elements(By.CSS_SELECTOR, '[class*="font-display"] [class*="justify-between"]')
        result = []
        for elem in group_elements:
            job_name_elem = elem.find_element(By.CSS_SELECTOR, 'div a[rel]')
            job_name = job_name_elem.text
            location_elem = elem.find_element(By.CSS_SELECTOR, 'div>p[class="text-sm"]')
            job_url = job_name_elem.get_attribute('href')
            location = location_elem.text
            job = {
                "company": company,
                "title": job_name,
                "location": location,
                "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
