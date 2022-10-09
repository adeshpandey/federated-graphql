from ariadne import load_schema_from_path, QueryType
from ariadne.asgi import GraphQL
from ariadne.contrib.federation import make_federated_schema, FederatedObjectType
from fastapi import FastAPI


def get_review_list(*_):
    return "Users List"


type_defs = load_schema_from_path("gql/reviews.graphql")

query = QueryType()
review = FederatedObjectType("Review")
user = FederatedObjectType("User")
product = FederatedObjectType("Product")


@review.reference_resolver
def resolve_reviews_reference(_, _info, representation):
    return get_review_by_id(representation["id"])


@review.field("author")
def resolve_review_author(review, *_):
    return {"__typename": "User", "email": review["user"]["email"]}


@review.field("product")
def resolve_review_product(review, *_):
    return {"__typename": "Product", "upc": review["product"]["upc"]}


@user.field("reviews")
def resolve_user_reviews(representation, *_):
    return get_user_reviews(representation["email"])


@product.field("reviews")
def resolve_product_reviews(representation, *_):
    return get_product_reviews(representation["upc"])


reviews = [
    {
        "id": "1",
        "user": {"email": "ada@example.com"},
        "product": {"upc": "1"},
        "body": "Love it!",
    },
    {
        "id": "2",
        "user": {"email": "ada@example.com"},
        "product": {"upc": "2"},
        "body": "Too expensive.",
    },
    {
        "id": "3",
        "user": {"email": "alan@example.com"},
        "product": {"upc": "2"},
        "body": "Could be better.",
    },
]


def get_review_by_id(id: int):
    return next((review for review in reviews if review["id"] == id), None)


def get_user_reviews(email: str):
    return [review for review in reviews if review["user"]["email"] == email]


def get_product_reviews(upc: str):
    return [review for review in reviews if review["product"]["upc"] == upc]


schema = make_federated_schema(type_defs, [query, user, review, product])

graphql_api = GraphQL(schema=schema, debug=True)

app = FastAPI()
app.mount("/graphql", graphql_api)
