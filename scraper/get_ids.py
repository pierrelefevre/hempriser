import hemnet
from collections import deque
import db
import time


def iterate_strings(chars):
    queue = deque(chars)

    while queue:
        current_string = queue.popleft()
        yield current_string

        for char in chars:
            queue.append(current_string + char)


chars = "abcdefghijklmnopqrstuvwxyz "

string_generator = iterate_strings(chars)

terms = []
while True:
    curr = next(string_generator)

    if len(curr) > 5:
        break

    if len(terms) > 200_000:
        db.write_search_terms(terms)
        terms = []
        print(f"Wrote 100k terms for {curr}")

    terms.append({"term": curr})

# locs = hemnet.get_location_ids(curr)

# print(f"Found {len(locs)} locations for {curr}")
# if len(locs) > 0:
#     db.write_locations(locs)
#     print(f"Wrote {len(locs)} locations for {curr}")
#     time.sleep(1)
