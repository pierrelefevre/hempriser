import os
import pymongo as mongo
import datetime
from dotenv import load_dotenv

# Collection dict
c = {}

load_dotenv()


def setup():
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
    c["listings-live-clean"] = db["listings-live-clean"]
    c["listings"] = db["listings"]
    c["inflation"] = db["inflation"]
    c["predictions"] = db["predictions"]


setup()


def get_predictions():
    predictions = c["predictions"].find({}, {"_id": 0})
    return list(predictions)

def get_live_listings(page: int, page_size: int):
    live_listings = (
        c["listings-live-clean"]
        .find({}, {"_id": 0})
        .skip(page * page_size)
        .limit(page_size)
    )

    return list(live_listings)


def get_live_listing_by_url(url: str):
    live_listing = c["listings-live-clean"].find_one({"url": url}, {"_id": 0})
    return live_listing


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
