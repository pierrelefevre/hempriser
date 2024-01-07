import os
import pickle
import json
import db

import pandas as pd


# dict of {"name": name, {"model": model, "scaler": scaler, "results": results}}
models = {}


def load_models():
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


def choose_model(transformed_params):
    if "askingPrice" in transformed_params:
        with_asking_price_models = []
        for name, model in models.items():
            if "with-askingPrice" in name:
                with_asking_price_models.append(model)

        # sort by trainedAt
        with_asking_price_models.sort(key=lambda x: x["metadata"]["trainedAt"])

        return with_asking_price_models[-1]
    else:
        without_asking_price_models = []
        for name, model in models.items():
            if "without-askingPrice" in name:
                without_asking_price_models.append(model)

        # sort by trainedAt
        without_asking_price_models.sort(key=lambda x: x["metadata"]["trainedAt"])

        return without_asking_price_models[-1]


def get_live_listing_prediction(url: str):
    # Check if the listing is in the database, otherwise it is treated as a non-existent listing
    return db.get_live_listing_by_url(url)


def get_live_listings(page: int, page_size: int):
    return db.get_live_listings(page, page_size)
