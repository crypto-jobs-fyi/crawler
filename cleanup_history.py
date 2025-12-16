"""
Script to remove company history entries that are not present in company_list.py
"""

import json
import sys
from src.company_list import get_company_list


def cleanup_history():
    """Remove history entries for companies not in company_list.py"""
    
    # Get list of active companies from company_list.py
    company_list = get_company_list()
    active_companies = {company.company_name for company in company_list}
    
    # Load history.json
    with open("history.json", "r") as f:
        history = json.load(f)
    
    # Find companies in history that are not in company_list
    history_companies = set(history.keys())
    # Exclude meta entries like "Total Jobs"
    companies_to_remove = (history_companies - active_companies) - {"Total Jobs"}
    
    if not companies_to_remove:
        print("✓ All companies in history.json are in company_list.py")
        return
    
    print(f"Found {len(companies_to_remove)} companies to remove:")
    for company in sorted(companies_to_remove):
        print(f"  - {company}")
    
    # Remove the companies
    for company in companies_to_remove:
        del history[company]
    
    # Write back to history.json
    with open("history.json", "w") as f:
        json.dump(history, f, indent=4)
    
    print(f"\n✓ Removed {len(companies_to_remove)} companies from history.json")
    print(f"✓ Remaining companies: {len(history)}")


if __name__ == "__main__":
    try:
        cleanup_history()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
