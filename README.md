# STELLA at MLentory

This repository consists of the core stella infrastructure required for the integration into MLentory.


## Getting Started

### Clone the repo 
Once you have cloned this repository, execute:
```
git clone --recurse-submodules https://github.com/stella-project/stella-app.git
```

If already cloned, update submodules with:

```
git submodule update --init --recursive
```

### Start the STELLA App

Run the following to start the STELLA app, its PostgreSQL database, and the mlentory_base and mlentory_experiment containers:

```
sudo docker compose -f docker-compose-mlentory.yml
```

### Initialize the STELLA database

```
sudo docker exec -it stella-app-1 flask seed-db
```

The stella web application is accessible at **http://localhost:8080**

In order to see the retrived results from the stella ranking point you can make use of the search interface

### Search Interface

To interact with the STELLA ranking endpoint via a UI:

```
cd search
sudo docker compose up -d
```

This will start the interface at **http://localhost:8081**

Enter a query to retrieve results. The results are presented in raw format as per the ranking endpoint — this is intentional to understand and debug the rankings.

### Accessing the STELLA App Ranking Endpoint

+ From outside the Docker container (e.g: from the host machine):
Use the following curl command to access the STELLA App's ranking API:

```
curl "http://localhost:8080/stella/api/v1/ranking?query=classification"
```

+ From within another Docker container (e.g: from mlentory_base):
Use the container name in the request instead of localhost:

```
curl "http://mlentory_base:5000/ranking?query=classification"
```

### Testing the `mlentory_base` system

To test the baseline system via the systems.py script, set the correct base_url depending on the execution context:

+ Running Locally (Outside Docker):

```
self.base_url = "http://localhost:8000/models/search_by_phrase"
```

+ Running Inside Docker Container:

```
self.base_url = "http://backend:8000/models/search_by_phrase"
```

### About the Systems

### mlentory_base

This component serves as the **baseline system** for MLentory within the STELLA integration. It acts as a wrapper around MLentory’s search backend, specifically targeting the `search_by_phrase` endpoint. It sends search queries to the backend, extracts model identifiers (model IDs) from the knowledge graph using the `db_identifier` property and returns only the relevant model IDs. 


