import json
import flask
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


@app.route("/listings", methods=["GET"])
def get_listings():
    args = flask.request.args

    skip = int(args.get("skip", 0))
    limit = int(args.get("limit", 10))

    return flask.jsonify(listings[skip : skip + limit])


@app.route("/locations", methods=["GET"])
def get_locations():
    return flask.jsonify(locations)


@app.route
@app.route("/predict", methods=["POST"])
def predict():
    return 42


print("Starting server")

app.run(host="0.0.0.0", port=8080)
