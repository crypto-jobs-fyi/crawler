from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


def to_records(group_elements, company) -> list:
    result = []
    for elem in group_elements:
        job_url = elem.get_attribute('href')
        job = {
            "company": company,
            "title": elem.find_element(By.CSS_SELECTOR, 'div[class="job-list-item"] h4').text,
            "location": elem.find_element(By.CSS_SELECTOR, 'div[class="job-list-item"] p').text,
            "link": job_url
        }
        result.append(job)
    return result


class ScrapePaxos(ScrapeIt):
    name = 'PAXOS'

    def getJobs(self, driver, web_page, company='paxos') -> list:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.implicitly_wait(5)
        driver.get(web_page)
        group_elements = driver.find_elements(By.CSS_SELECTOR, '[class="job-listings"] a[href]')
        result = to_records(group_elements, company)
        print(f'[{self.name}] Scraped {len(result)} jobs from {web_page}')
        return result
