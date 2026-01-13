"""
Script to remove company history entries that are not present in the company list files
"""

import json
import sys
from src.companies import Companies
from src.logging_utils import get_logger

logger = get_logger(__name__)


def cleanup_history(history_file: str, company_list: list, label: str) -> tuple[int, int]:
    """Remove history entries for companies not in the company list"""
    
    # Get active company names
    active_companies = {company.company_name for company in company_list}
    
    # Load history file
    with open(history_file, "r") as f:
        history = json.load(f)
    
    # Find companies in history that are not in company list
    history_companies = set(history.keys())
    # Exclude meta entries like "Total Jobs"
    companies_to_remove = (history_companies - active_companies) - {"Total Jobs"}
    
    if not companies_to_remove:
        logger.info(
            "History validation",
            extra={"history_file": history_file, "label": label, "message": "No removals"},
        )
        return 0, len(history)
    
    logger.info(
        "History removals identified",
        extra={
            "history_file": history_file,
            "label": label,
            "removal_count": len(companies_to_remove),
        },
    )
    for company in sorted(companies_to_remove):
        logger.info(
            "History removal candidate",
            extra={"history_file": history_file, "label": label, "company": company},
        )
    
    # Remove the companies
    for company in companies_to_remove:
        del history[company]
    
    # Write back to history file
    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)
    
    return len(companies_to_remove), len(history)


def main():
    """Clean all history files"""
    
    # Get all company lists
    crypto_companies = Companies.filter_companies(category="crypto")
    ai_companies = Companies.filter_companies(category="ai")
    fin_companies = Companies.filter_companies(category="fintech")
    tech_companies = Companies.filter_companies(category="tech")
    
    files_to_clean = [
        ("crypto_history.json", crypto_companies, "Crypto"),
        ("ai_history.json", ai_companies, "AI"),
        ("fin_history.json", fin_companies, "Fintech"),
        ("tech_history.json", tech_companies, "Tech"),
    ]
    
    total_removed = 0
    
    for history_file, company_list, label in files_to_clean:
        try:
            logger.info(
                "History cleanup start",
                extra={"history_file": history_file, "label": label},
            )
            removed, remaining = cleanup_history(history_file, company_list, label)
            total_removed += removed
            logger.info(
                "History cleanup summary",
                extra={
                    "history_file": history_file,
                    "label": label,
                    "removed": removed,
                    "remaining": remaining,
                },
            )
        except FileNotFoundError:
            logger.error(
                "History file missing",
                extra={"history_file": history_file, "label": label},
            )
        except Exception as e:
            logger.error(
                "History cleanup error",
                extra={"history_file": history_file, "label": label},
                exc_info=True,
            )

    logger.info(
        "History cleanup complete",
        extra={"total_removed": total_removed},
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error("Cleanup failure", extra={"error": str(e)}, exc_info=True)
        sys.exit(1)
