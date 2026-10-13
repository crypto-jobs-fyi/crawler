from playwright.sync_api import Page

from src.playwright_scrape_it import PlaywrightScrapeIt


def clean_location(location: str) -> str:
    return (
        location.replace("United States", "US")
        .replace("United Kingdom", "UK")
        .replace("Singapore, Singapore", "Singapore")
        .replace("New York, New York", "New York")
        .strip()
    )


class ScrapeKulaPlaywright(PlaywrightScrapeIt):
    name = "Kula"

    def getJobs(self, page: Page, web_page: str, company: str) -> list[dict]:
        self.log_info("Scrape page", company=company, web_page=web_page)
        page.goto(web_page, wait_until="domcontentloaded", timeout=60_000)

        cards = page.locator('div[class*="chakra-card"]')
        result = []
        for index in range(cards.count()):
            card = cards.nth(index)
            text_elements = card.locator('div[class*="chakra-stack"] p[class*="chakra-text"]')
            title = self._text(text_elements.nth(0), "Unknown") if text_elements.count() else "Unknown"
            location = (
                self._text(text_elements.nth(1), "Unknown")
                if text_elements.count() > 1
                else "Unknown"
            )
            link = card.locator('a[class*="chakra-link"]')
            result.append(
                {
                    "company": company,
                    "title": title,
                    "location": clean_location(location),
                    "link": self._href(link, page.url),
                }
            )

        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_found=cards.count(),
            jobs_scraped=len(result),
        )
        return result
