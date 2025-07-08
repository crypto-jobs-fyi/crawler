from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt
from caqui import asynchronous
import time
CSS_SELECTOR = "css"  # for ChromeDriver


def clean_location(location):
    locations = set(filter(None, ([x.strip() for x in location.split(',')])))
    if len(locations) == 1:
        return next(iter(locations))
    joined = ' '.join(locations).lower()
    if joined.count('remote') > 1:
        return joined.replace('remote', '', 1).title()
    return joined.strip().strip('-').title()

def get_jobs(driver, company):
    group_elements = driver.find_elements(By.CSS_SELECTOR, 'div [class="job-post"]')
    result = []
    print(f'[GREENHOUSE] Found {len(group_elements)} jobs. Scraping jobs...')
    for elem in group_elements:
        link_elem = elem.find_element(By.CSS_SELECTOR, 'a')
        location_elem = elem.find_element(By.CSS_SELECTOR, 'p[class*="body--metadata"]')
        job_url = link_elem.get_attribute('href')
        location = location_elem.text
        job_name = link_elem.text
        job = {
            "company": company,
            "title": job_name,
            "location": clean_location(location),
            "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
        }
        result.append(job)
    return result

class ScrapeGreenhouse(ScrapeIt):
    name = 'GREENHOUSE'

    def has_next_page(self, driver):
        next_page = driver.find_elements(By.XPATH, '//button[@aria-label="Next page" and @aria-disabled="false"]')
        if len(next_page) > 0:
            print(f'[{self.name}] Next page found, click and scrape more jobs...')
            driver.execute_script("arguments[0].click();", next_page[0])
            time.sleep(2)
        return len(next_page) > 0

    def getJobs(self, driver, web_page, company) -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        if company == 'bitcoin':
            time.sleep(5)
        iframe = driver.find_elements(By.TAG_NAME, 'iframe')
        if len(iframe) > 0:
            print(f'[{self.name}] iFrame detected..')
            time.sleep(3)
            driver.switch_to.frame(iframe[0])
            time.sleep(5)
        result = get_jobs(driver, company)
        while self.has_next_page(driver):
            result += get_jobs(driver, company)
        print(f'[{self.name}] Scraped {len(result)} jobs from {web_page}')
        return result


class ScrapeGreenhouseAsync(ScrapeIt):
    name = 'GREENHOUSE'

    async def getJobs(self, driver, web_page, company) -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
        await asynchronous.go_to_page(*driver, web_page)
        await asynchronous.set_timeouts(*driver, 5000)
        iframe = await asynchronous.find_elements(*driver, By.TAG_NAME, 'iframe')
        if len(iframe) > 0:
            print(f'[{self.name}] iFrame detected..')
            time.sleep(3)
            await asynchronous.switch_to_frame(*driver, iframe[0])
            time.sleep(5)
        group_elements = await asynchronous.find_elements(*driver, CSS_SELECTOR, 'div [class="opening"]')
        result = []
        for elem in group_elements:
            link_elem = await asynchronous.find_child_element(*driver, elem, CSS_SELECTOR, 'a')
            location_elem = await asynchronous.find_child_element(*driver, elem, CSS_SELECTOR, 'span')
            job_url = await asynchronous.get_attribute(*driver, link_elem, "href")
            job_name = await asynchronous.get_text(*driver, link_elem)
            location = await asynchronous.get_text(*driver, location_elem)
            cleaned_location = location.replace('\n', ', ')
            job = {
                "company": company,
                "title": job_name,
                "location": clean_location(cleaned_location),
                "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
            }
            result.append(job)
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        return result
