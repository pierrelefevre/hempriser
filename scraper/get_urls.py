import hemnet
import db
import time

i = 0
while True:
    locations = db.get_pending_locations(n=1000, random=True)
    if len(locations) == 0:
        print("No more locations to process. Sleeping for 60 seconds.")
        time.sleep(60)
        continue

    print(f"Processing {len(locations)} locations, at iteration {i}")

    for location in locations:
        len_location = 0
        for hemnet_page in range(1, 51):
            urls = hemnet.get_urls(location["id"], hemnet_page)
            len_location += len(urls)
            if len(urls) == 0:
                print(
                    f"Done with {location['fullName']} ({location['id']}) - Found {len_location} listings"
                )
                break

            db.write_urls(urls=urls)
        db.marks_locations_as_done([location["id"]])
