import pandas as pd

def load_dataset(name: str) -> pd.DataFrame:
    return pd.read_parquet(f"../dataset/{name}.parquet")


def main():
    listings = load_dataset("listings")

    print(listings.describe())
    print()
    print(listings.info())
    print()
    print(listings.head())

if __name__ == '__main__':
    main()
