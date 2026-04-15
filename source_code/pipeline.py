import time
from source_code.msg_history import add_message, get_history
from source_code.retriver import retrive
from source_code.create_prompt import create_prompt
from source_code.llm import generate_response
from source_code.store_cache import store_cache

def ask(query, conn, cursor, user_id, collection, config):
    start_retriver = time.perf_counter()

    history = get_history(user_id)
    retrived_chunks = retrive(query, conn, cursor, config["chunk_size"], config["overlap"], config["top_k"])
    
    retrival_time = time.perf_counter() - start_retriver

    prompt = create_prompt(query, retrived_chunks, history)
    print("Prompt:\n", prompt)

    start_generator = time.perf_counter()

    response = generate_response(prompt)
    generation_time = time.perf_counter() - start_generator

    add_message(user_id, "user", query)
    add_message(user_id, "assistant", response)
    store_cache(query, response, collection)

    return response, retrived_chunks, retrival_time, generation_time

