import json
import sys
import time
import os
from typing import Optional, Dict, List
from threading import Thread, Lock
from queue import Queue
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BaseScraper:
    """Base class for job description scrapers with parallel threading support"""
    
    def __init__(self, source_file: str, output_file: str, num_threads: int = 4):
        self.source_file = source_file
        self.output_file = output_file
        self.num_threads = num_threads
        self.results = []
        self.scraped_links = set()
        self.results_lock = Lock()
        self.queue = Queue()
        self.successful = 0
        self.failed = 0
        self.stats_lock = Lock()
        self._load_existing_results()
    
    def _load_existing_results(self):
        """Load existing results from output file if it exists"""
        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, "r") as f:
                    self.results = json.load(f)
                    self.scraped_links = {item["link"] for item in self.results}
                print(f"Loaded {len(self.results)} existing results from {self.output_file}")
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Could not load existing results: {e}", file=sys.stderr)
                self.results = []
                self.scraped_links = set()
    
    def extract_links(self) -> List[str]:
        """Extract links from source JSON file that haven't been scraped"""
        try:
            with open(self.source_file, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading {self.source_file}: {e}", file=sys.stderr)
            return []
        
        links = []
        if isinstance(data, dict) and "data" in data:
            for job in data["data"]:
                if isinstance(job, dict) and "link" in job:
                    link = job["link"]
                    if link not in self.scraped_links:
                        links.append(link)
        
        return links

    def get_driver(self):
        """Initialize and return a headless Chrome driver"""
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")
        return webdriver.Chrome(options=options)

    def scrape_job_details(self, link: str, timeout: int = 10) -> Optional[Dict]:
        """To be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement scrape_job_details")

    def worker(self, thread_id: int, total: int):
        """Worker thread to process scraping tasks"""
        while True:
            task = self.queue.get()
            
            if task is None:
                self.queue.task_done()
                break
            
            idx, link = task
            print(f"[Thread {thread_id}] [{idx}/{total}] Scraping: {link}")
            
            task_start = time.time()
            # Force max 10s timeout as requested
            job_details = self.scrape_job_details(link, timeout=10)
            task_duration = time.time() - task_start
            
            with self.stats_lock:
                if job_details:
                    with self.results_lock:
                        self.results.append({
                            "link": link,
                            **job_details
                        })
                    self.successful += 1
                    title = job_details.get("title", "Unknown")
                    print(f"  ✓ Success: {title} ({len(job_details.get('description', ''))} chars) in {task_duration:.2f}s")
                else:
                    self.failed += 1
                    print(f"  ✗ Failed: {link} in {task_duration:.2f}s")
            
            self.queue.task_done()

    def scrape_all(self, links: List[str]):
        """Scrape all links using multiple threads"""
        total = len(links)
        threads = []
        for i in range(self.num_threads):
            t = Thread(target=self.worker, args=(i + 1, total))
            t.start()
            threads.append(t)
        
        for idx, link in enumerate(links, 1):
            self.queue.put((idx, link))
        
        self.queue.join()
        
        for _ in range(self.num_threads):
            self.queue.put(None)
        
        for t in threads:
            t.join()

    def save_results(self):
        """Save results to JSON file"""
        with open(self.output_file, "w") as f:
            json.dump(self.results, f, indent=2)

    def run(self):
        """Main execution flow"""
        print(f"Extracting links from {self.source_file}...")
        links = self.extract_links()
        
        if not links:
            print(f"No new links to scrape in {self.source_file}")
            return
        
        print(f"Found {len(links)} new links to scrape")
        print(f"Starting scraper with {self.num_threads} threads...\n")
        
        start_time = time.time()
        self.scrape_all(links)
        elapsed_time = time.time() - start_time
        
        self.save_results()
        
        print(f"\n✓ Scraping complete!")
        print(f"  New successful: {self.successful}")
        print(f"  New failed: {self.failed}")
        print(f"  Total scraped: {len(self.results)}")
        print(f"  Total time: {elapsed_time:.2f} seconds")
        if self.successful + self.failed > 0:
            avg_time = elapsed_time / (self.successful + self.failed)
            print(f"  Average time per task: {avg_time:.2f} seconds")
        print(f"  Results saved to: {self.output_file}")
