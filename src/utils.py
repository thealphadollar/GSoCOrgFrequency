import os
from csv import DictReader, DictWriter

from tomark import Tomark

from const import CHARATER_WHITELIST, START_YEAR

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
        year_data = {}
        with open(os.path.join(DATA_DIR, '{}.csv'.format(str(year))), 'r') as f:
            reader = DictReader(f)
            for row in reader:
                year_data[create_key(row['name'])] = row
        return year_data
    except FileNotFoundError:
        return None

def save_csv(data_dict, year="allyears"):
    print(data_dict)
    with open(os.path.join(DATA_DIR, '{}.csv'.format(str(year))), 'w') as f:
        values = list(data_dict.values())
        writer = DictWriter(f, values[0].keys())
        writer.writeheader()
        writer.writerows(values)

def process_all_year_data(all_year_data, end_year):
    processed_data = {}
    for year in range(START_YEAR, end_year):
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
                if cur_year_data[key].get('technologies', ''):
                    technologies = processed_data[key]['Technologies'].split(" | ")
                    technologies.extend(cur_year_data[key].get('technologies', '').split(" | "))
                    technologies = list(set(technologies))
                    technologies.remove('')
                    processed_data[key]['Technologies'] = ' | '.join(technologies)
                if cur_year_data[key].get('topics', ''):
                    topics = processed_data[key]['Topics'].split(" | ")
                    topics.extend(cur_year_data[key].get('topics', '').split(" | "))
                    topics = list(set(topics))
                    topics.remove('')
                    processed_data[key]['Topics'] = ' | '.join(topics)
                if cur_year_data[key].get('category', ''):
                    if processed_data[key]['Categories']:
                        processed_data[key]['Categories'] = processed_data[key]['Categories'] + " | " + cur_year_data[key].get('category', '')
                    else:
                        processed_data[key]['Categories'] = cur_year_data[key].get('category', '')
                processed_data[key]['Latest Year'] = year
    return processed_data

def update_readme(all_year_data):
    all_year_data = list(all_year_data.values())
    for i in range(len(all_year_data)):
        for key in all_year_data[i].keys():
            all_year_data[i][key] = str(all_year_data[i][key]).replace(" | ", ", ")
            all_year_data[i][key] = str(all_year_data[i][key]).replace("|", " ")
    all_year_data.sort(key=lambda x: x['Name'].lower())
    markdown_table = Tomark.table(all_year_data)
    with open(os.path.join(ROOT_DIR, 'Organisation Data.md'), 'w') as f:
        f.writelines(markdown_table)

def create_key(org_name):
    return ''.join(filter(CHARATER_WHITELIST.__contains__, org_name.lower()))