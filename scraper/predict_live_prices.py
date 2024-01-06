import os
import pickle
import json
import pandas as pd
import db
import time
import transform
import cerberus
import datetime

models = {}


def load_models():
    print("Loading models")
    for name in os.listdir("../models"):
        print(f"Loading model {name}")
        model = pickle.load(open(f"../models/{name}/model.pkl", "rb"))
        scaler = pickle.load(open(f"../models/{name}/scaler.pkl", "rb"))
        results = pd.read_csv(f"../models/{name}/results.csv", index_col=0)
        metadata = json.load(open(f"../models/{name}/metadata.json", "r"))
        models[name] = {
            "name": name,
            "model": model,
            "scaler": scaler,
            "results": results,
            "metadata": metadata,
        }


def predict(body, model):
    # Make sure all required parameters are present using cerberus
    schema = {
        "housingForm": {
            "type": "string",
            "allowed": transform.allowed_housing_forms,
        },
        "livingArea": {"type": "number", "min": 0},
        "rooms": {"type": "number", "min": 0},
        "constructionYear": {"type": "number", "min": 0},
        "renovationYear": {"type": "number", "min": 0},
        "askingPrice": {"type": "number", "min": 0},
        "fee": {"type": "number", "min": 0},
        "runningCosts": {"type": "number", "min": 0},
        "hasElevator": {"type": "boolean"},
        "hasBalcony": {"type": "boolean"},
        "hasHousingCooperative": {"type": "boolean"},
        "lat": {"type": "number"},
        "long": {"type": "number"},
        # optional askingPrice
    }

    v = cerberus.Validator(schema, allow_unknown=True)
    if not v.validate(body):
        print("Failed to validate body")
        return None

    # Parse soldAt to a datetime object ISO format
    try:
        body["soldAt"] = datetime.datetime.now()
    except Exception as e:
        print("Failed to parse soldAt, " + e)
        return None

    # Transform the parameters to the format used in the model'
    try:
        transformed_params = transform.transform_params(body)
    except Exception as e:
        print("Failed to transform params, " + e)
        return None

    # Convert to df and sort alphabetically
    transformed_params_df = pd.DataFrame([transformed_params])
    transformed_params_df = transformed_params_df.reindex(
        sorted(transformed_params_df.columns), axis=1
    )

    # Scale the data
    transformed_params = model["scaler"].transform(transformed_params_df)

    # Extract the values
    transformed_params_values = transformed_params[0]

    # Predict
    prediction = model["model"].predict([transformed_params_values])
    return {
        "prediction": prediction[0],
        "model": model["name"],
    }


# db.reset_all_predictions()
load_models()
total = 0

while True:
    listings = db.get_unpredicted_live_listings()

    if len(listings) == 0:
        print("No more listings to predict. Sleeping for 60 seconds...")
        time.sleep(60)

    for listing in listings:
        if "lat" not in listing.keys() or "long" not in listing.keys():
            print("Skipping listing without lat/long")
            continue
        prediction = {}
        for model_name in models:
            model = models[model_name]["model"]
            scaler = models[model_name]["scaler"]
            metadata = models[model_name]["metadata"]

            newListing = listing.copy()
            if "without" in model_name:
                del newListing["askingPrice"]

            if "housingCooperative" in listing.keys():
                newListing["hasHousingCooperative"] = True
                del newListing["housingCooperative"]
            else:
                newListing["hasHousingCooperative"] = False

            del newListing["streetAddress"]
            del newListing["thumbnail"]
            del newListing["_id"]
            del newListing["createdAt"]
            del newListing["url"]
            del newListing["id"]

            prediction[model_name] = predict(newListing, models[model_name])
            print(f"Predicted {model_name} to {prediction[model_name]}")

        db.write_prediction_live(listing["url"], prediction)
        total += 1
        print(f"Predicted {listing['url']}, total predicted {total}")
