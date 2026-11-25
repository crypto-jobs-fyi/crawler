from src.playwright_adapter import By, PlaywrightConditions as EC
from src.playwright_adapter import PlaywrightElement, PlaywrightWait
from src.scrape_it import ScrapeIt


def clean_location(location: str) -> str:
    return location.strip()


class ScrapeFundamentalLabs(ScrapeIt):
    name = 'FUNDAMENTAL_LABS'
    _job_locator = 'a[href^="/careers/"]'

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
        job_links: list[tuple[str, str]] = []
        for elem in group_elements:
            title_element = elem.find_element(By.CSS_SELECTOR, 'span.t')
            description_elements = elem.find_elements(By.CSS_SELECTOR, 'span.s')
            title = title_element.text
            if description_elements:
                title = title.removesuffix(description_elements[0].text).strip()
            job_links.append((title, elem.get_attribute('href')))

        result: list = []
        for title, job_url in job_links:
            page.get(job_url)
            metadata = page.find_elements(By.CSS_SELECTOR, 'div.meta')
            location = ''
            if metadata:
                location = clean_location(metadata[0].text.split('·')[-1])
            result.append(
                {
                    "company": company,
                    "title": title,
                    "location": location,
                    "link": job_url,
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
