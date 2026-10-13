import json
import re
import unicodedata

from src.playwright_adapter import By
from src.playwright_adapter import PlaywrightConditions as EC
from src.playwright_adapter import PlaywrightPageAdapter, PlaywrightWait
from src.scrape_it import ScrapeIt


class ScrapeRevolut(ScrapeIt):
    name = "REVOLUT"
    _next_data_locator = "script#__NEXT_DATA__"

    @staticmethod
    def _slugify_title(title: str) -> str:
        normalized = unicodedata.normalize("NFKD", title)
        ascii_title = normalized.encode("ascii", "ignore").decode("ascii")
        return re.sub(r"[^a-z0-9]+", "-", ascii_title.lower()).strip("-")

    @staticmethod
    def _location_text(locations: list[dict]) -> str:
        values = []
        for location in locations:
            location_type = location.get("type")
            label = "Office" if location_type == "office" else "Remote"
            value = location.get("country") if location_type == "remote" else location.get("name")
            if value:
                values.append(f"{label}: {value}")
        return "; ".join(values)

    def getJobs(
        self,
        page: PlaywrightPageAdapter,
        web_page: str,
        company: str,
    ) -> list:
        self.log_info("Scrape page", company=company, web_page=web_page)
        page.implicitly_wait(10)
        page.get(web_page)
        PlaywrightWait(page, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self._next_data_locator))
        )
        raw_data = page.execute_script(
            "return document.querySelector('#__NEXT_DATA__').textContent;"
        )
        if not raw_data:
            raise RuntimeError("Revolut careers page did not expose Next.js data")

        page_data = json.loads(raw_data)
        positions = page_data["props"]["pageProps"]["positions"]
        result = []
        for position in positions:
            title = position.get("text", "").strip()
            position_id = position.get("id", "").strip()
            location = self._location_text(position.get("locations", []))
            if not title or not position_id or not location:
                self.log_warning(
                    "Skipping incomplete position",
                    company=company,
                    position_id=position_id,
                )
                continue

            slug = self._slugify_title(title)
            link = f"https://www.revolut.com/careers/position/{slug}-{position_id}/"
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
            jobs_found=len(positions),
            jobs_scraped=len(result),
        )
        return result
