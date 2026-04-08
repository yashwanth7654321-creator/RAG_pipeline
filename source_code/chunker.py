
from config import CHUNK_SIZE
from config import CHUNK_OVERLAP

step = CHUNK_SIZE - CHUNK_OVERLAP

def chunk_text(text):
    to_list = text.split()
    chunk =[]
    for i in range(0, len(to_list), step):
        chunk.append(" ".join(to_list[i:i+CHUNK_SIZE]))
    return chunk
