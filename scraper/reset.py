import db

reset = {
    "listings": False,
    "listings-raw": False,
    "urls": False,
    "locations": False,
    "search-terms": True,
}

for collection_name, should_reset in reset.items():
    if should_reset and collection_name in db.c:
        fil = {"status": {"$ne": "pending"}}
        write = {"status": "pending"}

        db.c[collection_name].update_many(fil, {"$set": write})
