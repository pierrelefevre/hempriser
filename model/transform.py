import datetime
import db


def get_closest_cpi(date: datetime.datetime):
    return db.get_inflation(date.year, date.month)

def transform_listing(listing):
    # Remove unwanted fields
    if '_id' in listing.keys():
        del listing['_id']
    if 'url' in listing.keys():
        del listing['url']
    if 'id' in listing.keys():
        del listing['id']
    if 'createdAt' in listing.keys():
        del listing["createdAt"]

    # Add the closest inflation data
    inflation = get_closest_cpi(listing['soldAt'])
    if inflation is None:
        return None
    
    listing['cpi'] = inflation['cpiDecided']

    # Convert 'housingCooperative' to 'hasHousingCooperative', if it exists, is not None and is not empty
    if 'housingCooperative' in listing.keys() and listing['housingCooperative'] is not None and listing['housingCooperative'] != '':
        listing['hasHousingCooperative'] = True
    else:
        listing['hasHousingCooperative'] = False
    if 'housingCooperative' in listing.keys():
        del listing['housingCooperative']

    # Convert "housingForm" to a one-hot encoding
    # Query in MongoDB to find all unique values:
    #     {housingForm: {$nin: ["Gård med skogsbruk","Tomt","Gård med jordbruk","Kedjehus","Gård/skog","Gård utan jordbruk", "Lägenhet", "Par-/kedje-/radhus", "Övrig", "Parhus", "Fritidshus", "Vinterbonat fritidshus", "Fritidsboende", "Radhus", "Villa"]}}
    housing_form = listing['housingForm']
    listing['isApartment'] = housing_form == 'Lägenhet'
    listing['isHouse'] = housing_form == 'Villa'
    listing['isRowHouse'] = housing_form == 'Radhus' or 'radhus' in housing_form.lower()
    listing['isTerracedHouse'] = housing_form == 'Kedjehus'
    listing['isPairHouse'] = housing_form == 'Parhus'
    listing['isTenantOwner'] = housing_form == 'Bostadsrätt'
    listing['isLeisureHouse'] = housing_form == 'Fritidshus' or 'fritidshus' in housing_form.lower()
    listing['isFarm'] = housing_form == 'Gård' or 'gård' in housing_form.lower()
    listing['isForest'] = housing_form == 'Skog'
    listing['isPlot'] = housing_form == 'Tomt'
    listing['isOtherHousingForm'] = housing_form == 'Övrig' or 'övrig' in housing_form.lower()

    # Convert "constructionYear" to "age"
    year_now = datetime.datetime.now().year
    listing['age'] = year_now - listing['constructionYear']
    del listing['constructionYear']

    # Convert "renovationYear" to "sinceLastRenovation"
    if 'renovationYear' in listing.keys():
        listing['sinceLastRenovation'] = year_now - listing['renovationYear']
        del listing['renovationYear']
    else:
        listing['sinceLastRenovation'] = listing['age']

    # Convert "soldAt" to "soldYear" and "soldMonth"
    listing['soldYear'] = listing['soldAt'].year
    listing['soldMonth'] = listing['soldAt'].month
    del listing['soldAt']

    del listing['housingForm']

    return listing

if __name__ == "__main__":
    mock = {
        "district": 939989,
        "municipality": 17912,
        "county": 17746,
        "city": 19696,
        "finalPrice": 2975000,
        "askingPrice": 2975000,
        "fee": 3000,
        "livingArea": 155,
        "rooms": 5,
        "constructionYear": 1983,
        "housingForm": "Lägenhet",
        "runningCosts": 39503,
        "hasElevator": False,
        "hasBalcony": False,
        "lat": 59.04411147817049,
        "long": 17.308288753630684,
        "soldAt": datetime.datetime(2016, 10, 26, 0, 0, 0, 0),
        "createdAt": datetime.datetime(2024, 1, 4, 16, 56, 14, 536000)
    }

    import json
    print(json.dumps(transform_listing(mock), indent=4))