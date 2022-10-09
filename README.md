# federated-graphql
A federated GraphQL application using FastAPI, Ariadne and Apollo Router

### How to run in docker

    docker-compsoe up

### How can I run wihout docker

* run individual apps with uviron like as follows:
  * uviron user_service:app --port 8000
  * uvicorn product_service:app --port 8001
  * uvicorn reviews_service:app --port 8002
* cd apollo-router and download apollo-router mentioned at: https://medium.com/@adeshpandey/you-should-write-your-next-app-backend-in-graphql-why-2ac11d8ed8df
  * Change the url for the services in supergraph-schema.graphql
    * like for user_service:8000 -> localhost:8000
    * for product_service -> localhost:8001
    * for review_service:8000 -> localhost:8002
  * ./router --dev --supergraph supergraph-schema.graphql

Cheers!