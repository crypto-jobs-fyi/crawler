from src.playwright_adapter import By
from src.playwright_adapter import PlaywrightConditions as EC
from src.playwright_adapter import PlaywrightElement, PlaywrightPageAdapter, PlaywrightWait
from src.scrape_it import ScrapeIt


class ScrapeRippling(ScrapeIt):
    name = "RIPPLING"
    _job_locator = 'a[href*="/jobs/"]:not(:has(button))'

    def getJobs(
        self,
        page: PlaywrightPageAdapter,
        web_page: str,
        company: str,
    ) -> list:
        self.log_info("Scrape page", company=company, web_page=web_page)
        page.implicitly_wait(10)
        page.get(web_page)
        cards: list[PlaywrightElement] = PlaywrightWait(page, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, self._job_locator))
        )

        result = []
        seen_links = set()
        for card in cards:
            title = card.text.strip()
            location = card.find_element(
                By.XPATH,
                './../..//span[@data-icon="LOCATION_OUTLINE"]/following-sibling::p',
            ).text.strip()
            link = card.get_attribute("href")
            if not title or not location or not link or link in seen_links:
                continue
            seen_links.add(link)
            result.append(
                {
                    "company": company,
                    "title": title,
                    "location": location,
                    "link": link,
                }
            )

        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_found=len(cards),
            jobs_scraped=len(result),
        )
        return result
