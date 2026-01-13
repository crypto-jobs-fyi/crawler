"""
Script to remove job links from jobs age files that are not in the jobs.json files
"""

import json
import sys
import re
from src.logging_utils import get_logger

logger = get_logger(__name__)


def extract_url_from_html_link(html_link: str) -> str:
    """Extract URL from HTML link tag like <a href='url'>text</a>"""
    match = re.search(r"href='([^']+)'", html_link)
    return match.group(1) if match else ""


def get_job_links_from_json(jobs_file: str) -> set[str]:
    """Extract all job links from jobs.json file"""
    try:
        with open(jobs_file, "r") as f:
            data = json.load(f)
        
        links = set()
        if "data" in data and isinstance(data["data"], list):
            for job in data["data"]:
                if "link" in job:
                    links.add(job["link"])
        return links
    except FileNotFoundError:
        logger.error(
            "Jobs file missing",
            extra={"jobs_file": jobs_file},
        )
        return set()


def cleanup_jobs_age(age_file: str, valid_links: set[str]) -> tuple[int, int]:
    """Remove job links not present in the jobs.json file"""
    
    with open(age_file, "r") as f:
        data = json.load(f)
    
    links_to_remove = []
    for link_key in data.keys():
        # Try to extract URL if it's an HTML link tag
        extracted_url = extract_url_from_html_link(link_key)
        
        # Check if either the key itself or extracted URL is in valid links
        if extracted_url and extracted_url in valid_links:
            # Valid link found
            continue
        elif link_key in valid_links:
            # Direct match
            continue
        else:
            # No match found
            links_to_remove.append(link_key)
    
    # Remove invalid links
    for link in links_to_remove:
        del data[link]
    
    # Write back
    with open(age_file, "w") as f:
        json.dump(data, f, indent=4)
    
    return len(links_to_remove), len(data)


def main():
    """Clean all jobs age files"""
    
    # Get valid links from jobs.json files
    crypto_links = get_job_links_from_json("jobs.json")
    ai_links = get_job_links_from_json("ai_jobs.json")
    fin_links = get_job_links_from_json("fin_jobs.json")
    
    files_to_clean = [
        ("jobs_age.json", crypto_links, "Crypto"),
        ("ai_jobs_age.json", ai_links, "AI"),
        ("fin_jobs_age.json", fin_links, "Fintech"),
    ]
    
    total_removed = 0
    
    for age_file, valid_links, label in files_to_clean:
        try:
            logger.info(
                "Jobs age cleanup start",
                extra={"label": label, "age_file": age_file},
            )
            if not valid_links:
                logger.warning(
                    "No valid links",
                    extra={"label": label, "age_file": age_file},
                )
                continue
            removed, remaining = cleanup_jobs_age(age_file, valid_links)
            total_removed += removed
            logger.info(
                "Jobs age cleanup summary",
                extra={
                    "label": label,
                    "age_file": age_file,
                    "removed": removed,
                    "remaining": remaining,
                },
            )
        except FileNotFoundError:
            logger.error(
                "Age file missing",
                extra={"age_file": age_file},
            )
        except Exception as e:
            logger.error(
                "Age cleanup error",
                extra={"age_file": age_file, "label": label},
                exc_info=True,
            )

    logger.info(
        "Jobs age cleanup complete",
        extra={"total_removed": total_removed},
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error("Cleanup failure", extra={"error": str(e)}, exc_info=True)
        sys.exit(1)
