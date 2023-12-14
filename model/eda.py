import db
import datetime
import json
import re


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


def clean_listing(listing):
    apollo = listing["props"]["pageProps"]["__APOLLO_STATE__"]

    # Get location IDs
    locations = []
    for k in apollo:
        if k.startswith("Location"):
            locations.append(apollo[k]["id"])

    print(locations)
    cleaned = {"location": locations}
    pass


def main():
    # read ../mock/listing.json
    with open("../mock/listing.json", "r") as f:
        listing = json.load(f)
    clean_listing(listing)
    db.setup()


if __name__ == "__main__":
    main()
