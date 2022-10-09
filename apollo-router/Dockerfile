FROM debian:latest
RUN apt update && apt install -y curl
RUN curl -sSL https://router.apollo.dev/download/nix/latest | sh

COPY ./supergraph-schema.graphql /supergraph-schema.graphql
COPY ./router.yml /router.yml

EXPOSE 4000
ENTRYPOINT ["./router", "--dev", "--supergraph", "/supergraph-schema.graphql","--config", "/router.yml"]


