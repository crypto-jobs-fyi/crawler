import time
from selenium.webdriver.common.by import By
from src.scrape_it import ScrapeIt


def clean_location(location):
    if 'remote' in location.lower() or 'global' in location.lower():
        return "REMOTE"
    joined = ' '.join(set(([x.strip() for x in location.split(',')])))
    return joined


class ScrapeRecruitee(ScrapeIt):
    def getJobs(self, driver, web_page, company) -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.get(web_page)
        driver.implicitly_wait(5)
        time.sleep(3)
        group_elements = driver.find_elements(By.CSS_SELECTOR, 'div [data-testid="offer-list-cards-desktop-display"] a[class*="-1"]')
        result = []
        for elem in group_elements:
            job_url = elem.get_attribute('href')
            job_name = elem.text
            job = {
                "company": company,
                "title": job_name,
                "location": "REMOTE",
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
