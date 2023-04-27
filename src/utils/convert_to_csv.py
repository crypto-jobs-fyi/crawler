# Add the parent directory of the script to the Python path
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import csv
from src.company_list import get_company_list

company_list = get_company_list()

print(len(company_list))

# def process_input(company_list):
#     csv_data = [('Name', 'Jobs URL', 'Company URL', 'Category')]

#     for item in company_list:
#         csv_data.append((item.company_name, item.jobs_url, item.company_url, item.company_type))

#     return csv_data

# csv_data = process_input(company_list)

# with open('src/utils/companies.csv', 'w', newline='') as csvfile:
#     csv_writer = csv.writer(csvfile)
#     csv_writer.writerows(csv_data)

# print('CSV file has been created.')
