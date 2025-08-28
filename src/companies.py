import json


from src.company_item import CompanyItem

class Companies:

    @staticmethod
    def get_company(name: str, company_list: list[CompanyItem]) -> CompanyItem:
        companies = list(filter(lambda jd: jd.company_name == name, company_list))
        if len(companies) > 1:
            raise NameError(f'Duplicated company name: {name}')
        return companies[0]

    @staticmethod
    def write_companies(file_name, company_list: list[CompanyItem]):
        result_list = []
        for com in company_list:
            company_item = {
                "company_name": com.company_name,
                "company_url": com.company_url,
                "jobs_url": com.jobs_url,
            }
            result_list.append(company_item)
        print(f'[COMPANY_LIST] Number of Companies writen {len(result_list)}')
        with open(file_name, 'w') as companies_file:
            json.dump(result_list, companies_file, indent=4)

    @staticmethod
    def filter_companies(company_list: list[CompanyItem], scraper_type) -> list[CompanyItem]:
        return [company for company in company_list if getattr(company, 'scraper_type', None) == scraper_type]
    
    @staticmethod
    def filter_companies_not(company_list: list[CompanyItem], scraper_types: list) -> list[CompanyItem]:
        return [company for company in company_list if getattr(company, 'scraper_type', None) not in scraper_types]
