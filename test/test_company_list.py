import pytest
from src.companies import Companies
from src.company_item import CompanyItem

def test_load_companies():
    """Test that Companies.load_companies returns a non-empty list of CompanyItem objects."""
    companies = Companies.load_companies()
    assert isinstance(companies, list)
    assert len(companies) > 0
    for company in companies:
        assert isinstance(company, CompanyItem)
        assert company.company_name
        assert company.jobs_url
        assert company.scraper_type
        assert company.company_url

def test_get_company_found():
    """Test that Companies.get_company can find a company by name in the list."""
    companies = Companies.load_companies()
    # 'kraken' is known to be in the list
    company = Companies.get_company('kraken', companies)
    assert company.company_name == 'kraken'
    assert 'kraken.com' in company.jobs_url

def test_get_company_not_found():
    """Test that Companies.get_company raises IndexError when company is not found."""
    companies = Companies.load_companies()
    with pytest.raises(IndexError):
        Companies.get_company('non_existent_company_xyz', companies)
