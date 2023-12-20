import db
import time


def clean_listing(json_data):
    print(json_data.keys())
    output = {}

    # prepare empty lists
    # output["districts"] = []
    # output["images"] = []

    # loop through the json data
    base = json_data["props"]["pageProps"]["__APOLLO_STATE__"]
    for key, value in base.items():
        # Check if the key is a property listing

        if key.startswith("Location") and "type" in value.keys():
            if value["type"] == "MUNICIPALITY":
                output["municipality"] = value["fullName"]

            if value["type"] == "COUNTY":
                output["county"] = value["fullName"]

            if value["type"] == "DISTRICT" and "districts" in output:
                output["districts"] = value["fullName"]

            if value["type"] == "CITY":
                output["city"] = value["fullName"]

            if value["type"] == "STREET":
                output["street"] = value["fullName"]

            if value["type"] == "POSTAL_CITY":
                output["postalCity"] = value["fullName"]

            if value["type"] == "COUNTRY":
                output["country"] = value["fullName"]

        if key.startswith("ActivePropertyListing"):
            output["id"] = value["id"]
            output["title"] = value["title"]
            output["askingPrice"] = value["askingPrice"]["amount"]
            output["squareMeterPrice"] = value["squareMeterPrice"]["amount"]
            output["fee"] = value["fee"]["amount"]
            output["livingArea"] = value["livingArea"]
            output["rooms"] = value["numberOfRooms"]

            # format legacyConstructionYear to int from str
            try:
                output["constructionYear"] = int(value["legacyConstructionYear"])
            except ValueError:
                pass

            output["isForeclosure"] = value["isForeclosure"]
            output["isNewConstruction"] = value["isNewConstruction"]
            output["runningCosts"] = value["runningCosts"]["amount"]
            output["housingForm"] = value["housingForm"]["name"]
            output["closestWaterDistanceMeters"] = value["closestWaterDistanceMeters"]
            output["timesViewed"] = value["timesViewed"]
            output["postCode"] = value["postCode"]
            output["housingCooperative"] = value["housingCooperative"]["name"]

            for amenity in value["relevantAmenities"]:
                if amenity["kind"] == "ELEVATOR":
                    output["hasElevator"] = amenity["isAvailable"]

                if amenity["kind"] == "BALCONY":
                    output["hasBalcony"] = amenity["isAvailable"]

    return output


def clean_all():
    while True:
        raw_listings = db.get_raw_listings(n=50000, random=True)
        if len(raw_listings) == 0:
            print("No more listings to clean. Sleeping for 60 seconds...")
            time.sleep(60)
            continue

        print(f"Cleaning {len(raw_listings)} listings...")

        cleaned = []
        for raw_listing in raw_listings:
            try:
                listing = clean_listing(raw_listing)
                cleaned.append(listing)
            except Exception as e:
                print("Failed to clean listing, details: " + str(e))
                continue
        db.write_listing(cleaned, raw=False)
        db.marks_raw_listings_as_done([listing["url"] for listing in cleaned])


def clean_mock():
    import json

    with open("../mock/listing.json") as f:
        json_data = json.loads(f.read())

    res = clean_listing(json_data)
    for key, value in res.items():
        print(key, value)


if __name__ == "__main__":
    clean_mock()
    # clean_all()
