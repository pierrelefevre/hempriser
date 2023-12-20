import db

reset = {
    "listings": False,
    "listings-raw": True,
    "urls": False,
    "locations": False,
    "search-terms": False,
}

def main():
    for collection_name, should_reset in reset.items():
        if should_reset and collection_name in db.c:
            fil = {"status": {"$ne": "pending"}}
            write = {"status": "pending"}

            db.c[collection_name].update_many(fil, {"$set": write})

if __name__ == "__main__":
    print("This will reset all of the documents in the specified collections to 'pending':")
    for collection_name, should_reset in reset.items():
        if should_reset:
            print("\t- " + collection_name)

    print("Are you sure you want to continue? This is IRREVERSIBLE (y/n)")
    if input() != "y":
        print("Exiting...")
        exit()

    print("Resetting collections...")
    main()