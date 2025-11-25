import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

VECTOR_DIR = "vectorstores"
os.makedirs(VECTOR_DIR , exist_ok=True)

# load the same global embedder we are using for embeddings 
embedder = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")

def save_vector_store(vector_store: FAISS ,documnet_id: str):
    # save the just embedded faiss in local memory 
    save_path = os.path.join(VECTOR_DIR, documnet_id)
    vector_store.save_local(save_path)
    return save_path

def load_vector_store(document_id: str) ->FAISS:
    #load the stores vector Faiss for retrieving it
    
    load_path = os.path.join(VECTOR_DIR, document_id) # assigned the path under document id in load path
    
    if not os.path.exists(load_path):
        raise FileNotFoundError(f'vector store does not exist for {document_id}')
    
    vector_store = FAISS.load_local(
        load_path ,
        embeddings= embedder,
        allow_dangerous_deserialization=True 
    )
    
    return vector_store

def get_retriever(document_id :str , k: int = 4):
    # return a retriever that searches the vector_store on the basis of similarity 
    
    vs = load_vector_store(document_id)
    retriever= vs.as_retriever(
        search_type ="similarity",
        search_kwargs = {"k" : k}
    )
    
    return retriever 
    

