import json
from src.company_list import get_company_list
from src.company_list import get_company

company_list = get_company_list()
print(f'Number of companies: {len(company_list)}')
result_list = []
for company in company_list:
    company_item = {
        "company_name": company.company_name,
        "company_url": company.company_url,
        "jobs_url": company.jobs_url,
    }
    result_list.append(company_item)
print(f'Number of companies in JSON: {len(result_list)}')
with open('companies.json', 'w') as f:
    json.dump(result_list, f, indent=4)

print(get_company('kraken'))
