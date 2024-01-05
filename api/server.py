import json
import flask
import cerberus
import datetime
import transform
import helpers

import pandas as pd

from flask_cors import CORS


print("Bostadspriser API")


app = flask.Flask(__name__)
CORS(app)

print("Loading data")

listings = []
locations = []


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


@app.route("/models", methods=["GET"])
def get_models():
    models_dto = []
    for model in helpers.models.values():
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

    skip = int(args.get("page", 0))
    limit = int(args.get("pageSize", 10))

    return helpers.get_live_listings(skip, limit)


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
    model = helpers.choose_model(transformed_params.keys())

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
