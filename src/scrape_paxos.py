from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


def to_records(group_elements, company):
    result = []
    for elem in group_elements:
        job_url = elem.get_attribute('href')
        location_elem = elem.find_element(By.CSS_SELECTOR, 'div[class*="ashby-job-posting-brief-details"] p')
        location_text : str = location_elem.text.strip()
        job = {
            "company": company,
            "title": elem.find_element(By.CSS_SELECTOR, 'div h3').text,
            "location": location_text.replace('United States', 'US').replace('United Kingdom', 'UK').replace('United Arab Emirates', 'UAE'),
            "link": job_url
        }
        result.append(job)
    return result


class ScrapePaxos(ScrapeIt):
    name = 'PAXOS'

    def getJobs(self, driver, web_page, company='paxos'):
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.implicitly_wait(5)
        driver.get(web_page)
        group_elements = driver.find_elements(By.CSS_SELECTOR, 'div a[class*="_container"]')
        ## logging the number of job elements found
        self.log_info(
            "Found job elements",
            company=company,
            web_page=web_page,
            elements_found=len(group_elements),
        )
        result = to_records(group_elements, company)
        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_scraped=len(result),
        )
        return result
