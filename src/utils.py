import os

from const import CHARATER_WHITELIST, START_YEAR
from csv import DictReader, DictWriter
from tomark import Tomark


DATA_DIR = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)),
    '..',
    'data')

ROOT_DIR = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)),
    '..')

def load_year_data(year):
    try:
        with open(os.path.join(DATA_DIR, '{}.txt'.format(str(year))), 'r') as f:
            return DictReader(f)
    except FileNotFoundError:
        return None

def save_csv(data_dict, year="allyears"):
    with open(os.path.join(DATA_DIR, '{}.txt'.format(str(year))), 'r') as f:
        writer = DictWriter(f, data_dict.keys())
        writer.writeheader()
        writer.writerows(data_dict)

def process_all_year_data(all_year_data, end_year):
    processed_data = {}
    for year in range(START_YEAR, end_year+1):
        cur_year_data = all_year_data[year]
        for key in cur_year_data.keys():
            if processed_data.get(key, None) is None:
                processed_data[key] = {}
                processed_data[key]['Name'] = cur_year_data[key]['name']
                processed_data[key]['Count'] = 1
                processed_data[key]['Technologies'] = cur_year_data[key].get('technologies', '')
                processed_data[key]['Topics'] = cur_year_data[key].get('topics', '')
                processed_data[key]['Categories'] = cur_year_data[key].get('category', '')
                processed_data[key]['Latest Year'] = year
            else:
                processed_data[key]['Count'] += 1
                technologies = processed_data[key]['Technologies'].split(" | ").extend(cur_year_data[key].get('technologies', '').split(" | "))
                processed_data[key]['Technologies'] = ' | '.join(list(set(technologies)))
                topics = processed_data[key]['Topics'].split(" | ").extend(cur_year_data[key].get('topics', '').split(" | "))
                processed_data[key]['Topics'] = ' | '.join(list(set(topics)))
                if cur_year_data[key].get('category', ''):
                    processed_data[key]['Categories'] = processed_data[key]['Categories'] + " | " + cur_year_data[key].get('category', '')
                processed_data[key]['Latest Year'] = year
    return processed_data

def update_readme(all_year_data):
    markdown_table = Tomark.table(all_year_data.values())
    with open(os.path.join(ROOT_DIR, 'Organisation Data.md', 'w')) as f:
        f.writelines(markdown_table)

def create_key(org_name):
    return ''.join(filter(CHARATER_WHITELIST.__contains__, org_name.lower()))