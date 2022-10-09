from ariadne import load_schema_from_path, QueryType
from ariadne.contrib.federation import FederatedObjectType, make_federated_schema
from ariadne.asgi import GraphQL
from fastapi import FastAPI


def get_product_list(*_):
    return "Product List"


type_defs = load_schema_from_path("gql/product.graphql")

query = QueryType()
product = FederatedObjectType("Product")


products = [
    {"upc": "1", "name": "Table", "price": 899, "weight": 100},
    {"upc": "2", "name": "Couch", "price": 1299, "weight": 1000},
    {"upc": "3", "name": "Chair", "price": 54, "weight": 50},
]


@query.field("topProducts")
def resolve_top_products(*_, first):
    print(products)
    return products[:first]


@product.reference_resolver
def resolve_product_reference(_, _info, representation):
    return get_product_by_upc(representation["upc"])


schema = make_federated_schema(type_defs, [query, product])
graphql_api = GraphQL(schema, debug=True)

def get_product_by_upc(upc: str):
    return next((product for product in products if product["upc"] == upc), None)


app = FastAPI()
app.mount("/graphql", graphql_api)
