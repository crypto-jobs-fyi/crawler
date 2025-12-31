"""
Script to scrape job descriptions from Greenhouse.io job links in ai_jobs_greenhouse.json
Uses Selenium with parallel threading (4 threads) to fetch description text 
from CSS selector '.job__description.body'
"""

import sys
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.scrape_descriptions_base import BaseScraper


class GreenhouseScraper(BaseScraper):
    """Scraper for Greenhouse.io jobs with parallel threading support"""
    
    def __init__(self, num_threads: int = 4):
        super().__init__(
            source_file="ai_jobs_greenhouse.json",
            output_file="ai_jobs_greenhouse_descriptions.json",
            num_threads=num_threads
        )
    
    def scrape_job_details(self, link: str, timeout: int = 10) -> Optional[dict]:
        """Scrape job title and description from Greenhouse.io link"""
        driver = self.get_driver()
        
        try:
            driver.get(link)
            
            # Wait for description element to be present
            wait = WebDriverWait(driver, timeout)
            
            # Get Title
            try:
                title_element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".job__title h1"))
                )
                title = title_element.text.strip()
            except:
                title = "Unknown Title"

            # Get Location
            try:
                location_element = driver.find_element(By.CSS_SELECTOR, ".job__location")
                location = location_element.text.strip()
            except:
                location = "Unknown Location"

            # Get Description
            description_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".job__description.body"))
            )
            
            # Get the text content
            description = description_element.text
            
            if description and description.strip():
                return {
                    "title": title,
                    "location": location,
                    "description": description
                }
            return None
        
        except TimeoutException:
            print(f"  ✗ Timeout waiting for elements: {link}", file=sys.stderr)
            return None
        except NoSuchElementException:
            print(f"  ✗ Elements not found: {link}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"  ✗ Error scraping {link}: {e}", file=sys.stderr)
            return None
        finally:
            driver.quit()


if __name__ == "__main__":
    try:
        scraper = GreenhouseScraper(num_threads=4)
        scraper.run()
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

