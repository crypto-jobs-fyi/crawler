import json
from typing import Any

from src.scrape_lever import ScrapeLever
from src.company_item import CompanyItem
from src.scrape_ashbyhq import ScrapeAshbyhq
from src.scrape_greenhouse import ScrapeGreenhouse


def get_company_list() -> list[CompanyItem | Any]:
    return [
        CompanyItem('groq', 'https://job-boards.greenhouse.io/groq', ScrapeGreenhouse, 'https://groq.com'),
        CompanyItem('GPTZero', 'https://jobs.ashbyhq.com/GPTZero', ScrapeAshbyhq, 'https://gptzero.me'),
        CompanyItem("perplexityai", "https://job-boards.greenhouse.io/perplexityai", ScrapeGreenhouse,
                    "https://www.perplexity.ai"),
        CompanyItem('characterai', 'https://jobs.ashbyhq.com/character', ScrapeAshbyhq, 'https://character.ai'),
        CompanyItem("cohere", "https://jobs.ashbyhq.com/cohere", ScrapeAshbyhq, "https://cohere.com"),
        CompanyItem("reka", "https://jobs.ashbyhq.com/reka", ScrapeAshbyhq, "https://www.reka.ai"),
        CompanyItem("sesame", "https://jobs.ashbyhq.com/sesame", ScrapeAshbyhq, "https://www.sesame.com"),
        CompanyItem("everai", "https://jobs.ashbyhq.com/everai", ScrapeAshbyhq, "https://www.everai.ai"),
        CompanyItem("elevenlabs", "https://jobs.ashbyhq.com/elevenlabs", ScrapeAshbyhq, "https://elevenlabs.io"),
        CompanyItem('invisibletech', 'https://job-boards.eu.greenhouse.io/invisibletech', ScrapeGreenhouse, 'https://www.invisible.co'),
        CompanyItem('blackforestlabs', 'https://job-boards.greenhouse.io/blackforestlabs', ScrapeGreenhouse, 'https://bfl.ai'),
        CompanyItem("mistral", "https://jobs.lever.co/mistral", ScrapeLever, "https://mistral.ai"),
        CompanyItem("lovable", "https://jobs.ashbyhq.com/lovable", ScrapeAshbyhq, "https://lovable.dev"),
        CompanyItem("windsurf", "https://jobs.ashbyhq.com/windsurf", ScrapeAshbyhq, "https://windsurf.com"),
        CompanyItem("eliseai", "https://jobs.ashbyhq.com/eliseai", ScrapeAshbyhq, "https://www.eliseai.com"),
        CompanyItem('deepmind', 'https://job-boards.greenhouse.io/deepmind', ScrapeGreenhouse, 'https://deepmind.google'),
        CompanyItem('scaleai', 'https://job-boards.greenhouse.io/scaleai', ScrapeGreenhouse, 'https://scale.com'),
        CompanyItem('arizeai', 'https://job-boards.greenhouse.io/arizeai', ScrapeGreenhouse, 'https://arize.com'),
        CompanyItem('xai', 'https://job-boards.greenhouse.io/xai', ScrapeGreenhouse, 'https://x.ai'),
    ]


def get_company(name) -> CompanyItem:
    company_list = get_company_list()
    companies = list(filter(lambda jd: jd.company_name == name, company_list))
    if len(companies) > 1:
        raise NameError(f'Duplicated company name: {name}')
    return companies[0]


def write_companies(file_name):
    result_list = []
    for com in get_company_list():
        company_item = {
            "company_name": com.company_name,
            "company_url": com.company_url,
            "jobs_url": com.jobs_url,
        }
        result_list.append(company_item)
    print(f'[COMPANY_LIST] Number of Companies writen {len(result_list)}')
    with open(file_name, 'w') as companies_file:
        json.dump(result_list, companies_file, indent=4)
