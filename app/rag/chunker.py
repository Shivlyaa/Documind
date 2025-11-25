from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

def chunk_document(
    docs: list[Document] , 
    chunk_size: int = 1000 , 
    chunk_overlap: int = 200) -> list[Document]:
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size= chunk_size,
        chunk_overlap = chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_documents(docs)
    
    for i, chunk in enumerate(chunks):
        if "chunk_index" not in chunk.metadata:
            chunk.metadata["chunk_index"] = i
        
    
    return chunks