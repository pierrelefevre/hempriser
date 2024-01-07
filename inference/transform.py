import db
import datetime

def housing_one_hot(housing_form):
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
    t_listing = {}

    # 0. Insert all values that should be kept as is
    t_listing["finalPrice"] = listing["finalPrice"]
    t_listing["livingArea"] = listing["livingArea"]
    t_listing["rooms"] = listing["rooms"]
    if "askingPrice" in listing:
        t_listing["askingPrice"] = listing["askingPrice"]
    t_listing["hasElevator"] = listing["hasElevator"]
    t_listing["hasBalcony"] = listing["hasBalcony"]
    if "lat" in listing and "long" in listing:
        t_listing["lat"] = listing["lat"]
        t_listing["long"] = listing["long"]
    t_listing["fee"] = listing["fee"]
    t_listing["runningCosts"] = listing["runningCosts"]

    cpi = db.get_cpi(listing["soldAt"])
    if cpi is None:
        return None

    t_listing["cpi"] = cpi

    # Convert 'housingCooperative' to 'hasHousingCooperative', if it exists, is not None and is not empty
    if (
        "housingCooperative" in listing.keys()
        and listing["housingCooperative"] is not None
        and listing["housingCooperative"] != ""
    ):
        t_listing["hasHousingCooperative"] = True
    else:
        t_listing["hasHousingCooperative"] = False

    # Convert "housingForm" to a one-hot encoding
    for name, one_hot_encoding in housing_one_hot(listing["housingForm"]).items():
        t_listing[name] = one_hot_encoding

    # Convert "constructionYear" to "age"
    year_now = datetime.datetime.now().year
    t_listing["age"] = year_now - listing["constructionYear"]

    # Convert "renovationYear" to "sinceLastRenovation"
    if "renovationYear" in listing.keys():
        t_listing["sinceLastRenovation"] = year_now - listing["renovationYear"]
    else:
        t_listing["sinceLastRenovation"] = t_listing["age"]

    # Convert "soldAt" to "yearsSinceSold" (represented as a float since we know the exact date)
    t_listing["yearsSinceSold"] = (
        datetime.datetime.now() - listing["soldAt"]
    ).days / 365.25


    return t_listing