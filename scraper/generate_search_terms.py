import db


def iterate_strings(chars, current_string="", max_length=None):
    if max_length is not None and len(current_string) >= max_length:
        return
    yield current_string
    for char in chars:
        yield from iterate_strings(chars, current_string + char, max_length)


chars = "abcdefghijklmnopqrstuvwxyz "
string_generator = iterate_strings(chars, max_length=6)

terms = []
reached_checkpoint = False
while True:
    curr = next(string_generator)

    if curr == "voqzs":
        reached_checkpoint = True

    if not reached_checkpoint:
        continue

    if len(curr) > 5:
        break

    if len(terms) > 200_000:
        db.write_search_terms(terms)
        terms = []
        print(f"Wrote 100k terms for {curr}")

    terms.append({"term": curr})
