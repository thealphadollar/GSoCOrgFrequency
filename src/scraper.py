#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

from const import (NEW_FORMAT_DIVISION, NEW_FORMAT_LINK, OLD_FORMAT_LINK,
                   ROOT_URL, TO_REPLACE)
from utils import create_key


def scrape_from_2016(soup):
    all_org_data = {}
    orgs = soup.findAll('li', attrs={'class': 'organization-card__container'})
    for ind, org in enumerate(orgs):
        print("DEBUG: Scraped detail for {}/{} orgs".format(ind, len(orgs)), end="\r")
        link = org.find('a', attrs={'class': 'organization-card__link'})
        org_name = org['aria-label']
        org_link = ROOT_URL + link['href']
        response = requests.get(org_link)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        
        tech_tags = soup.findAll('li', attrs={
            'class': 'organization__tag organization__tag--technology'
        }
        )
        technologies = []
        for tag in tech_tags:
            technologies.append(tag.text.replace(" ", ''))
        
        topic_tags = soup.findAll('li', attrs={
            'class': 'organization__tag organization__tag--category'
        }
        )
        category = topic_tags[0].text.replace('\n','')
        
        topic_tags = soup.findAll('li', attrs={
            'class': 'organization__tag organization__tag--topic'
        }
        )
        topics = []
        for tag in topic_tags:
            topics.append(tag.text)
        
        all_org_data[create_key(org_name)] = {
            "name": org_name,
            "technologies": ' | '.join(technologies),
            "topics": ' | '.join(topics),
            "category": category
        }
    return all_org_data

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
    else:
        url = NEW_FORMAT_LINK.replace(TO_REPLACE, str(year))

    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    if year < NEW_FORMAT_DIVISION:
        return scrape_before_2016(soup)
    else:
        return scrape_from_2016(soup)

if __name__ == "__main__":
    scrape_year_data(2015)
    scrape_year_data(2019)