"""
Script to remove company history entries that are not present in the company list files
"""

import json
import sys
from src.company_list import get_company_list as get_crypto_companies
from src.company_ai_list import get_company_list as get_ai_companies
from src.company_fin_list import get_company_list as get_fin_companies


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
        print(f"✓ All companies in {history_file} are in {label} list")
        return 0, len(history)
    
    print(f"Found {len(companies_to_remove)} companies to remove from {label}:")
    for company in sorted(companies_to_remove):
        print(f"  - {company}")
    
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
    crypto_companies = get_crypto_companies()
    ai_companies = get_ai_companies()
    fin_companies = get_fin_companies()
    
    files_to_clean = [
        ("history.json", crypto_companies, "Crypto"),
        ("ai_history.json", ai_companies, "AI"),
        ("fin_history.json", fin_companies, "Fintech"),
    ]
    
    total_removed = 0
    
    for history_file, company_list, label in files_to_clean:
        try:
            print(f"\nCleaning {label} history ({history_file})...")
            removed, remaining = cleanup_history(history_file, company_list, label)
            total_removed += removed
            print(f"  ✓ Removed {removed} companies")
            print(f"  ✓ Remaining companies: {remaining}")
        except FileNotFoundError:
            print(f"  ✗ File not found: {history_file}")
        except Exception as e:
            print(f"  ✗ Error: {e}", file=sys.stderr)
    
    print(f"\n✓ Total removed: {total_removed} invalid company entries")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
