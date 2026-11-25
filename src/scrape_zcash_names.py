from src.playwright_adapter import By, PlaywrightConditions as EC
from src.playwright_adapter import PlaywrightElement, PlaywrightWait
from src.scrape_it import ScrapeIt


class ScrapeZcashNames(ScrapeIt):
    name = 'ZCASH_NAMES'
    _job_locator = 'article h2 a[href^="/careers/"]'

    def getJobs(self, page, web_page, company) -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        page.implicitly_wait(7)
        page.get(web_page)
        group_elements: list[PlaywrightElement] = PlaywrightWait(page, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, self._job_locator))
        )
        result: list = []
        for elem in group_elements:
            result.append(
                {
                    "company": company,
                    "title": elem.text.strip(),
                    "location": "",
                    "link": elem.get_attribute('href'),
                }
            )
        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_found=len(group_elements),
            jobs_scraped=len(result),
        )
        return result
