from source_code.msg_history import add_message, get_history
from source_code.retriver import retrive
from source_code.create_prompt import create_prompt
from source_code.llm import generate_response
from source_code.store_cache import store_cache

def ask(query, conn, cursor, user_id, collection):
    history = get_history(user_id)
    retrived_chunks = retrive(query, conn, cursor)
    prompt = create_prompt(query, retrived_chunks, history)
    print("Prompt:\n", prompt)
    response = generate_response(prompt)
    add_message(user_id, "user", query)
    add_message(user_id, "assistant", response)
    store_cache(query, response, collection)
    return response

