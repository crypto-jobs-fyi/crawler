from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.scrape_it import ScrapeIt, write_jobs


def clean_location(location: str):
    location = location.replace("/ Full-time", "")
    if 'global' in location.lower() or 'remote : remote' in location.lower():
        return "REMOTE"
    set_of_locations = set(([x.strip() for x in location.split(',')]))
    result_locations = set()
    for loc in set_of_locations:
        if loc.endswith('/'):
            result_locations.add(loc[0:-1].strip())
            break
        result_locations.add(loc)
    return ' '.join(result_locations)


class ScrapeBinance(ScrapeIt):
    def getJobs(self, driver, web_page, company='binance') -> []:
        print(f'[BINANCE] Scrap page: {web_page}')
        driver.get(web_page)
        wait = WebDriverWait(driver, 120)
        apply_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[.="Apply"]')))
        group_elements = driver.find_elements(By.XPATH, '//div[contains(@class,"posting")]')
        print(f'[BINANCE] Found {len(apply_buttons)} jobs on {web_page}')
        result = []
        for elem in group_elements:
            link_elem = elem.find_element(By.CSS_SELECTOR, 'a')
            location_elem = elem.find_element(By.CSS_SELECTOR, 'div[data-bn-type="text"]')
            job_url = link_elem.get_attribute('href')
            location = clean_location(location_elem.text)
            job_name = link_elem.text
            job = {
                "company": company,
                "title": job_name,
                "location": location,
                "link": f"<a href='{job_url}' target='_blank' >Apply</a>"
            }
            result.append(job)
        print(f'[BINANCE] Scraped {len(result)} jobs from {web_page}')
        write_jobs(result)
        return result
