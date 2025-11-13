from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


class ScrapeAvara(ScrapeIt):
    name = 'Avara'

    def getJobs(self, driver, web_page, company = 'avara') -> list:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.implicitly_wait(5)
        driver.get(web_page)
        # use reverse strategy from a link to a title
        group_elements = driver.find_elements(By.XPATH, '//li/a[contains(@href, "careers")]')
        result = []
        for elem in group_elements:
            job_name_elem = elem.find_element(By.XPATH, './/h3')
            job_name = job_name_elem.text
            job_url = elem.get_attribute('href')
            location = 'London or EU - Remote'
            job = {
                "company": company,
                "title": job_name,
                "location": location,
                "link": job_url
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
