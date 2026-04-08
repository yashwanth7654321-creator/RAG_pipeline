import os
from config import TEXT_DATA_PATH 

def load_documents():
     docs = []
     for doc in os.listdir(TEXT_DATA_PATH):
         if doc.endswith(".txt"):
             with open(os.path.join(TEXT_DATA_PATH, doc), "r", encoding="utf-8") as f:
                text = f.read()
                docs.append({"text": text, "source": doc, "page": None})
     return docs