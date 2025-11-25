from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

embeddings= HuggingFaceEmbeddings(model_name ='sentence-transformers/all-MiniLM-L6-v2')

def embed_chunks(chunks: list[Document] , document_id: str) -> FAISS:
   
    
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    save_path =f'vectorstores/{document_id}'
    vector_store.save_local(save_path)
    
    return vector_store