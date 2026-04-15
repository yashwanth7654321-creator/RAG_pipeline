
def chunk_text(text, config):

    chunk_size = config["chunk_size"]
    overlap = config["overlap"]
    step = chunk_size - overlap

    to_list = text.split()
    chunk =[]
    for i in range(0, len(to_list), step):
        chunk.append(" ".join(to_list[i:i+chunk_size]))
    return chunk
