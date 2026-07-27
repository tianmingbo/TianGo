from elasticsearch import Elasticsearch

client = Elasticsearch(
    "http://127.0.0.1:9200",
    basic_auth=("elastic", "07cGnfKRLPZ3ddcckH3h")
)
