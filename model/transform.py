import datetime
import db

# Below are the steps to transform a listing from the raw format to the format used in the model
# This is useful when the same transformation needs to be done on the API side as on the model side
# 1. Remove unwanted fields
# 2. Add the closest inflation data
# 3. Convert 'housingCooperative' to 'hasHousingCooperative', if it exists, is not None and is not empty
# 4. Convert "housingForm" to a one-hot encoding
# 5. Convert "constructionYear" to "age"
# 6. Convert "renovationYear" to "sinceLastRenovation"
# 7. Convert "soldAt" to "soldYear" and "soldMonth"


allowed_types = [
    "Tomt",
    "Vinterbonat fritidshus",
    "Lägenhet",
    "Gård med skogsbruk",
    "Villa",
    "Kedjehus",
    "Parhus",
    "Par-/kedje-/radhus",
    "Radhus",
    "Gård utan jordbruk",
    "Fritidshus",
    "Gård/skog",
    "Övrig",
    "Fritidsboende",
    "Gård med jordbruk",
]


def get_closest_cpi(date: datetime.datetime):
    return db.get_inflation(date.year, date.month)


def convert_housing_form_to_one_hot_encoding(housing_form):
    one_hot_encoded_housing_form = {
        "isPlot": housing_form == "Tomt",
        "isWinterLeisureHouse": housing_form == "Vinterbonat fritidshus",
        "isApartment": housing_form == "Lägenhet",
        "isFarmWithForest": housing_form == "Gård med skogsbruk",
        "isHouse": housing_form == "Villa",
        "isRowHouse": housing_form == "Kedjehus",
        "isPairHouse": housing_form == "Parhus",
        "isPairTerracedRowHouse": housing_form == "Par-/kedje-/radhus",
        "isTerracedHouse": housing_form == "Radhus",
        "isFarmWithoutForest": housing_form == "Gård utan jordbruk",
        "isLeisureHouse": housing_form == "Fritidshus"
        or housing_form == "Fritidsboende",
        "isFarmWithForest": housing_form == "Gård/skog",
        "isOtherHousingForm": housing_form == "Övrig",
        "isFarmWithAgriculture": housing_form == "Gård med jordbruk",
    }

    return one_hot_encoded_housing_form


def transform_listing(listing):
    # Remove unwanted fields
    if "_id" in listing.keys():
        del listing["_id"]
    if "url" in listing.keys():
        del listing["url"]
    if "id" in listing.keys():
        del listing["id"]
    if "createdAt" in listing.keys():
        del listing["createdAt"]

    # Add the closest inflation data
    inflation = get_closest_cpi(listing["soldAt"])
    if inflation is None:
        return None

    listing["cpi"] = inflation["cpiDecided"]

    # Convert 'housingCooperative' to 'hasHousingCooperative', if it exists, is not None and is not empty
    if (
        "housingCooperative" in listing.keys()
        and listing["housingCooperative"] is not None
        and listing["housingCooperative"] != ""
    ):
        listing["hasHousingCooperative"] = True
    else:
        listing["hasHousingCooperative"] = False
    if "housingCooperative" in listing.keys():
        del listing["housingCooperative"]

    # Convert "housingForm" to a one-hot encoding
    for name, one_hot_encoding in convert_housing_form_to_one_hot_encoding(
        listing["housingForm"]
    ).items():
        listing[name] = one_hot_encoding
    del listing["housingForm"]

    # Convert "constructionYear" to "age"
    year_now = datetime.datetime.now().year
    listing["age"] = year_now - listing["constructionYear"]
    del listing["constructionYear"]

    # Convert "renovationYear" to "sinceLastRenovation"
    if "renovationYear" in listing.keys():
        listing["sinceLastRenovation"] = year_now - listing["renovationYear"]
        del listing["renovationYear"]
    else:
        listing["sinceLastRenovation"] = listing["age"]

    # Convert "soldAt" to "soldYear" and "soldMonth"
    listing["soldYear"] = listing["soldAt"].year
    listing["soldMonth"] = listing["soldAt"].month
    del listing["soldAt"]

    # Remove "district", "municipality", "county" and "city", since we use coordinates instead
    del listing["district"]
    del listing["municipality"]
    del listing["county"]
    del listing["city"]

    return listing


if __name__ == "__main__":
    mock = {
        "district": 939989,
        "municipality": 17912,
        "county": 17746,
        "city": 19696,
        "finalPrice": 2975000,
        "askingPrice": 2975000,
        "fee": 3000,
        "livingArea": 155,
        "rooms": 5,
        "constructionYear": 1983,
        "housingForm": "Lägenhet",
        "runningCosts": 39503,
        "hasElevator": False,
        "hasBalcony": False,
        "housingCooperative": "Någon Bostadsrättsförening",
        "lat": 59.04411147817049,
        "long": 17.308288753630684,
        "soldAt": datetime.datetime(2016, 10, 26, 0, 0, 0, 0),
        "createdAt": datetime.datetime(2024, 1, 4, 16, 56, 14, 536000),
    }

    import json

    print(json.dumps(transform_listing(mock), indent=4))
