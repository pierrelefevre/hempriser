import json
import flask
import pickle
import cerberus
import datetime

from flask_cors import CORS

import transform

print("Bostadspriser API")


app = flask.Flask(__name__)
CORS(app)

print("Loading data")


listings = []
locations = []

# Temporary solution until we have some better way of selecting the model we want to use
model = pickle.load(open("../models/main.pkl", "rb"))


with open("listings.json", "r") as f:
    listings = json.load(f)

with open("locations.json", "r") as f:
    locations = json.load(f)


@app.route("/", methods=["GET"])
def home():
    return "Bostadspriser API"


@app.route("/healthz", methods=["GET"])
def healthz():
    return "OK"


@app.route("/listings", methods=["GET"])
def get_listings():
    args = flask.request.args

    skip = int(args.get("skip", 0))
    limit = int(args.get("limit", 10))

    return flask.jsonify(listings[skip: skip + limit])


@app.route("/locations", methods=["GET"])
def get_locations():
    return flask.jsonify(locations)


@app.route("/predict", methods=["POST"])
def predict():
    body = flask.request.json

    # Predict can be either a URL to Hemnet, where the parameters will be scraped
    # Or a JSON object with the parameters already scraped

    if "url" in body:
        return flask.jsonify({"error": "Not implemented"}), 501
    else:
        # Make sure all required parameters are present using cerberus
        schema = {
            "housingForm": {"type": "string", "allowed": transform.allowed_housing_forms},
            "livingArea": {"type": "number", "min": 0},
            "rooms": {"type": "number", "min": 0},
            "constructionYear": {"type": "number", "min": 0},
            "renovationYear": {"type": "number", "min": 0},
            "soldAt": {"type": "string"},
            "askingPrice": {"type": "number", "min": 0},
            "fee": {"type": "number", "min": 0},
            "runningCosts": {"type": "number", "min": 0},
            "hasElevator": {"type": "boolean"},
            "hasBalcony": {"type": "boolean"},
            "hasHousingCooperative": {"type": "boolean"},

            # Coords
            "lat": {"type": "number"},
            "long": {"type": "number"},

            # These might be removed if we use coords instead, since coords are more precise and easier to learn for a model
            "district": {"type": "number", "min": 0},
            "municipality": {"type": "number", "min": 0},
            "city": {"type": "number", "min": 0},
            "county": {"type": "number", "min": 0},
        }

        v = cerberus.Validator(schema)
        if not v.validate(body):
            return flask.jsonify({"error": v.errors}), 400

        # Parse soldAt to a datetime object ISO format
        try:
            body["soldAt"] = datetime.datetime.fromisoformat(body["soldAt"])
        except Exception as e:
            return flask.jsonify({"error": str(e)}), 400

        # Transform the parameters to the format used in the model'
        try:
            transformed_params = transform.transform_params(body)
        except Exception as e:
            return flask.jsonify({"error": str(e)}), 400

        # Sort the parameters alphabetically by key, then extract the values
        transformed_params = [transformed_params[key]
                              for key in sorted(transformed_params.keys())]

        # Make the prediction
        prediction = model.predict([transformed_params])
        return flask.jsonify({"prediction": prediction[0]})


print("Starting server")

app.run(host="0.0.0.0", port=8080)
