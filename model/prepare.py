import pandas as pd
import db
import transform


def main():
    # Load data from collection 'listings' and create a large parquet file from it
    print("Loading data from database...")

    print("Preparing the data...")
    transformed = []
    page = 0
    pageSize = 10000

    while True:
        listings = db.get_listings(pageSize, page)
        if len(listings) == 0:
            print("No more listings to load")
            break
        print(
            f"Loaded {len(listings)} listings (page {page} total {(page + 1) * pageSize})"
        )

        for listing in listings:
            res = transform.transform_listing(listing)
            if not res:
                continue

            transformed.append(res)

        print("Transformed " + str(len(transformed)) + " listings, saving...")
        df = pd.DataFrame(transformed)
        if page == 0:
            df.to_parquet("../dataset/listings.parquet", engine="fastparquet")
        else:
            df.to_parquet(
                "../dataset/listings.parquet", engine="fastparquet", append=True
            )

        page += 1

    print("Done preparing the data")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
