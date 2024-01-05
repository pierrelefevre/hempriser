import sys

import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR

# List of regressors to try
regressors = {
    "Linear Regression": {"model": LinearRegression(), "params": {}},
    "Ridge Regression": {
        "model": Ridge(),
        "params": {
            "alpha": [0.1, 1, 10, 100],
        },
    },
    "Lasso Regression": {
        "model": Lasso(),
        "params": {
            "alpha": [0.1, 1, 10, 100],
        },
    },
    "Random Forest": {
        "model": RandomForestRegressor(),
        # Random Forest was too slow to run with GridSearchCV, so it will use the default parameters
        "params": {},
    },
    "Gradient Boosting": {
        "model": GradientBoostingRegressor(),
        "params": {
            "n_estimators": [10, 100],
            "max_depth": [3, 10],
            "min_samples_split": [2, 5],
        },
    },
}

# List of setups to use, each will result in a model that can be used for a specific purpose
# "features" will be a list of features to use, every feature that is not here will be dropped
setups = {
    "bostadspriser-without-askingPrice": {
        "features": [
            "fee",
            "livingArea",
            "rooms",
            "runningCosts",
            "hasElevator",
            "hasBalcony",
            "lat",
            "long",
            "cpi",
            "hasHousingCooperative",
            "isPlot",
            "isWinterLeisureHouse",
            "isApartment",
            "isFarmWithForest",
            "isHouse",
            "isRowHouse",
            "isPairHouse",
            "isPairTerracedRowHouse",
            "isTerracedHouse",
            "isFarmWithoutForest",
            "isLeisureHouse",
            "isOtherHousingForm",
            "isFarmWithAgriculture",
            "age",
            "sinceLastRenovation",
            "soldYear",
            "soldMonth",
        ],
        "target": "finalPrice",
    },
    "bostadspriser-with-askingPrice": {
        "features": [
            "fee",
            "livingArea",
            "rooms",
            "runningCosts",
            "hasElevator",
            "hasBalcony",
            "lat",
            "long",
            "cpi",
            "hasHousingCooperative",
            "isPlot",
            "isWinterLeisureHouse",
            "isApartment",
            "isFarmWithForest",
            "isHouse",
            "isRowHouse",
            "isPairHouse",
            "isPairTerracedRowHouse",
            "isTerracedHouse",
            "isFarmWithoutForest",
            "isLeisureHouse",
            "isOtherHousingForm",
            "isFarmWithAgriculture",
            "age",
            "sinceLastRenovation",
            "soldYear",
            "soldMonth",
            "askingPrice",
        ],
        "target": "finalPrice",
    },
}


def print_same_line(text):
    print(text, end="")
    sys.stdout.flush()


def get_test_train_split(dataset, features, target):
    y = dataset[target]
    X = dataset[features]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test


def evaluate_model(
    name, regressor_name, model, params, X_train, y_train, X_test, y_test
):
    print(f"[{name}] Evaluating " + regressor_name + "... ")

    print(f"[{name}] Grid searching... ")
    gs_model = GridSearchCV(
        estimator=model,
        param_grid=params,
        scoring="neg_mean_squared_error",
        cv=5,
        n_jobs=-1,
    )

    print(f"[{name}] Fitting model... ")
    gs_model.fit(X_train, y_train)

    print(f"[{name}] Best params (" + str(gs_model.best_params_) + ") ")

    print(f"[{name}] Predicting... ")
    y_pred = gs_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print(f"[{name}] MSE: " + str(mse) + ", RMSE: " + str(rmse) + ", R^2: " + str(r2))
    return gs_model, mse, rmse, r2


# def train, takes in a test train split and returns the best model and its results
def train(name, X_train, y_train, X_test, y_test):
    results = {}
    for regressor_name, regressor in regressors.items():
        model, mse, rmse, r2 = evaluate_model(
            name,
            regressor_name,
            regressor["model"],
            regressor["params"],
            X_train,
            y_train,
            X_test,
            y_test,
        )
        results[regressor_name] = {"model": model, "MSE": mse, "RMSE": rmse, "R^2": r2}

    return results


def main():
    print("Loading data...")
    file_path = "../dataset/listings.parquet"
    data = pd.read_parquet(file_path)

    # print how many rows and columns
    print("Rows: " + str(data.shape[0]) + ", Columns: " + str(data.shape[1]))

    print("Preprocessing...")
    # Dropping NaN values will drop every row without coordinates
    data = data.dropna()

    # Sort column names alphabetically to make it easier to use the model from the API later (it will also sort alphabetically)
    data = data.reindex(sorted(data.columns), axis=1)

    for name, setup in setups.items():
        print(f"[{name}] Getting test train split...")
        X_train, X_test, y_train, y_test = get_test_train_split(
            data, setup["features"], setup["target"]
        )

        print(f"[{name}] Training...")
        results = train(
            name,
            X_train,
            y_train,
            X_test,
            y_test,
        )

        best_model = results_df.index[0]
        print(f"[{name}] Best model: " + best_model)

        # Save model
        print("Saving model...")
        with open("../models/main.pkl", "wb") as f:
            pickle.dump(results[best_model]["model"], f)

        # Save results
        results_df = pd.DataFrame(results)
        results_df = results_df.drop("model", axis=0)
        results_df = results_df.transpose()
        results_df = results_df.sort_values(by=["RMSE"])
        results_df.to_csv("../models/main_results.csv")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
