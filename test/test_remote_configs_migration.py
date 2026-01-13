import json
import urllib.request
import pytest
from src.companies import Companies

@pytest.fixture
def remote_ai_companies():
    url = "https://raw.githubusercontent.com/crypto-jobs-fyi/crawler/refs/heads/main/ai_companies.json"
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())

@pytest.fixture
def remote_crypto_companies():
    url = "https://raw.githubusercontent.com/crypto-jobs-fyi/crawler/refs/heads/main/companies.json"
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())

def normalize_url(url):
    return url.lower().rstrip('/').replace('https://', '').replace('http://', '')

def test_verify_ai_companies_migration(remote_ai_companies):
    """
    Verify that all companies from the remote ai_companies.json 
    are present in the local companies.json.
    """
    local_companies = Companies.load_companies()
    local_names = {c.company_name.lower() for c in local_companies}
    
    missing_companies = []
    for remote_company in remote_ai_companies:
        name = remote_company['company_name'].lower()
        if name not in local_names:
            missing_companies.append(name)
            
    assert not missing_companies, f"Missing AI companies in companies.json: {', '.join(missing_companies)}"

def test_verify_ai_companies_urls(remote_ai_companies):
    """
    Verify that for each AI company, the jobs_url matches (ignoring case and protocol).
    """
    local_companies = Companies.load_companies()
    local_map = {c.company_name.lower(): c for c in local_companies}
    
    mismatched_urls = []
    for remote_company in remote_ai_companies:
        name = remote_company['company_name'].lower()
        if name in local_map:
            local_url_norm = normalize_url(local_map[name].jobs_url)
            remote_url_norm = normalize_url(remote_company['jobs_url'])
            
            if local_url_norm != remote_url_norm:
                mismatched_urls.append(f"{name}: {local_map[name].jobs_url} != {remote_company['jobs_url']}")
                
    assert not mismatched_urls, f"Mismatched jobs URLs for AI companies: {'; '.join(mismatched_urls)}"

def test_verify_crypto_companies_migration(remote_crypto_companies):
    """
    Verify that all companies from the remote companies.json (crypto)
    are present in the local companies.json.
    """
    local_companies = Companies.load_companies()
    local_names = {c.company_name.lower() for c in local_companies}
    
    missing_companies = []
    for remote_company in remote_crypto_companies:
        name = remote_company['company_name'].lower()
        if name not in local_names:
            missing_companies.append(name)
            
    assert not missing_companies, f"Missing crypto companies in companies.json: {', '.join(missing_companies)}"

def test_verify_crypto_companies_urls(remote_crypto_companies):
    """
    Verify that for each crypto company, the jobs_url matches (ignoring case and protocol).
    """
    local_companies = Companies.load_companies()
    local_map = {c.company_name.lower(): c for c in local_companies}
    
    mismatched_urls = []
    for remote_company in remote_crypto_companies:
        name = remote_company['company_name'].lower()
        if name in local_map:
            local_url_norm = normalize_url(local_map[name].jobs_url)
            remote_url_norm = normalize_url(remote_company['jobs_url'])
            
            if local_url_norm != remote_url_norm:
                mismatched_urls.append(f"{name}: {local_map[name].jobs_url} != {remote_company['jobs_url']}")
                
    assert not mismatched_urls, f"Mismatched jobs URLs for crypto companies: {'; '.join(mismatched_urls)}"
