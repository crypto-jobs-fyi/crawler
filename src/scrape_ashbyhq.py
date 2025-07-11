from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt
from caqui import synchronous, asynchronous

CSS_SELECTOR = "css"  # for ChromeDriver


def clean_location(location):
    locations = list(filter(None, ([x.strip() for x in location.split('•')])))
    result = locations[1]
    return result.strip().replace('United States', 'US').replace('United Kingdom', 'UK').replace('Canada', 'CA').replace('Australia', 'AU').replace('Germany', 'DE').replace('France', 'FR').replace('Spain', 'ES').replace('Netherlands', 'NL').replace('Sweden', 'SE')


class ScrapeAshbyhqAsync(ScrapeIt):
    name = 'ashbyhq'

    async def getJobs(self, driver, web_page, company) -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
        # driver.get(web_page)
        await asynchronous.go_to_page(*driver, web_page)
        # driver.implicitly_wait(5)
        await asynchronous.set_timeouts(*driver, 5000)
        # group_elements = driver.find_elements(By.CSS_SELECTOR, 'a[class*="container_"]')
        group_elements = await asynchronous.find_elements(*driver, CSS_SELECTOR, 'a[class*="container_"]')
        job_location_locator = 'div p'
        result = []
        for elem in group_elements:
            link_elem = elem
            # job_name_elem = elem.find_element(By.CSS_SELECTOR, 'h3')
            job_name_elem = await asynchronous.find_child_element(*driver, elem, CSS_SELECTOR, "h3")
            # location_elem = elem.find_element(By.CSS_SELECTOR, job_location_locator)
            location_elem = await asynchronous.find_child_element(*driver, elem, CSS_SELECTOR, job_location_locator)
            # job_url = link_elem.get_attribute('href')
            job_url = await asynchronous.get_attribute(*driver, link_elem, "href")
            # job_name = job_name_elem.text
            job_name = await asynchronous.get_text(*driver, job_name_elem)
            # location = location_elem.text
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


class ScrapeAshbyhq(ScrapeIt):
    name = 'ashbyhq'

    def getJobs(self, driver, web_page, company) -> []:
        print(f'[{self.name}] Scrap page: {web_page}')
        driver.get(web_page)
        driver.implicitly_wait(7)
        group_elements = driver.find_elements(By.CSS_SELECTOR, 'a[class*="container_"]')
        job_location_locator = 'div p'
        result = []
        for elem in group_elements:
            link_elem = elem
            job_name_elem = elem.find_element(By.CSS_SELECTOR, 'h3')
            location_elem = elem.find_element(By.CSS_SELECTOR, job_location_locator)
            job_url = link_elem.get_attribute('href')
            job_name = job_name_elem.text
            location = location_elem.text
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
