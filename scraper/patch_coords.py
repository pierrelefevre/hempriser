import time
import db
import hemnet
import random
import platform
import datetime

i = 0

try:
    while True:
        db.update_status(platform.node(), datetime.datetime.now(), "running")
        raw_listings = db.get_pending_listings_without_coord(n=100, random=True)
        if len(raw_listings) == 0:
            print(
                "No more pending raw listings without coords. Sleeping for 60 seconds..."
            )
            time.sleep(60)

        timeout = 2

        print(f"Getting {len(raw_listings)} raw listings without coords...")
        for item in raw_listings:
            time.sleep(random.uniform(0, 1))
            url = item["url"]

            coords = hemnet.get_coords(url)
            if coords is None:
                print(f"Failed to get coords for url {url}")
                time.sleep(timeout)
                timeout = timeout * 2
                continue

            timeout = 2

            print(f"Done with {url} - iteration {i}")

            db.write_raw_listing_coord(url, coords)
            i += 1
except Exception as e:
    db.update_status(platform.node(), datetime.datetime.now(), "crashed")
    raise e
