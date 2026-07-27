from tools import client

index_name = "book"

mappings = {
    "properties": {
        "text": {
            "type": "text"
        }
    }
}
mapping_response = client.indices.create(index=index_name, mappings=mappings)
print(mapping_response)
