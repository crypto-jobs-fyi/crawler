from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt, write_jobs
from caqui import synchronous, asynchronous
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


class ScrapeGreenhouse(ScrapeIt):
    name = 'GREENHOUSE'

    def getJobs(self, driver, web_page, company) -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        iframe = driver.find_elements(By.TAG_NAME, 'iframe')
        if len(iframe) > 0:
            print(f'[{self.name}] iFrame detected..')
            time.sleep(3)
            driver.switch_to.frame(iframe[0])
            time.sleep(5)
        group_elements = driver.find_elements(By.CSS_SELECTOR, 'div [class="opening"]')
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
        print(f'[{self.name}] Found {len(group_elements)} jobs, Scraped {len(result)} jobs from {web_page}')
        write_jobs(result)
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
        write_jobs(result)
        return result
