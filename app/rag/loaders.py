from langchain_community.document_loaders import PyPDFLoader , UnstructuredWordDocumentLoader , TextLoader
import os

from typing import List

def load_document(file_path:str):

    # check even the file exists in the first place or not 
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'file not found : {file_path}')
    
    #determine its extension:
    ext= file_path.lower()
    
    

    if ext.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        
    elif ext.endswith(".txt"):
        loader = TextLoader(file_path)
        
    elif ext.endswith(".docx"):
        loader = UnstructuredWordDocumentLoader(file_path)
        
    else:
        raise ValueError(f"Unsupported file type: {ext}")

#now load accordingly

    docs = loader.load() 
    return docs 