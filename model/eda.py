import db
import datetime
import json
import re
import clean

example_listing = {}


def parse_date(date: str) -> datetime.datetime:
    # Såld 19 november 2020

    regex = r"Såld (\d+) (\w+) (\d+)"
    match = re.match(regex, date)
    if match:
        day = int(match.group(1))
        month = match.group(2)
        year = int(match.group(3))
        return datetime.datetime(year, month, day)
    else:
        print("Could not parse date: ", date)
        return None


def get_closest_inflation(date: datetime.datetime):
    # 1980M01
    year = date.year
    month = date.month
    id = f"{year}M{month}"

    return db.get_inflation(id)


def main():
    db.setup()
    listings = db.get_pending_raw_listings(n=10)

    for listing in listings:
        print(listing["props"]["pageProps"].keys())

    exit()
    clean.clean_listing(listings[0])


if __name__ == "__main__":
    main()
