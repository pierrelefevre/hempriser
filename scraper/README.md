# Getting started with the scraper


### 1. Ensure MongoDB is running and can be accessed by the scraper using the required envs
All the collections and required indexes will be created automatically.

If you are trying locally, you can use the following docker-compose file to start a MongoDB instance.

(Make sure you have a `data` folder in the same directory as the `docker-compose.yml` file)

```yaml
version: '3.1'

services:
  mongodb:
    image: mongo
    environment:
      MONGO_INITDB_ROOT_USERNAME: user
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - ./data:/data/db
    ports:
      - 27017:27017
```

And then run it using `docker-compose up -d`.

Then create a file called `.env` in the scraper directory with the following content:

```bash
MONGO_USER=user
MONGO_SECRET=password
MONGO_HOST=localhost:27017
```

### 2. Add the SCB inflation data to the database
```python
python scb.py
```

### 3. Add the search-terms to the database
```python
python generate_search_terms.py
```

### 4. Run the scraper

The scraper can be run in mutliple ways, see below.

#### 4.1. Run the scraper manually

The data is fetched in a pipeline, with MongoDB keeping track on what needs to be done and what has been done. The scraper will run until all the search-terms have been processed.

The flow of the data is: Search term -> Location IDs -> URLs -> Raw Listing (unparsed) -> Parsed Listing -> Parsed Listing with geocoding (coordinates)

This means you will need to run all the separate scripts in order to get the data from the search terms to the parsed listings with coordinates.

1. Fetch the location IDs from the search terms
```python
python get_ids.py
```

2. Fetch the URLs from the location IDs
```python
python get_urls.py
```

3. Fetch the raw listings from the URLs
```python
python get_listings_raw.py
```

4. Parse the raw listings
```python
python get_listings_clean.py
```

#### 4.2. Run the scraper using the bash script

The bash script will run all the parts of the scraper. Since every part will wait if there isn't anything to do, it is safe to run the in parallel.

```bash
./start-all.sh <number of processes>
```

### 4.3. Run the scraper using systemd

The scraper takes A LOT of time to go through the data, so it is convinent to run it as a service. This can be installed on mutliple computers to speed up the process.

The service is called `bostadspriser.service` and can be started using `systemctl start bostadspriser.service`. The service will run the bash script `start-all.sh` with the number of processes specified in the `ExecStart` command. 

So you need to edit the `bostadspriser.service` file to specify the number of processes you want to run.

```bash
sudo setup-service.sh
```

