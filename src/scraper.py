#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

from const import (NEW_FORMAT_DIVISION, OLD_FORMAT_LINK, TO_REPLACE)
from utils import create_key
from dynamic_scraper import scrape_from_2016

def scrape_before_2016(soup):
    all_org_data = {}
    orgs = soup.findAll('li', attrs={'class': 'mdl-list__item mdl-list__item--one-line'})
    for org in orgs:
        link = org.find('a')
        org_name = link.text
        all_org_data[create_key(org_name)] = {
            "name": org_name,
        }
    return all_org_data


def scrape_year_data(year):
    print("DEBUG: Scraping data for {}...".format(year))
    if year < NEW_FORMAT_DIVISION:
        url = OLD_FORMAT_LINK.replace(TO_REPLACE, str(year))
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        return scrape_before_2016(soup)
    else:
        return scrape_from_2016(year)