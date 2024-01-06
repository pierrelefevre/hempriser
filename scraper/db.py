import pymongo as mongo
import datetime
from dotenv import load_dotenv
import os


# Collection dict
c = {}

load_dotenv()


def setup():
    print("Setting up database connection...")

    required_env_vars = [
        "MONGO_USER",
        "MONGO_SECRET",
        "MONGO_HOST",
    ]

    missing_some = False
    for var in required_env_vars:
        if var not in os.environ:
            print(f"Missing {var} in .env")
            missing_some = True

    if missing_some:
        exit()

    db_user = os.getenv("MONGO_USER")
    db_pass = os.getenv("MONGO_SECRET")

    client = mongo.MongoClient(
        f"mongodb://{db_user}:{db_pass}@{os.getenv('MONGO_HOST')}"
    )

    client.server_info()

    db = client["bostadspriser"]

    global c
    c["listings-raw"] = db["listings-raw"]
    c["listings"] = db["listings"]
    c["listings-live"] = db["listings-live"]
    c["listings-live-clean"] = db["listings-live-clean"]
    c["urls"] = db["urls"]
    c["urls-live"] = db["urls-live"]
    c["locations"] = db["locations"]
    c["search-terms"] = db["search-terms"]
    c["inflation"] = db["inflation"]
    c["status"] = db["status"]


setup()

# Write


def write_raw_listing(listing: dict, live=False):
    collection = "listings-raw"
    if live:
        collection = "listings-live"

    listing["createdAt"] = datetime.datetime.now()
    listing["status"] = "pending"

    try:
        c[collection].insert_one(listing)
    except mongo.errors.BulkWriteError as e:
        pass
    except mongo.errors.DuplicateKeyError:
        pass


def write_raw_listing_coord(url: str, coord: dict, live=False):
    collection = "listings-raw"
    if live:
        collection = "listings-live"

    try:
        c[collection].update_one(
            {"url": url},
            {"$set": {"coord": coord}},
        )
    except mongo.errors.BulkWriteError as e:
        pass
    except mongo.errors.DuplicateKeyError:
        pass


def write_listings(listings: dict, live=False):
    for listing in listings:
        listing["createdAt"] = datetime.datetime.now()

    collection = "listings"
    if live:
        collection = "listings-live-clean"
    try:
        c[collection].insert_many(listings, ordered=False)
    except mongo.errors.BulkWriteError as e:
        pass
    except mongo.errors.DuplicateKeyError:
        pass


def write_locations(locations: list):
    for location in locations:
        location["createdAt"] = datetime.datetime.now()
        location["status"] = "pending"

    try:
        c["locations"].insert_many(locations, ordered=False)
    except mongo.errors.BulkWriteError as e:
        pass
    except mongo.errors.DuplicateKeyError:
        pass


def write_urls(urls: list, live=False):
    write = []
    for url in urls:
        write.append(
            {
                "url": url,
                "createdAt": datetime.datetime.now(),
                "status": "pending",
            }
        )

    try:
        if live:
            c["urls-live"].insert_many(write, ordered=False)
        else:
            c["urls"].insert_many(write, ordered=False)
    except mongo.errors.BulkWriteError as e:
        pass
    except mongo.errors.DuplicateKeyError:
        pass


def write_inflations(inflations: list):
    try:
        c["inflation"].insert_many(inflations, ordered=False)
    except mongo.errors.BulkWriteError as e:
        pass
    except mongo.errors.DuplicateKeyError:
        pass


def write_prediction_live(url: str, prediction: dict):
    c["listings-live-clean"].update_one(
        {"url": url},
        {"$set": {"prediction": prediction}},
    )


def reset_all_predictions():
    c["listings-live-clean"].update_many(
        {},
        {"$unset": {"prediction": ""}},
    )


def marks_urls_as_done(urls: list, live=False):
    collection = "urls"
    if live:
        collection = "urls-live"
    c[collection].update_many(
        {"url": {"$in": urls}},
        {"$set": {"status": "done"}},
    )


def mark_locations_as_done(ids: list):
    c["locations"].update_many(
        {"id": {"$in": ids}},
        {"$set": {"status": "done"}},
    )


def mark_locations_last_scraped(ids: list):
    c["locations"].update_many(
        {"id": {"$in": ids}},
        {"$set": {"lastScraped": datetime.datetime.now()}},
    )


def mark_raw_listing_as_missing_fields(url: str, live=False):
    collection = "listings-raw"
    if live:
        collection = "listings-live"

    c[collection].update_one(
        {"url": url},
        {"$set": {"status": "missingFields"}},
    )


def mark_raw_listing_as_failed(url: str, live=False):
    collection = "listings-raw"
    if live:
        collection = "listings-live"

    c[collection].update_one(
        {"url": url},
        {"$set": {"status": "failed"}},
    )


