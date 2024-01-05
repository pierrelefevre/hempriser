import os
import json
import flask
import pickle
import cerberus
import datetime
import transform

import pandas as pd

from flask_cors import CORS


print("Bostadspriser API")


app = flask.Flask(__name__)
CORS(app)

print("Loading data")

listings = []
locations = []

# dict of {"name": name, {"model": model, "scaler": scaler, "results": results}}
models = {}

print("Loading models")
for name in os.listdir("models"):
    print(f"Loading model {name}")
    model = pickle.load(open(f"models/{name}/model.pkl", "rb"))
    scaler = pickle.load(open(f"models/{name}/scaler.pkl", "rb"))
    results = pd.read_csv(f"models/{name}/results.csv", index_col=0)
    metadata = json.load(open(f"models/{name}/metadata.json", "r"))
    models[name] = {
        "name": name,
        "model": model,
        "scaler": scaler,
        "results": results,
        "metadata": metadata,
    }

with open("listings.json", "r") as f:
    listings = json.load(f)

with open("locations.json", "r") as f:
    locations = json.load(f)


def choose_model(transformed_params):
    if "askingPrice" in transformed_params:
        return models["bostadspriser-with-askingPrice"]

    return models["bostadspriser-without-askingPrice"]


@app.route("/", methods=["GET"])
def home():
    return "Bostadspriser API"


@app.route("/healthz", methods=["GET"])
def healthz():
    return "OK"


@app.route("/models", methods=["GET"])
def get_models():
    models_dto = []
    for model in models.values():
        models_dto.append(
            {
                "name": model["name"],
                "results": model["results"].to_dict(),
                "metadata": model["metadata"],
            }
        )

    return flask.jsonify(models_dto)


@app.route("/listings", methods=["GET"])
def get_listings():
    args = flask.request.args

    skip = int(args.get("skip", 0))
    limit = int(args.get("limit", 10))

    return flask.jsonify(listings[skip : skip + limit])


@app.route("/locations", methods=["GET"])
def get_locations():
    return flask.jsonify(locations)


@app.route("/predict", methods=["POST"])
def predict():
    body = flask.request.json

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
        "soldAt": {"type": "string"},
        # optional askingPrice
        "askingPrice": {"type": "number", "min": 0},
    }

    v = cerberus.Validator(schema, allow_unknown=True)
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

    # Chose model depending on the parameters
    model = choose_model(transformed_params.keys())

    print("model chosen: " + model["name"])

    # Convert to df and sort alphabetically
    transformed_params_df = pd.DataFrame([transformed_params])

    print("before sort")
    print(transformed_params_df.columns)

    transformed_params_df = transformed_params_df.reindex(sorted(transformed_params_df.columns), axis=1)

    print("after sort")
    print(transformed_params_df.columns)

    # Scale the data
    transformed_params = model["scaler"].transform(transformed_params_df)

    # Extract the values
    transformed_params_values = transformed_params[0]

    # Predict
    prediction = model["model"].predict([transformed_params_values])
    return flask.jsonify(
        {
            "prediction": prediction[0],
            "model": model["name"],
        }
    )


print("Starting server")

app.run(host="0.0.0.0", port=8080)
