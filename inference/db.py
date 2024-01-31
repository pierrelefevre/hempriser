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
    c["listings"] = db["listings"]
    c["listings"].create_index("id", unique=True)
    c["listings"].create_index("url", unique=True)

    c["predictions"] = db["predictions"]

    c["inflation"] = db["inflation"]
    c["inflation"].create_index("id", unique=True)


setup()


def get_sold_non_predicted_listings_after(after: datetime.datetime):
    sold_listings = c["listings"].find(
        {
            "createdAt": {"$gte": after},
            "predicted": {"$in": [False, None]},
            "lat": {"$exists": True},
            "long": {"$exists": True},
        },
        {"_id": 0},
    )

    return list(sold_listings)


def write_prediction(url, listing_created_at, prediction, label):
    c["predictions"].insert_one(
        {
            "prediction": prediction,
            "label": label,
            "createdAt": datetime.datetime.now(),
            "listingCreatedAt": listing_created_at,
        },
    )

    c["listings"].update_one({"url": url}, {"$set": {"predicted": True}})


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


def get_cpi(date):
    inflation = get_inflation(date.year, date.month)
    if inflation is not None:
        return float(inflation["cpiDecided"])

    latest = get_latest_inflation()
    if latest is None:
        return None

    return float(latest["cpiDecided"])
