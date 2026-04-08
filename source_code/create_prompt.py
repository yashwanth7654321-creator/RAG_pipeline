def create_prompt(query, retrived_chunks, history):
    history_text = "\n".join([f"{msg['role']} : {msg['content']}" for msg in history])
    context = "\n\n".join([chunk for chunk, _ in retrived_chunks])
    prompt = f"""You are a helpful assistant.
    Rules:
    - Use the context as the primary source.
    - Use conversation history only to understand the question.
    - Resolve references like "it", "this" using history.
    - If answer is not in context, say "I don't know".,

    Conversation history:
    {history_text}
    
    Context: 
    {context}
    
    Question: 
    {query}
    
    Answer : """
    return prompt