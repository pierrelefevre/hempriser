import json
import flask
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)


def read_file():
    with open("listings.json", "r") as f:
        data = json.load(f)
    return data


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

    data = read_file()

    return flask.jsonify(data[skip : skip + limit])


@app.route("/predict", methods=["POST"])
def predict():
    return 42


app.run(host="0.0.0.0", port=8080)
