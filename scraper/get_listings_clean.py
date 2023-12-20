import db
import time
import locale


def clean_listing(listing_raw):
    output = {}

    output["url"] = listing_raw["url"]

    # prepare empty lists
    # output["district"] = []
    # output["images"] = []

    # loop through the json data
    base = listing_raw["props"]["pageProps"]["__APOLLO_STATE__"]
    for key, value in base.items():
        # Check if the key is a property listing
        try:
            if key.startswith("Location") and "type" in value.keys():
                if value["type"] == "MUNICIPALITY":
                    output["municipality"] = int(value["id"])

                if value["type"] == "COUNTY":
                    output["county"] = int(value["id"])

                if value["type"] == "DISTRICT" and "districts" not in output:
                    output["district"] = int(value["id"])

                if "city" not in output and (value["type"] == "CITY" or value["type"] == "POSTAL_CITY"):
                    output["city"] = int(value["id"])

                if value["type"] == "COUNTRY":
                    if value["fullName"] != "Sverige" and value["fullName"] != "Sweden":
                        raise Exception("Not in Sweden")

            if key.startswith("SoldPropertyListing"):
                output["id"] = int(value["id"])
                if "sellingPrice" in value.keys() and value["sellingPrice"] is not None:
                    output["finalPrice"] = value["sellingPrice"]["amount"]
                else:
                    raise Exception("Missing sellingPrice")

                if "askingPrice" in value.keys() and value["askingPrice"] is not None:
                    output["askingPrice"] = value["askingPrice"]["amount"]
                else:
                    output["askingPrice"] = output["finalPrice"]
                    

                if "fee" in value.keys() and value["fee"] is not None:
                    output["fee"] = value["fee"]["amount"]
                else:
                    output["fee"] = 0

                output["livingArea"] = value["livingArea"]

                if "numberOfRooms" in value.keys():
                    output["rooms"] = value["numberOfRooms"]
                else:
                    output["rooms"] = 1

                # format legacyConstructionYear to int from str
                    
                # not renovated: 1953
                # renovated: 1953/2010
                    
                if "legacyConstructionYear" in value.keys() and value["legacyConstructionYear"] is not None:
                    try:
                        split = value["legacyConstructionYear"].split("/")
                        if len(split) == 1:
                            output["constructionYear"] = int(split[0])
                            output["renovationYear"] = int(split[0])
                        else:
                            output["constructionYear"] = int(split[0])
                            output["renovationYear"] = int(split[1])
                    except Exception:
                        pass

                

                if "runningCosts" in value.keys() and value["runningCosts"] is not None:
                    output["runningCosts"] = value["runningCosts"]["amount"]
                else:
                    output["runningCosts"] = 0

                output["housingForm"] = value["housingForm"]["name"]

                if "housingCooperative" in value.keys() and value["housingCooperative"] is not None:

                    # check if housingCooperative is a string or a dict
                    if isinstance(value["housingCooperative"], str):
                        output["housingCooperative"] = value["housingCooperative"]
                    else:
                        output["housingCooperative"] = value["housingCooperative"]["name"]
                else:
                    output["housingCooperative"] = None

                # find all amenities
                output["hasElevator"] = False
                output["hasBalcony"] = False
                for amenity in value["relevantAmenities"]:
                    if amenity["kind"] == "ELEVATOR":
                        output["hasElevator"] = amenity["isAvailable"]

                    if amenity["kind"] == "BALCONY":
                        output["hasBalcony"] = amenity["isAvailable"]

                # find all images
                # sample:
                #
                # "images({\"limit\":300})": {
                #             "__typename": "ListingImageResults",
                #             "images": [
                #                 {
                #                     "__typename": "ListingImage",
                #                     "url({\"format\":\"ITEMGALLERY_CUT\"})": "https://bilder.hemnet.se/images/itemgallery_cut/a7/8f/a78fc0fa6e971d3e3df18760ea808fa1.jpg",
                #                     "url({\"format\":\"ITEMGALLERY_PORTRAIT_CUT\"})": "https://bilder.hemnet.se/images/itemgallery_portrait_cut/a7/8f/a78fc0fa6e971d3e3df18760ea808fa1.jpg",
                #                     "url({\"format\":\"WIDTH1024\"})": "https://bilder.hemnet.se/images/1024x/a7/8f/a78fc0fa6e971d3e3df18760ea808fa1.jpg",
                #                     "originalWidth": 2048,
                #                     "originalHeight": 1365,
                #                     "labels": [
                #                     ]
                #                 },

                # for key2, value2 in value.items():
                #     if key2.startswith("images") and "images" in value2.keys():
                #         for image in value2["images"]:
                #             for imageKey in image.keys():
                #                 if "url" in imageKey and "WIDTH" in imageKey:
                #                     output["images"].append(image[imageKey])
                #                     break

        except Exception as e:
            print("Failed to clean listing, details: " + str(e))
            continue
    
        
    # if missing district, set it to the municipality
    if "district" not in output:
        output["district"] = output["municipality"]



    # Make sure we have all the required fields

    required_fields = [
        "id",
        "url",
        "finalPrice",
        "askingPrice",
        "fee",
        "livingArea",
        "rooms",
        "constructionYear",
        "runningCosts",
        "housingForm",
        "housingCooperative",
        "hasElevator",
        "hasBalcony",
        "district",
        "municipality",
        "county",
        "city",
    ]

    for field in required_fields:
        if field not in output:
            raise Exception(f"Missing required field: {field}")    
    
    
    return output


def clean_all():
    while True:
        raw_listings = db.get_pending_raw_listings(n=5000, random=False)
        if len(raw_listings) == 0:
            print("No more listings to clean. Sleeping for 60 seconds...")
            time.sleep(60)
            continue

        print(f"Cleaning {len(raw_listings)} listings...")

        cleaned = []
        err_due_to_missing_field = 0
        for raw_listing in raw_listings:
            try:
                listing = clean_listing(raw_listing)
                cleaned.append(listing)
            except Exception as e:
                if "Missing required field" in str(e):
                    err_due_to_missing_field += 1
                    db.mark_raw_listing_as_missing_fields(raw_listing["url"])
                    continue

                print("Failed to clean listing ("+str(raw_listing["url"])+"), details: " + str(e))
                db.mark_raw_listing_as_failed(raw_listing["url"])
                continue
        db.write_listings(cleaned)
        db.mark_raw_listings_as_done([listing["url"] for listing in cleaned])

        print(f"Done cleaning {len(cleaned)} listings. {err_due_to_missing_field} listings failed due to missing fields.")


def clean_mock():
    import json

    with open("../mock/listing.json") as f:
        json_data = json.loads(f.read())

    res = clean_listing(json_data)
    for key, value in res.items():
        print(key, value)


if __name__ == "__main__":
    try:
        # clean_mock()
        clean_all()
    except KeyboardInterrupt:
        print("Exiting...")
        exit()