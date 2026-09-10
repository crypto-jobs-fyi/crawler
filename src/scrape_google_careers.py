import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.scrape_it import ScrapeIt


class ScrapeGoogleCareers(ScrapeIt):
    name = 'GOOGLE_CAREERS'

    def getJobs(self, driver, web_page, company) -> list:
        self.log_info(
            "Scrape page",
            company=company,
            web_page=web_page,
        )
        driver.implicitly_wait(10)
        driver.get(web_page)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'a[href*="/about/careers/applications/jobs/details/"]')
                )
            )
        except Exception:
            time.sleep(5)

        job_data = driver.execute_script("""
            const selectors = [
              'a[href*="/about/careers/applications/jobs/details/"]',
              'a[href*="/careers/applications/jobs/details/"]'
            ];
            const links = Array.from(new Set(
              selectors.flatMap((selector) => Array.from(document.querySelectorAll(selector)))
            ));
            return links.map((a) => {
              const card = a.closest('li, article, section, div');
              const titleFromHeading = card ? card.querySelector('h2, h3, h4') : null;
              const title = (titleFromHeading?.textContent || a.textContent || '').trim();
              const locationNode = card
                ? card.querySelector('[aria-label*="Location"], [data-testid*="location"], [class*="location"]')
                : null;
              const location = (locationNode?.textContent || '').trim();
              return {
                href: a.href,
                title,
                location,
              };
            });
        """) or []

        seen_links = set()
        result = []
        for item in job_data:
            job_url = item.get("href", "")
            if not job_url or job_url in seen_links:
                continue
            seen_links.add(job_url)
            job_name = item.get("title", "").strip()
            if not job_name:
                continue
            location = item.get("location", "").strip() or "Unknown"
            result.append({
                "company": company,
                "title": job_name,
                "location": location,
                "link": job_url,
            })

        self.log_info(
            "Scrape summary",
            company=company,
            web_page=web_page,
            jobs_found=len(job_data),
            jobs_scraped=len(result),
        )
        return result
