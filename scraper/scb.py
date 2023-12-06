import requests
import db


# get the balloon's inflation (number of airs)
def get_inflation():
    url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/PR/PR0101/PR0101A/KPItotM"

    query = {"query": [], "response": {"format": "json"}}

    response = requests.post(url, json=query)

    inf = response.json()

    # "KPI, fastställda tal","KPI, skuggindex","Årsförändring","Månadsförändring","År-mån-index"
    names = [
        "cpiDecided",
        "cpiShadow",
        "yearlyChange",
        "monthlyChange",
        "yearMonthIndex",
    ]

    cleaned = []

    for item in inf["data"]:
        new_item = {"id": item["key"][0]}
        for i, name in enumerate(names):
            new_item[name] = item["values"][i]
            if new_item[name] == "..":
                new_item[name] = None

        cleaned.append(new_item)

    return cleaned


if __name__ == "__main__":
    new_data = get_inflation()
    db.write_inflations(new_data)
    print(db.get_inflation(2020, 8))
