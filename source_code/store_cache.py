import uuid
from  source_code.embedder import embed_text
from config import MAX_CACHE_SIZE

cache_ids = []

def store_cache(query : str, response : str, collection):
    query_embed = embed_text(query).tolist()
    new_id = str(uuid.uuid4())
    collection.add(
        ids = [new_id],
        embeddings = [query_embed],
        metadatas = [{"query": query, "response": response}]    
    )
    cache_ids.append(new_id)
    if len(cache_ids) > MAX_CACHE_SIZE:
        oldest_id = cache_ids.pop(0)
        collection.delete(ids=[oldest_id])

