from src.playwright_adapter import By
from src.playwright_adapter import PlaywrightWait
from src.playwright_adapter import PlaywrightConditions as EC
from src.scrape_it import ScrapeIt


class ScrapeCursor(ScrapeIt):
    name = 'Cursor'

    def getJobs(self, page, web_page, company) -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        page.implicitly_wait(15)
        page.get(web_page)
        PlaywrightWait(page, 15).until(
            EC.presence_of_element_located((By.XPATH, '//article/a[contains(@href, "/careers/")]'))
        )
        # Extract all data via JavaScript in one call to avoid stale element
        # issues caused by Next.js re-rendering after initial load.
        job_data = page.execute_script("""
            const links = Array.from(document.querySelectorAll('article a[href*="/careers/"]'));
            return links.map(a => {
                const titleElem = a.querySelector('p');
                const spans = a.querySelectorAll('div span');
                return {
                    href: a.href,
                    title: titleElem ? titleElem.textContent.trim() : '',
                    location: spans.length >= 5 ? spans[4].textContent.trim() : ''
                };
            });
        """) or []
        result = []
        for item in job_data:
            job_name = item.get('title', '')
            if not job_name:
                continue
            job = {
                "company": company,
                "title": job_name,
                "location": item.get('location', ''),
                "link": item.get('href', '')
            }
            result.append(job)
        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_found=len(job_data),
            jobs_scraped=len(result),
        )
        return result
