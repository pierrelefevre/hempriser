import db
import datetime
import helpers
import pandas as pd

# Below are the steps to transform a listing from the raw format to the format used in the model
# This is copied from the model/transform.py file
#
# 1. Add the closest inflation data: cpi
# 2. Convert "housingCooperative" to 'hasHousingCooperative'
# 3. Convert "housingForm" to a one-hot encoding
#       3.1 Allowed values:
#       - Tomt
#       - Vinterbonat fritidshus
#       - Lägenhet
#       - Gård med skogsbruk
#       - Villa
#       - Kedjehus
#       - Parhus
#       - Par-/kedje-/radhus
#       - Radhus
#       - Gård utan jordbruk
#       - Fritidshus
#       - Gård/skog
#       - Övrig
#       - Fritidsboende
#       - Gård med jordbruk
# 4. Convert "constructionYear" to "age"
# 5. Convert "renovationYear" to "sinceLastRenovation"
# 6. Convert "soldAt" to "soldYear" and "soldMonth"

allowed_housing_forms = [
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


def get_cpi(date):
    inflation = db.get_inflation(date.year, date.month)
    if inflation is not None:
        return float(inflation["cpiDecided"])

    latest = db.get_latest_inflation()
    if latest is None:
        return None

    return float(latest["cpiDecided"])


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


def transform_params(params):
    """
    This method should mimic the method in the model/transform.py file.

    It should take the parameters from the API request and transform them as a listing is transformed in the model.
    """

    t_params = {}

    # 0. Insert all values that should be kept as is
    t_params["livingArea"] = params["livingArea"]
    t_params["rooms"] = params["rooms"]
    if "askingPrice" in params:
        t_params["askingPrice"] = params["askingPrice"]
    t_params["hasElevator"] = params["hasElevator"]
    t_params["hasBalcony"] = params["hasBalcony"]
    t_params["lat"] = params["lat"]
    t_params["long"] = params["long"]
    t_params["fee"] = params["fee"]
    t_params["runningCosts"] = params["runningCosts"]

    # 1. Get the closest inflation data
    cpi = get_cpi(params["soldAt"])
    if cpi is None:
        raise Exception("No CPI data found for the given date")

    t_params["cpi"] = cpi

    # 2. Convert "housingCooperative" to 'hasHousingCooperative'
    if "hasHousingCooperative" in params:
        t_params["hasHousingCooperative"] = params["hasHousingCooperative"]
    elif "housingCooperative" in params:
        t_params["hasHousingCooperative"] = params["housingCooperative"] is not None

    # 3. Convert "housingForm" to a one-hot encoding
    for name, one_hot_encoding in convert_housing_form_to_one_hot_encoding(
        params["housingForm"]
    ).items():
        t_params[name] = one_hot_encoding

    # 4. Convert "constructionYear" to "age"
    year_now = datetime.datetime.now().year
    t_params["age"] = year_now - params["constructionYear"]

    # 5. Convert "renovationYear" to "sinceLastRenovation"
    t_params["sinceLastRenovation"] = year_now - params["renovationYear"]

    # 6. Convert "soldAt" to "soldYear" and "soldMonth"
    t_params["soldYear"] = params["soldAt"].year
    t_params["soldMonth"] = params["soldAt"].month

    # Chose model depending on the parameters
    model, t_params = helpers.choose_model(t_params)

    # Convert to df and sort alphabetically
    t_params_df = pd.DataFrame([t_params])
    t_params_df = t_params_df.reindex(sorted(t_params_df.columns), axis=1)

    # Scale the data
    t_params = model["scaler"].transform(t_params_df)

    # Extract the values
    t_params_values = t_params[0]

    return t_params_values, model
