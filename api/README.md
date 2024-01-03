# bostadspriser/api
This API is intended to provide simple read access to the listings and post access to the prediction model.

## Endpoints
### GET /listings?skip=1&n=10
Returns a list of listings.

Parameters:
- skip: number of listings to skip
- n: number of listings to return


```sh 
curl https://api.bostad.åt.se/listings
```
```json
{
  "listings": [
    {
      "_id": {
        "$oid": "658d4620617d218c30c51422"
      },
      "url": "https://www.hemnet.se/salda/lagenhet-3rum-kviberg-goteborgs-kommun-soldathemsgatan-17-1291405",
      "district": 939969,
      "municipality": 17920,
      "county": 17755,
      "city": 18820,
      "id": 1291405,
      "finalPrice": 3205000,
      "askingPrice": 3200000,
      "fee": 4838,
      "livingArea": 80,
      "rooms": 3,
      "soldAt": {
        "$date": "2020-11-19T00:00:00.000Z"
      },
      "constructionYear": 2014,
      "renovationYear": 2014,
      "runningCosts": 1200,
      "housingForm": "Lägenhet",
      "housingCooperative": null,
      "hasElevator": true,
      "hasBalcony": true,
      "createdAt": {
        "$date": "2023-12-28T10:55:44.358Z"
      }
    },
    ...
  ]
}
```

### POST /predict
Predicts a house price based on the given parameters.

```sh
curl -X POST -H "Content-Type: application/json" -d \
'{
    "district": 939969,
    "municipality": 17920,
    "county": 17755,
    "city": 18820,
    "id": 1291405,
    "finalPrice": 3205000,
    "askingPrice": 3200000,
    "fee": 4838,
    "livingArea": 80,
    "rooms": 3,
    "soldAt": {
      "$date": "2020-11-19T00:00:00.000Z"
    },
    "constructionYear": 2014,
    "renovationYear": 2014,
    "runningCosts": 1200,
    "housingForm": "Lägenhet",
    "housingCooperative": null,
    "hasElevator": true,
    "hasBalcony": true,
}' https://api.bostad.åt.se/predict
```
```json
{
  "prediction": 3205000,
}
```
