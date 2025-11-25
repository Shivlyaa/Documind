from app.rag.vector_store import get_retriever

def retrieved_chunks(document_id:str , question: str, k: int = 4):
   
    # get the retriever
    retriever = get_retriever(document_id , k)
    
    #results
    results = retriever.invoke(question)
    
    return results
