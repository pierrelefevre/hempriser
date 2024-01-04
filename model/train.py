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


def print_same_line(text):
    print(text, end="")
    sys.stdout.flush()


def train():
    print("Loading data...")
    file_path = '../dataset/listings.parquet'
    data = pd.read_parquet(file_path)

    # drop "askingPrice"
    data = data.drop('askingPrice', axis=1)

    # print how many rows and columns
    print("Rows: " + str(data.shape[0]) + ", Columns: " + str(data.shape[1]))

    print("Preprocessing...")
    data = data.dropna()

    print("Selecting target variable and features...")
    y = data['finalPrice']
    X = data.drop('finalPrice', axis=1)

    print("Splitting dataset into training and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    print("Normalizing...")
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # List of regressors to try
    regressors = {
        'Linear Regression': {
            'model': LinearRegression(),
            'params': {}
        },
        'Ridge Regression': {
            'model': Ridge(),
            'params': {
                'alpha': [0.1, 1, 10, 100],
            }
        },
        'Lasso Regression': {
            'model': Lasso(),
            'params': {
                'alpha': [0.1, 1, 10, 100],
            }
        },
        'Random Forest': {
            'model': RandomForestRegressor(),
            # Random Forest was too slow to run with GridSearchCV, so it will use the default parameters
            'params': {}
        },
        'Gradient Boosting': {
            'model': GradientBoostingRegressor(),
            'params': {
                'n_estimators': [10, 100],
                'max_depth': [3, 10],
                'min_samples_split': [2, 5],
            }
        },
    }

    def evaluate_model(model, params, X_train, y_train, X_test, y_test):
        print_same_line("Evaluating " + name + "... Finding params... ")

        grid_search = GridSearchCV(estimator=model, param_grid=params,
                                   scoring='neg_mean_squared_error', cv=5, n_jobs=-1)
        print_same_line("Fitting... ")
        grid_search.fit(X_train, y_train)
        print_same_line("(" + str(grid_search.best_params_) + ") ")

        print_same_line("Predicting... ")
        y_pred = grid_search.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        print(" MSE: " + str(mse) + ", RMSE: " +
              str(rmse) + ", R^2: " + str(r2))
        return model, mse, rmse, r2

    print("Evaluating models...")
    results = {}
    for name, regressor in regressors.items():
        model, mse, rmse, r2 = evaluate_model(
            regressor['model'], regressor['params'], X_train, y_train, X_test, y_test)
        results[name] = {'model': model, 'MSE': mse, 'RMSE': rmse, 'R^2': r2}

    # Print result as a matrix in pandas, sorted by RMSE
    print("Results:")
    results_df = pd.DataFrame(results)
    results_df = results_df.drop('model', axis=0)
    results_df = results_df.transpose()
    results_df = results_df.sort_values(by=['RMSE'])
    print(results_df)

    print("Saving model...")
    best_model = results_df.index[0]
    with open('../models/main.pkl', 'wb') as f:
        pickle.dump(results[best_model]['model'], f)


if __name__ == '__main__':
    try:
        train()
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
