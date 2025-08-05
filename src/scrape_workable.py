import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from src.scrape_it import ScrapeIt


def show_more(driver, locator: str) -> None:
    print(f'[workable] Show more jobs..')
    show_more_button: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, locator)
    if len(show_more_button) > 0:
        driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button[0])
        time.sleep(5)
        driver.execute_script("arguments[0].click();", show_more_button[0])
        time.sleep(5)
        show_more(driver, locator)


def clean_location(location: str) -> str:
    return ' '.join(set(([x.strip() for x in location.split(',')])))


class ScrapeWorkable(ScrapeIt):
    name = 'workable'.upper()

    def getJobs(self, driver, web_page, company) -> list:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        clear_filters_locator: str = 'a[data-ui="clear-filters"]'
        driver.implicitly_wait(5)
        clear_filters: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, clear_filters_locator)
        if len(clear_filters) > 0:
            print(f'[{self.name}] Clear filters')
            driver.execute_script("arguments[0].click();", clear_filters[0])
        driver.implicitly_wait(15)
        wait: WebDriverWait = WebDriverWait(driver, 10)
        result: list = []
        show_more_locator: str = 'button[data-ui="load-more-button"]'
        job_root_locator: str = 'li[data-ui^="job"]'
        show_more_buttons: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, show_more_locator)
        if len(show_more_buttons) > 0:
            print(f'[{self.name}] Show more Jobs button found..')
            show_more(driver, show_more_locator)
        # just try to find elements and exit if none
        temp_elements: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, job_root_locator)
        if len(temp_elements) == 0:
            print(f'[{self.name}] Found 0 jobs on {web_page}')
            return result
        group_elements: list[WebElement] = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, job_root_locator)))
        driver.implicitly_wait(5)
        for elem in group_elements:
            link_elem: WebElement = elem.find_element(By.CSS_SELECTOR, 'a')
            remote_elem: list[WebElement] = elem.find_elements(By.CSS_SELECTOR, '[data-ui="job-remote"]')
            job_name_elem: WebElement = elem.find_element(By.CSS_SELECTOR, '[data-ui="job-title"],[data-id="job-item"]')
            location_elem: WebElement = elem.find_element(By.CSS_SELECTOR, 'span[data-ui="job-location"],span[data-ui="job-workplace"]')
            job_url: str = link_elem.get_attribute('href')
            job_name: str = job_name_elem.text
            location: str = location_elem.text
            if len(remote_elem) > 0:
                location = location + ' REMOTE'
            job: dict = {
                "company": company,
                "title": job_name,
                "location": clean_location(location),
                "link": job_url
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
