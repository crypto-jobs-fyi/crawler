from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


class ScrapeBase(ScrapeIt):
    name = 'Base'

    def getJobs(self, driver, web_page, company = 'base') -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
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
                "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
