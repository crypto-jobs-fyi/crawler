from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


class ScrapeWorkday(ScrapeIt):
    name = 'Workday'

    def getJobs(self, driver, web_page, company) -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
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
                "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
