from src.playwright_adapter import By, PlaywrightConditions as EC
from src.playwright_adapter import PlaywrightElement, PlaywrightWait
from src.scrape_it import ScrapeIt


def clean_location(location: str) -> str:
    return location.strip()


class ScrapeWorkato(ScrapeIt):
    name = 'WORKATO'
    _job_locator = 'a.job-list__list'
    _load_more_locator = 'button.jobs-viewer__load-more'

    def getJobs(self, page, web_page, company) -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        page.implicitly_wait(7)
        page.get(web_page)
        PlaywrightWait(page, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, self._job_locator))
        )

        while True:
            load_more_buttons: list[PlaywrightElement] = [
                button
                for button in page.find_elements(
                    By.CSS_SELECTOR,
                    self._load_more_locator,
                )
                if button.is_displayed() and button.get_attribute('disabled') is None
            ]
            if not load_more_buttons:
                break

            previous_count = len(
                page.find_elements(By.CSS_SELECTOR, self._job_locator)
            )
            load_more_buttons[0].click()
            PlaywrightWait(page, 20).until(
                lambda current_page: len(
                    current_page.find_elements(By.CSS_SELECTOR, self._job_locator)
                ) > previous_count
            )

        group_elements: list[PlaywrightElement] = page.find_elements(
            By.CSS_SELECTOR,
            self._job_locator,
        )
        result: list = []
        for elem in group_elements:
            job_name = elem.find_element(
                By.CSS_SELECTOR,
                'div.job-vacancy__title',
            ).text
            location = elem.find_element(
                By.CSS_SELECTOR,
                'div.job-list__location',
            ).text
            result.append(
                {
                    "company": company,
                    "title": job_name,
                    "location": clean_location(location),
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
