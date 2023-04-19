from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt, write_jobs
import time


def clean_location(location):
    locations = set(filter(None, ([x.strip() for x in location.split(',')])))
    if len(locations) == 1:
        return next(iter(locations))
    joined = ' '.join(locations).lower()
    if joined.count('remote') > 1:
        return joined.replace('remote', '', 1).title()
    return joined.strip().strip('-').title()


class ScrapeGreenhouse(ScrapeIt):
    name = 'GREENHOUSE'

    def getJobs(self, driver, web_page, company) -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        iframe = driver.find_elements(By.TAG_NAME, 'iframe')
        if len(iframe) > 0:
            print(f'[{self.name}] iFrame detected..')
            time.sleep(2)
            driver.switch_to.frame(iframe[0])
            time.sleep(2)
        group_elements = driver.find_elements(By.CSS_SELECTOR, 'div [class="opening"]')
        print(f'[{self.name}] Found {len(group_elements)} jobs.')
        result = []
        for elem in group_elements:
            link_elem = elem.find_element(By.CSS_SELECTOR, 'a')
            location_elem = elem.find_element(By.CSS_SELECTOR, 'span')
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
        print(f'[{self.name}] Scraped {len(result)} jobs from {web_page}')
        write_jobs(result)
        return result
