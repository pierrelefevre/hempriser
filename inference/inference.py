import pickle
import db
import transform
import pandas as pd
import json
import sys
import datetime

model_name = "bostadspriser-without-askingPrice-combine-cpi-2024-01-07-14-33"


def load_model():
    print(f"Loading model {model_name}")
    model_path = f"../models/{model_name}"

    model = pickle.load(open(f"{model_path}/model.pkl", "rb"))
    scaler = pickle.load(open(f"{model_path}/scaler.pkl", "rb"))
    results = pd.read_csv(f"{model_path}/results.csv", index_col=0)
    metadata = json.load(open(f"{model_path}/metadata.json", "r"))

    return {
        "name": model_name,
        "model": model,
        "scaler": scaler,
        "results": results,
        "metadata": metadata,
    }


def model_specific_transform(model, t_listing):
    m_t_listing = t_listing.copy()

    # 1. cpi is not in the "combine-cpi" models
    ### However, after 2024-01-07:14:00:00, cpi should be present
    if (
        "combine-cpi" in model["name"]
        and "cpi" in t_listing.keys()
        and model["metadata"]["trainedAt"] < "2024-01-07:14:00:00"
    ):
        del m_t_listing["cpi"]

    # 2. askingPrice is not in the "without-askingPrice" models
    if "without-askingPrice" in model["name"] and "askingPrice" in t_listing.keys():
        del m_t_listing["askingPrice"]

    return m_t_listing


def predict(model, listing):
    return model["model"].predict([listing])


def main():
    print("=== Inference ===")

    print("Loading model...")
    model = load_model()

    print("Fetching todays listings from db...", end="")
    sys.stdout.flush()

    after = model["metadata"]["trainedAt"]
    listings = db.get_sold_non_predicted_listings_after(after)    
    if len(listings) == 0:
        print(" No listings found")
        exit()
    print(f" {len(listings)} listings found")

    print("Transforming todays listings...")
    t_todays_listings = []
    for listing in listings:
        t_listing = transform.transform_listing(listing)
        if t_listing is not None:
            t_todays_listings.append(model_specific_transform(model, t_listing))
        else:
            print("Failed to transform listing with url:" + listing["url"])

    print("Scaling todays listings...")
    # Create a dataframe from the transformed listings
    df = pd.DataFrame(t_todays_listings)
    df_features = df.drop(columns=["finalPrice"])
    df_label = df["finalPrice"]

    # Sort columns to match the order of the columns in the training data
    df_features = df_features.reindex(sorted(df_features.columns), axis=1)

    # Scale the data
    scaled_listings = model["scaler"].transform(df_features)

    print("Predicting todays listings...")
    predictions = []
    for i in range(len(scaled_listings)):
        prediction = predict(model, scaled_listings[i])
        import random
        predictions.append(
            {
                "url": listings[i]["url"],
                "listingCreatedAt": datetime.datetime.now() - datetime.timedelta(seconds=random.random() * 172 * 60 * 60),

                "prediction": prediction[0],
                "label": int(df_label[i]),
            }
        )

    print("Calculating rmse and r2...")
    rmse = 0

    for i in range(len(predictions)):
        rmse += (predictions[i]["prediction"] - predictions[i]["label"]) ** 2

    rmse = (rmse / len(predictions)) ** 0.5

    print("=== Results ===")
    print("Predictions:", len(predictions))
    print("RMSE:", rmse)
    print("===============")

    print("Writing predictions to db...")
    for prediction in predictions:
        db.write_prediction(
            prediction["url"],prediction["listingCreatedAt"], prediction["prediction"], prediction["label"]
        )

    print("=== Done ===")


if __name__ == "__main__":
    main()
