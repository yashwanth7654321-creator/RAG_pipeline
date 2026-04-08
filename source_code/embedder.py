from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL
import numpy as np


model =  SentenceTransformer(EMBEDDING_MODEL)

def embed_text(chunk):
    vector = model.encode(chunk)
    normalized_vector = vector / np.linalg.norm(vector)
    return normalized_vector


