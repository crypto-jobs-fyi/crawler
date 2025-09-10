from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


class ScrapeBitcoinSuisse(ScrapeIt):
    name = 'BitcoinSuisse'

    def getJobs(self, driver, web_page, company = 'bitcoinsuisse') -> list:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.implicitly_wait(3)
        driver.get(web_page)
        group_elements = driver.find_elements(By.CSS_SELECTOR, '[id=jobList] div[class*="row-table"]')
        result = []
        for elem in group_elements:
            job_name_elem = elem.find_element(By.CSS_SELECTOR, '[class="job-title"] a')
            job_name = job_name_elem.text
            job_url = job_name_elem.get_attribute('href')
            location = elem.find_elements(By.CSS_SELECTOR, '[class*="cell-table"] div[class="inner"]')[1].text
            job = {
                "company": company,
                "title": job_name,
                "location": location,
                "link": job_url
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
