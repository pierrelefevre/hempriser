import hemnet
import db
import time


def main():
    i = 0
    while True:
        locations = db.get_next_live_locations(n=100)
        if len(locations) == 0:
            print("No more locations to process. Sleeping for 60 seconds.")
            time.sleep(60)
            continue

        print(f"Processing {len(locations)} locations, at iteration {i}")

        for location in locations:
            len_location = 0
            for hemnet_page in range(1, 51):
                urls = hemnet.get_urls(location["id"], hemnet_page, live=True)
                len_location += len(urls)
                if len(urls) == 0:
                    print(
                        f"Done with {location['fullName']} ({location['id']}) - Found {len_location} listings"
                    )
                    break

                db.write_urls(urls=urls, live=True)
            db.mark_locations_last_scraped([location["id"]])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
