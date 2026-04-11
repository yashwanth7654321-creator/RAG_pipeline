import numpy as np
from source_code.database import fetch_all_embeddings
from source_code.embedder import embed_text
from config import TOP_K

def cosine_similarity(a, b):
    dot_product = np.dot(a,b)
    return dot_product

def retrive(query, conn, cursor):
    query_vector = embed_text(query)
    data = fetch_all_embeddings(conn, cursor)
    score = []

    for chunk, vector in data:
        sim_score = cosine_similarity(query_vector, vector)
        score.append((chunk, sim_score))

    score_list = sorted(score, key = lambda x: x[1], reverse = True)
    top_score = score_list[:TOP_K]
    retrived_chunks = [chunk for chunk, _ in top_score]
    return retrived_chunks
