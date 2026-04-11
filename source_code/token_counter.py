import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(enc.encode(text))

def count_rag_tokens(query, chunks, response):
    context = "\n".join([c for c in chunks])

    input_text = query + "\n" + context

    input_tokens = count_tokens(input_text)
    output_tokens = count_tokens(response)

    tokens_data = {"input_tokens": input_tokens, 
              "output_tokens": output_tokens, 
              "total_tokens": input_tokens + output_tokens}
    
    return tokens_data
