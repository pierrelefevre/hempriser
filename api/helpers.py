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
        return models["bostadspriser-with-askingPrice"]

    return models["bostadspriser-without-askingPrice"]


def get_live_listings(page: int, page_size: int):
    return db.get_live_listings(page, page_size)