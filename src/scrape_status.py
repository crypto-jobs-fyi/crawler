from selenium.webdriver.common.by import By

from src.scrape_it import ScrapeIt, write_jobs


class ScrapeStatus(ScrapeIt):
    name = 'status'

    def getJobs(self, driver, web_page, company='status') -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        group_elements = driver.find_elements(By.CSS_SELECTOR, 'div[class*="border"] div a[class*="items-center"]')
        result = []
        for elem in group_elements:
            job_name_elem = elem
            job_url_elem = elem
            job_url = job_url_elem.get_attribute('href')
            job_name = job_name_elem.text.split('\n')[0]
            location = 'Remote'
            job = {
                "company": company,
                "title": job_name,
                "location": location,
                "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        write_jobs(result)
        return result
