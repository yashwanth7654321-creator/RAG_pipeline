from config import MAX_HISTORY
from config import MAX_HISTORY_TOKENS

chat_memory = {}

def summarize_text(text):
    if len(text) <= MAX_HISTORY_TOKENS:
        return text
    return text[:MAX_HISTORY_TOKENS] + "..."

def add_message(user_id, role, message):
    if user_id not in chat_memory:
        chat_memory[user_id] = []
    
    if  role == "assistant":
        message = summarize_text(message)
        
    chat_memory[user_id].append({"role": role, "content": message})

def get_history(user_id):
    return chat_memory.get(user_id, [])[-MAX_HISTORY:]


#chat_memory = {

#    "user123": [
#        {"role": "user", "content": "Hello"},
#        {"role": "assistant", "content": "Hi there!"}
#    ],
#    "user456": [
#        {"role": "user", "content": "What's up?"}
#    ]
# }
# #############################################################
# # output will be for chat_memory.get(user_id, [])[-k:]
# [
#    {"role":"user","content":"How are you?"},
#    {"role":"assistant","content":"Doing well!"}
# ]
# print(user_id)