def mark_raw_listings_as_done(urls: list, live=False):
    collection = "listings-raw"
    if live:
        collection = "listings-live"

    c[collection].update_many(
        {"url": {"$in": urls}},
        {"$set": {"status": "done"}},
    )


def mark_search_terms_as_done(terms: list):
    c["search-terms"].update_many(
        {"term": {"$in": terms}},
        {"$set": {"status": "done"}},
    )


def write_search_terms(terms: list):
    try:
        c["search-terms"].insert_many(terms, ordered=False)
    except mongo.errors.BulkWriteError as e:
        pass
    except mongo.errors.DuplicateKeyError:
        pass


def update_status(hostname: str, timestamp: datetime.datetime, status: str):
    c["status"].update_one(
        {"hostname": hostname},
        {"$set": {"timestamp": timestamp, "status": status}},
        upsert=True,
    )


# Read
def get_listings(n: int = 0, page: int = 0):
    res = c["listings"].find({}).skip(n * page).limit(n)
    return list(res)


def get_pending_locations(n: int = 0, page: int = 0, random: bool = False):
    if random:
        res = c["locations"].aggregate(
            [
                {"$match": {"status": "pending"}},
                {"$sample": {"size": n}},
            ]
        )
        return list(res)

    res = (
        c["locations"]
        .find({"status": "pending"})
        .sort("createdAt", -1)
        .skip(n * page)
        .limit(n)
    )
    return list(res)


# Get locations which do not have lastScraped, or where lastScraped is older than 1 day
def get_next_live_locations(n=10):
    res = (
        c["locations"]
        .find(
            {
                "$or": [
                    {"lastScraped": None},
                    {
                        "lastScraped": {
                            "$lt": datetime.datetime.now() - datetime.timedelta(days=1)
                        }
                    },
                ]
            }
        )
        .limit(n)
    )
    return list(res)


def get_unpredicted_live_listings(n=10):
    res = (
        c["listings-live-clean"]
        .find(
            {
                "$or": [
                    {"prediction": None},
                    {"prediction": {"$exists": False}},
                ]
            }
        )
        .limit(n)
    )
    return list(res)


def get_pending_urls(n: int = 0, page: int = 0, random: bool = False, live=False):
    collection = "urls"
    if live:
        collection = "urls-live"

    if random:
        res = c[collection].aggregate(
            [
                {"$match": {"status": "pending"}},
                {"$sample": {"size": n}},
            ]
        )
        return list(res)

    res = (
        c[collection]
        .find({"status": "pending"})
        .sort("createdAt", -1)
        .skip(n * page)
        .limit(n)
    )
    return list(res)


def get_pending_raw_listings(
    n: int = 0, page: int = 0, random: bool = False, live=False
):
    collection = "listings-raw"
    if live:
        collection = "listings-live"

    if random:
        res = c[collection].aggregate(
            [
                {"$match": {"status": "pending"}},
                {"$sample": {"size": n}},
            ]
        )
        return list(res)

    res = (
        c[collection].find({"status": "pending"})
        # .sort("createdAt", -1)
        # .skip(n * page)
        .limit(n)
    )
    return list(res)


def get_pending_listings_without_coord(n: int = 0, page: int = 0, random: bool = False):
    if random:
        res = c["listings-raw"].aggregate(
            [
                {"$match": {"coord": {"$exists": False}}},
                {"$sample": {"size": n}},
            ]
        )
        return list(res)

    res = (
        c["listings-raw"]
        .find({"coord": {"$exists": False}})
        .sort("createdAt", -1)
        .skip(n * page)
        .limit(n)
    )

    return list(res)


def get_pending_search_terms(n: int = 500):
    res = c["search-terms"].aggregate(
        [
            {"$match": {"status": "pending"}},
            {"$sample": {"size": n}},
        ]
    )
    return list(res)


def get_inflation(year: int, month: int):
    if month < 10:
        key = f"{year}M0{month}"
    else:
        key = f"{year}M{month}"

    res = c["inflation"].find_one({"id": key})
    return res


def get_latest_inflation():
    now = datetime.datetime.now()

    # do 100 iterations to find the latest inflation, if not found, return None
    for i in range(100):
        res = get_inflation(now.year, now.month)
        if res is not None:
            return res
        else:
            now = now - datetime.timedelta(days=30)


# Patch


def patch_locations():
    print("Patching locations")
    c["locations"].update_many(
        {"createdAt": None},
        {"$set": {"createdAt": datetime.datetime.now()}},
    )

    c["locations"].update_many(
        {"status": None},
        {"$set": {"status": "pending"}},
    )


if __name__ == "__main__":
    print("WARNING: You are running db.py directly. Please confirm [Enter]")
    input()
    patch_locations()
