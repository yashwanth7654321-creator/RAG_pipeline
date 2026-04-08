import os
from PyPDF2 import PdfReader
from config import TEXT_DATA_PATH 

def load_documents():
     docs = []
     for doc in os.listdir(TEXT_DATA_PATH):
         if doc.endswith(".txt"):
             with open(os.path.join(TEXT_DATA_PATH, doc), "r", encoding="utf-8") as f:
                text = f.read()
                docs.append({"text": text, "source": doc, "page": None})
                
        elif doc.endswith(".pdf"):
            reader = PdfReader(os.path.join(TEXT_DATA_PATH, doc))

            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()

                if text:  # avoid empty pages
                    docs.append({
                        "text": text,
                        "source": doc,
                        "page": page_num + 1
                    })

     return docs