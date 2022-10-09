from ariadne import make_executable_schema, load_schema_from_path, QueryType
from ariadne.asgi import GraphQL
from ariadne.contrib.federation import FederatedObjectType, make_federated_schema
from fastapi import FastAPI

type_defs = load_schema_from_path("gql/user.graphql")

query = QueryType()
user = FederatedObjectType("User")

@query.field("me")
def resolve_me(_, info):
    print("Hello.. its me.")
    return users[0]


@user.reference_resolver
def resolve_user_reference(_, _info, representation):
    return get_user_by_email(representation.get("email"))


schema = make_federated_schema(type_defs, [query, user])
graphql_api = GraphQL(schema, debug=True)

users = [
    {"id": 1, "name": "Ada Lovelace", "email": "ada@example.com"},
    {"id": 2, "name": "Alan Turing", "email": "alan@example.com"},
]


def get_user_by_email(email: str):
    return next((user for user in users if user["email"] == email), None)


app = FastAPI()
app.mount("/graphql", graphql_api)
