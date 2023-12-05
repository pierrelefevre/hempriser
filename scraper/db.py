import pymongo as mongo
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# collection dict
c = {}


def setup():
    print("Setting up database connection...")

    db_user = os.getenv("MONGO_USER")
    db_pass = os.getenv("MONGO_SECRET")

    client = mongo.MongoClient(
        f"mongodb://{db_user}:{db_pass}@{os.getenv('MONGO_HOST')}"
    )

    db = client["bostadspriser"]

    listings_raw_collection = db["listings-raw"]
    listings_collection = db["listings"]
    urls_collection = db["urls"]
    locations_collection = db["locations"]
    search_terms_collection = db["search-terms"]

    global c
    c["listings-raw"] = listings_raw_collection
    c["listings"] = listings_collection
    c["urls"] = urls_collection
    c["locations"] = locations_collection
    c["search-terms"] = search_terms_collection


setup()

# Write


def write_raw_listing(listing: dict):
    listing["createdAt"] = datetime.datetime.now()
    listing["status"] = "pending"

    try:
        c["listings-raw"].insert_one(listing)
    except mongo.errors.BulkWriteError as e:
        pass
    except mongo.errors.DuplicateKeyError:
        pass


def write_listing(listings: dict):
    for listing in listings:
        listing["createdAt"] = datetime.datetime.now()

    try:
        c["listings"].insert_many(listings, ordered=False)
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


def write_urls(urls: list):
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
        c["urls"].insert_many(write, ordered=False)
    except mongo.errors.BulkWriteError as e:
        pass
    except mongo.errors.DuplicateKeyError:
        pass


def marks_urls_as_done(urls: list):
    c["urls"].update_many(
        {"url": {"$in": urls}},
        {"$set": {"status": "done"}},
    )


def marks_locations_as_done(ids: list):
    c["locations"].update_many(
        {"id": {"$in": ids}},
        {"$set": {"status": "done"}},
    )


def marks_raw_listings_as_done(urls: list):
    c["locations"].update_many(
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


# Read


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


def get_pending_urls(n: int = 0, page: int = 0, random: bool = False):
    if random:
        res = c["urls"].aggregate(
            [
                {"$match": {"status": "pending"}},
                {"$sample": {"size": n}},
            ]
        )
        return list(res)

    res = (
        c["urls"]
        .find({"status": "pending"})
        .sort("createdAt", -1)
        .skip(n * page)
        .limit(n)
    )
    return list(res)


def get_pending_raw_listings(n: int = 0, page: int = 0, random: bool = False):
    if random:
        res = c["listings_raw"].aggregate(
            [
                {"$match": {"status": "pending"}},
                {"$sample": {"size": n}},
            ]
        )
        return list(res)

    res = (
        c["locations_raw"]
        .find({"status": "pending"})
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
