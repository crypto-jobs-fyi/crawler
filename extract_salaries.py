import json
import re
import os

def extract_salary(description):
    if not description:
        return None
    
    # Patterns to look for:
    # 1. Range: $180,000 - $300,000 USD
    # 2. Single value: $350K+
    # 3. Currency symbols: $, £, €, CAD
    # 4. Keywords: Salary, Compensation, Stipend, Pay
    
    patterns = [
        # Range with currency symbols/codes at start (e.g., $180,000 - $300,000, PLN 225,420 - 304,980)
        r'((?:[\$£€]|(?:USD|GBP|EUR|CAD|AUD|PLN))\s?[\d,.]+[kKmM]?\s?-\s?(?:(?:[\$£€]|(?:USD|GBP|EUR|CAD|AUD|PLN))\s?)?[\d,.]+[kKmM]?)',
        # Range with numbers and currency at the end (e.g., 165,000 - 185,000 GBP)
        r'([\d,.]+\s?-\s?[\d,.]+\s?(?:USD|GBP|EUR|CAD|AUD|PLN))',
        # Single value with currency symbol/code (e.g., $350K+, PLN 225,420)
        r'((?:[\$£€]|(?:USD|GBP|EUR|CAD|AUD|PLN))\s?[\d,.]+[kKmM]?\+?)',
        # Stipend/Weekly patterns (e.g., 3,850 USD / 2,310 GBP)
        r'([\d,.]+\s?(?:USD|GBP|EUR|CAD|AUD|PLN)\s?/\s?[\d,.]+\s?(?:USD|GBP|EUR|CAD|AUD|PLN))',
        # "Salary: $X" or "Compensation: $X"
        r'(?:Salary|Compensation|Stipend|Pay):\s?((?:[\$£€]|(?:USD|GBP|EUR|CAD|AUD|PLN))\s?[\d,.]+[kKmM]?)'
    ]
    
    def is_valid_salary(s):
        if not s:
            return False
        # Exclude funding/revenue numbers (M, million, billion)
        if re.search(r'[mM]\b|\bmillion\b|\bbillion\b', s, re.IGNORECASE):
            return False
        
        # Extract numeric part to check if it's too small (e.g., $2.5)
        nums = re.findall(r'[\d,.]+', s)
        for n in nums:
            try:
                # Remove thousand separators
                clean_n = n.replace(',', '')
                # Handle European dots if they are thousand separators (e.g. 155.000)
                if clean_n.count('.') == 1 and len(clean_n.split('.')[1]) == 3:
                    clean_n = clean_n.replace('.', '')
                
                val = float(clean_n)
                # If value is very small (like 2.5 or 150) and doesn't have 'k', it's likely not a salary
                # Note: PLN values are usually higher, so this threshold is safe
                if val < 1000 and 'k' not in s.lower():
                    return False
            except ValueError:
                continue
                
        return True

    # Search for "Salary" or "Compensation" context first to be more accurate
    context_search = re.search(r'(?:Salary|Compensation|Stipend|Pay Range|Base Salary).*?((?:[\$£€]|(?:USD|GBP|EUR|CAD|AUD|PLN))\s?[\d,.]+[^\n]*)', description, re.IGNORECASE | re.DOTALL)
    if context_search:
        line = context_search.group(0)
        for p in patterns:
            match = re.search(p, line)
            if match:
                res = match.group(1).strip()
                if is_valid_salary(res):
                    return res
    
    # Fallback to searching the whole description
    for p in patterns:
        for match in re.finditer(p, description):
            res = match.group(1).strip()
            if is_valid_salary(res):
                return res
            
    return None

def process_files():
    files = [
        'ai_jobs_ashby_descriptions.json',
        'ai_jobs_greenhouse_descriptions.json',
        'ai_jobs_lever_descriptions.json'
    ]
    
    for filename in files:
        if not os.path.exists(filename):
            print(f"File {filename} not found, skipping.")
            continue
            
        print(f"Processing {filename}...")
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"Error decoding {filename}, skipping.")
                continue
        
        updated_count = 0
        for entry in data:
            description = entry.get('description', '')
            salary = extract_salary(description)
            entry['salary'] = salary
            if salary:
                updated_count += 1
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"Finished {filename}. Found salary for {updated_count}/{len(data)} entries.")

if __name__ == "__main__":
    process_files()
