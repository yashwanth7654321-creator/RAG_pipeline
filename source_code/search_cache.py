from source_code.embedder import embed_text
from config import CACHE_THRESHOLD

def search_cache(query :  str, client, collection):
    query_embed = embed_text(query).tolist()
    results = collection.query(
        query_embeddings = [query_embed],
        n_results = 1
    )

    if results["distances"] and len(results["distances"][0]) > 0:
        distance = results["distances"][0][0]

        similarity = 1 - distance
        if similarity >= CACHE_THRESHOLD:
            return results["metadatas"][0][0]["response"]
    return None
