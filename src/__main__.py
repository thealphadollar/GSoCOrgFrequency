import datetime

from const import START_YEAR
from scraper import scrape_year_data
from utils import (load_year_data, process_all_year_data, save_csv,
                   update_readme)


def main():
    now = datetime.datetime.now()
    all_year_data = {}
    print("INFO: Fetching from {} to {}".format(START_YEAR, now.year))
    this_year_data_released = True
    for year in range(START_YEAR, now.year+1):
        year_data = load_year_data(year)
        if year_data is None or not year_data:
            year_data = scrape_year_data(year)
            if year == now.year and not year_data:
                this_year_data_released = False
                continue
            save_csv(year_data, year)
            print("INFO: Scraped for {} and saved to CSV in docs folder".format(year))
        all_year_data[year] = year_data
    end_year = now.year if this_year_data_released else now.year - 1
    all_year_data = process_all_year_data(all_year_data, end_year)
    save_csv(all_year_data)
    print("INFO: All years data added to CSV in docs folder")
    update_readme(all_year_data, end_year)
    print("INFO: Updated README.md in docs folder with latest information!")

if __name__ == "__main__":
    main()