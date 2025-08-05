from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


def to_records(driver, company) -> []:
    group_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-dept_id] > a[href*="c3"]')
    result = []
    print(f'[{company}] Found {len(group_elements)} jobs. Scraping jobs...')
    for elem in group_elements:
        job_url = elem.get_attribute('href')
        title = elem.find_element(By.CSS_SELECTOR, 'h4[class="title"]').text
        job = {
            "company": company,
            "title": title,
            "location": elem.find_element(By.CSS_SELECTOR, 'h6[class="location"]').text,
            "link": job_url
        }
        result.append(job)
    return result


class ScrapeC3(ScrapeIt):
    name = 'c3.ai'

    def getJobs(self, driver, web_page, company='c3.ai') -> list:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.implicitly_wait(5)
        driver.get(web_page)
        button = driver.find_element(By.XPATH, '//div[@id="jobBtnHolder"]/button')
        driver.execute_script("arguments[0].click();", button)
        result = to_records(driver, company)
        print(f'[{self.name}] Scraped {len(result)} jobs from {web_page}')
        return result
