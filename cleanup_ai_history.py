"""
Script to remove AI company history entries that are not present in company_ai_list.py
"""

import json
import sys
from src.company_ai_list import get_company_list


def cleanup_ai_history():
    """Remove AI history entries for companies not in company_ai_list.py"""
    
    # Get list of active AI companies from company_ai_list.py
    company_list = get_company_list()
    active_companies = {company.company_name for company in company_list}
    
    # Load ai_history.json (AI jobs history)
    with open("ai_history.json", "r") as f:
        history = json.load(f)
    
    # Find companies in history that are not in company_ai_list
    history_companies = set(history.keys())
    # Exclude meta entries like "Total Jobs"
    companies_to_remove = (history_companies - active_companies) - {"Total Jobs"}
    
    if not companies_to_remove:
        print("✓ All companies in ai_history.json are in company_ai_list.py")
        return
    
    print(f"Found {len(companies_to_remove)} companies to remove:")
    for company in sorted(companies_to_remove):
        print(f"  - {company}")
    
    # Remove the companies
    for company in companies_to_remove:
        del history[company]
    
    # Write back to ai_history.json
    with open("ai_history.json", "w") as f:
        json.dump(history, f, indent=4)
    
    print(f"\n✓ Removed {len(companies_to_remove)} companies from ai_history.json")
    print(f"✓ Remaining companies: {len(history)}")


if __name__ == "__main__":
    try:
        cleanup_ai_history()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
