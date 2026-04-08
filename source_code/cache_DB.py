import chromadb
def create_cache_DB():
    client = chromadb.Client()
    collection = client.get_or_create_collection("semantic_cache")
    return client, collection
