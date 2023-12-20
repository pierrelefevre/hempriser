import os
import pymongo as mongo
from dotenv import load_dotenv

c = {}


def setup():
    load_dotenv()
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

    db = client["bostadspriser"]

    global c
    c["listings-raw"] = db["listings-raw"]
    c["listings"] = db["listings"]
    c["urls"] = db["urls"]
    c["locations"] = db["locations"]
    c["search-terms"] = db["search-terms"]
    c["inflation"] = db["inflation"]


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
        c["listings-raw"]
        .find({"status": "pending"})
        .sort("createdAt", -1)
        .skip(n * page)
        .limit(n)
    )
    return list(res)


def get_inflation(key: str):
    c["inflation"].find_one({"key": key})
