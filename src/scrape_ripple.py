from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt, write_jobs


class ScrapeRipple(ScrapeIt):
    name = 'RIPPLE'

    def getJobs(self, driver, web_page, company='ripple') -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        # use reverse strategy from a link to a title
        group_elements = driver.find_elements(By.XPATH, '//div/a[contains(@class, "body3")]')
        print(f'[{self.name}] Found {len(group_elements)} jobs on {web_page}')
        result = []
        for elem in group_elements:
            link_elem = elem
            job_name_elem = elem.find_element(By.XPATH, './../../../div[contains(@class, "heading3")]')
            location_elem = elem
            job_url = link_elem.get_attribute('href')
            job_name = job_name_elem.text
            location = location_elem.text
            job = {
                "company": company,
                "title": job_name,
                "location": location,
                "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
            }
            result.append(job)
        print(f'[{self.name}] Scraped {len(result)} jobs from {web_page}')
        write_jobs(result)
        return result
