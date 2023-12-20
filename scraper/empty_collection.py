import db

reset = {
    "listings": True,
    "listings-raw": False,
    "urls": False,
    "locations": False,
    "search-terms": False,
}

def main():
    for collection_name, should_reset in reset.items():
        if should_reset and collection_name in db.c:
            db.c[collection_name].delete_many({})


if __name__ == "__main__":
    any_to_reset = False
    for collection_name, should_reset in reset.items():
        if should_reset:
            any_to_reset = True
            break

    if not any_to_reset:
        print("No collections to reset. Exiting...")
        exit()

    print("THIS WILL EMPTY THE SPECIFIED COLLECTION:")
    for collection_name, should_reset in reset.items():
        if should_reset:
            print("\t- " + collection_name)

    print("Are you sure you want to continue? This is IRREVERSIBLE (y/n)") 
    if input() != "y":
        print("Exiting...")
        exit()

    print("Emptying collections...")
    main()