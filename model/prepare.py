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
        print("Loaded " + str(len(listings)) + " listings (page " +
              str(page) + "), transforming...")

        page += 1

        for i, listing in enumerate(listings):
            res = transform.transform_listing(listing)
            if not res:
                continue

            transformed.append(res)

            if i % 10000 == 0:
                print("Done with " + str(i) +
                      " listings, appending to parquet...")
                df = pd.DataFrame(transformed)
                if i == 0:
                    df.to_parquet('../dataset/listings.parquet')
                else:
                    df.to_parquet(
                        '../dataset/listings.parquet', append=True)

    print("Done preparing the data")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
