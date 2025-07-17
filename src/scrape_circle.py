import time
from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


def to_records(driver, company) -> []:
    group_elements = driver.find_elements(By.CSS_SELECTOR, 'h3 a[href]')
    result = []
    print(f'[CIRCLE] Found {len(group_elements)} jobs. Scraping jobs...')
    for elem in group_elements:
        job_url = elem.get_attribute('href')
        job = {
            "company": company,
            "title": elem.text,
            "location": 'US',
            "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
        }
        result.append(job)
    return result


class ScrapeCircle(ScrapeIt):
    name = 'CIRCLE'
    def has_next_page(self, driver):
        next_page = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')
        is_displayed = next_page.is_displayed()
        if is_displayed:
            print(f'[{self.name}] Next page found, click and scrape more jobs...')
            driver.execute_script("arguments[0].click();", next_page)
            time.sleep(3)
        return is_displayed

    def getJobs(self, driver, web_page, company='circle') -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.implicitly_wait(5)
        driver.get(web_page)
        time.sleep(3)
        accept_cookies = driver.find_elements(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
        if len(accept_cookies) > 0:
            print(f'[{self.name}] Accepting cookies...')
            accept_cookies[0].click()
        # close_chat = driver.find_element(By.XPATH, '//button[@id="PhenomChatbotNotificationCloseButton"]')
        # close_chat.click()
        # //h3/a[@data-ph-at-id="job-link" and contains(@href, "circle")]
        result = to_records(driver, company)
        while self.has_next_page(driver):
            result += to_records(driver, company)

        print(f'[{self.name}] Scraped {len(result)} jobs from {web_page}')
        return result
