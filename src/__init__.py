import datetime

from const import START_YEAR
from scraper import scrape_year_data
from utils import (load_year_data, process_all_year_data, save_csv,
                   update_readme)


def main():
    now = datetime.datetime.now()
    all_year_data = {}
    for year in range(START_YEAR, now.year):
        year_data = load_year_data(year)
        if year_data is None:
            year_data = scrape_year_data(year)
            save_csv(year_data, year)
        all_year_data[year] = year_data
    all_year_data = process_all_year_data(all_year_data, now.year)
    save_csv(all_year_data)
    update_readme(all_year_data)

if __name__ == "__main__":
    main()