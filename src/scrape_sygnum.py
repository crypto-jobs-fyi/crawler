import time
from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt
# https://www.sygnum.com/careers-portal

class ScrapeSygnum(ScrapeIt):
    name = 'Sygnum'

    def tryAcceptCookies(self, driver):
        try:
            acceptCookies = driver.find_elements(By.XPATH, '//button[.="Essential only"]')
            if len(acceptCookies) > 0:
                acceptCookies[0].click()
        except Exception as e:
            self.log_error(
                "Accept cookies failed",
                error=str(e),
                exc_info=True,
            )
        return
    
    def tryAcceptGeo(self, driver):
        try:
            acceptGeo = driver.find_elements(By.XPATH, '//a[.="CONTINUE"]')
            if len(acceptGeo) > 0:
                acceptGeo[0].click()
        except Exception as e:
            self.log_error(
                "Geolocation acceptance failed",
                error=str(e),
                exc_info=True,
            )
        return

    def getJobs(self, driver, web_page, company = 'sygnum') -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.implicitly_wait(5)
        driver.get(web_page)
        self.tryAcceptCookies(driver)
        self.tryAcceptGeo(driver)
        # use reverse strategy from a link to a title
        group_elements = driver.find_elements(By.XPATH, '//ul/li[@class="results-list__item result-item"]')
        result = []
        for elem in group_elements:
            job_name_elem = elem.find_element(By.XPATH, './/h3/a')
            job_name = job_name_elem.text
            job_url = job_name_elem.get_attribute('href')
            location_text : str = elem.find_element(By.XPATH, './/p[@class="result-item__location"]').text
            job = {
                "company": company,
                "title": job_name,
                "location": location_text.replace('United States', 'US').replace('United Kingdom', 'UK').replace('United Arab Emirates', 'UAE'),
                "link": job_url
            }
            result.append(job)
        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_found=len(group_elements),
            jobs_scraped=len(result),
        )
        return result
