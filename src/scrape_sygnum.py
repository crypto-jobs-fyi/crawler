import time
from src.playwright_adapter import By
from src.scrape_it import ScrapeIt
# https://www.sygnum.com/careers-portal

class ScrapeSygnum(ScrapeIt):
    name = 'Sygnum'

    def tryAcceptCookies(self, page):
        try:
            acceptCookies = page.find_elements(By.XPATH, '//button[.="Accept"]')
            if len(acceptCookies) > 0:
                acceptCookies[0].click()
        except Exception as e:
            self.log_error(
                "Accept cookies failed",
                error=str(e),
                exc_info=True,
            )
        return
    
    def tryAcceptGeo(self, page):
        try:
            acceptGeo = page.find_elements(By.XPATH, '//a[.="CONTINUE"]')
            if len(acceptGeo) > 0:
                acceptGeo[0].click()
        except Exception as e:
            self.log_error(
                "Geolocation acceptance failed",
                error=str(e),
                exc_info=True,
            )
        return

    def tryClickClose(self, page):
        try:
            closeBtn = page.find_elements(By.XPATH, '//a[.="Close"]')
            if len(closeBtn) > 0:
                closeBtn[0].click()
        except Exception as e:
            self.log_error(
                "Close button click failed",
                error=str(e),
                exc_info=True,
            )
        return

    def getJobs(self, page, web_page, company = 'sygnum') -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        page.implicitly_wait(5)
        page.get(web_page)
        time.sleep(5) # wait for page to load after interactions
        self.tryAcceptCookies(page)
        self.tryAcceptGeo(page)
        self.tryClickClose(page)
        time.sleep(3) # wait for page to load after interactions
        # use reverse strategy from a link to a title
        group_elements = page.find_elements(By.XPATH, '//ul/li[@class="results-list__item result-item"]')
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
