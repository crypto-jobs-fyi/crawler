import re

from src.playwright_adapter import By, PlaywrightConditions as EC, PlaywrightWait
from src.scrape_it import ScrapeIt


class ScrapeDayforce(ScrapeIt):
    name = "Dayforce"

    _card_locator = '[test-id="job-posting-card"], [data-testid="job-posting-card"]'
    _title_locator = (
        'h1, h2, h3, h4, '
        '[test-id*="title"], [data-testid*="title"]'
    )
    _location_locator = (
        '[test-id*="location"], [data-testid*="location"], '
        '[aria-label*="location" i]'
    )

    def getJobs(self, page, web_page, company) -> list:
        self.log_info("Scrape page", company=company, web_page=web_page)
        page.implicitly_wait(15)
        page.get(web_page)

        cards = PlaywrightWait(page, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, self._card_locator))
        )
        result = []
        seen_links = set()

        while True:
            self._append_jobs(result, seen_links, cards, company)
            current_page, total_pages = self._pagination_state(page)
            if current_page is None or total_pages is None or current_page >= total_pages:
                break

            next_page = page.find_elements(
                By.CSS_SELECTOR,
                '[title="Next Page"] [aria-label="Go to next page"]',
            )
            if not next_page:
                break

            next_page[0].click()
            expected_page = current_page + 1
            PlaywrightWait(page, 20).until(
                lambda current: self._current_page(current) == expected_page
            )
            cards = PlaywrightWait(page, 20).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, self._card_locator)
                )
            )

        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_found=len(cards),
            jobs_scraped=len(result),
        )
        return result

    def _append_jobs(self, result, seen_links, cards, company) -> None:
        for card in cards:
            title = self._extract_title(card)
            location = self._extract_location(card, title)
            link = card.get_attribute("href")
            if not link:
                links = card.find_elements(By.CSS_SELECTOR, "a[href]")
                link = links[0].get_attribute("href") if links else None

            if not title or not location or not link:
                self.log_warning(
                    "Skipping incomplete job card",
                    company=company,
                    has_title=bool(title),
                    has_location=bool(location),
                    has_link=bool(link),
                )
                continue
            if link in seen_links:
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

    def _pagination_state(self, page) -> tuple[int | None, int | None]:
        pagination = page.find_elements(
            By.CSS_SELECTOR,
            'ul[aria-label^="Page "]',
        )
        if not pagination:
            return None, None

        label = pagination[0].get_attribute("aria-label") or ""
        match = re.fullmatch(r"Page (\d+) of (\d+)", label)
        if not match:
            return None, None
        return int(match.group(1)), int(match.group(2))

    def _current_page(self, page) -> int | None:
        current = page.find_elements(
            By.CSS_SELECTOR,
            '[role="link"][aria-current="true"]',
        )
        if not current:
            return None
        match = re.fullmatch(
            r"Page (\d+)",
            current[0].get_attribute("aria-label") or "",
        )
        return int(match.group(1)) if match else None

    def _extract_title(self, card) -> str:
        title_elements = card.find_elements(By.CSS_SELECTOR, self._title_locator)
        if title_elements:
            return self._clean_text(title_elements[0].text)

        lines = self._text_lines(card.text)
        return lines[0] if lines else ""

    def _extract_location(self, card, title: str) -> str:
        location_elements = card.find_elements(By.CSS_SELECTOR, self._location_locator)
        for element in location_elements:
            location = self._clean_text(element.text)
            if location:
                return location

        lines = self._text_lines(card.text)
        for line in lines:
            if line == title:
                continue
            if line.startswith(title):
                line = self._clean_text(line[len(title):])
            if line and line != title:
                return line
        return ""

    @staticmethod
    def _text_lines(text: str) -> list[str]:
        return [line for line in (text or "").splitlines() if line.strip()]

    @staticmethod
    def _clean_text(text: str) -> str:
        return " ".join((text or "").split())
