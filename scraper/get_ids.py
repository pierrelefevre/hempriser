import hemnet
import db

while True:
    print("Getting pending search terms...")
    terms = db.get_pending_search_terms()

    done = []
    for item in terms:
        try:
            locs = hemnet.get_location_ids()
            curr = item["term"]

            print(f"Found {len(locs)} locations for {curr}")
            if len(locs) > 0:
                db.write_locations(locs)
                print(f"Wrote {len(locs)} locations for {curr}")

            done.append(curr)

        except Exception as e:
            print(e)
            print(f"Failed to get locations for {curr}")

    print(f"Marking {len(done)} search terms as done...")
    db.mark_search_terms_as_done(done)
