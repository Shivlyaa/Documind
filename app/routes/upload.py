import os
from fastapi import APIRouter, UploadFile, File, HTTPException , status
from uuid import uuid4

from app.utils.file_ops import save_uploaded_file
from app.rag.loaders import load_document
from app.rag.chunker import chunk_document
from app.rag.embeddings import embed_chunks

router = APIRouter()

# Location where uploaded files will be stored
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Supported formats
ALLOWED_EXTS = {'.pdf' , '.txt' , '.docx'}


@router.post("/upload" , status_code=status.HTTP_201_CREATED)
async def upload_and_ingest_document(file: UploadFile = File(...)):
    """
    Accepts a document (PDF/TXT/DOCX),
    validates the type,
    saves it to /uploads,
    then ingests it with proper loading+chunk+embed
    and returns a document_id.
    """

    # 1) Validate file type
    original_filename = file.filename
    filename_without_ext , ext = os.path.splitext(original_filename.lower())
    
    if ext not in ALLOWED_EXTS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. "
                   f"Allowed: PDF, TXT, DOCX."
        )


    #2 save the file using save_uploaded_file
    document_id = str(uuid4())
    file_path= await save_uploaded_file(file, document_id, ext)
    
    #3 now that we have file_path, we can load it 
    try:
        docs = load_document(file_path)
    except Exception as e:
        #if failure on load, we gotta clean the file and save space
        try:
            os.remove(file_path)
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=f"Failed to parse uploaded file: {e}")
    
    
    # 4 chunking 
    chunks = chunk_document(docs)
    
    #5 embedding
    vectors= embed_chunks(chunks , document_id)
    
    return{
        "status": "success",
        "document_id": document_id,
        "original_filename" : original_filename,
        "filename": os.path.basename(file_path),
        "file_path": file_path,
        "num_documents": len(docs),
        "preview": docs[0].page_content[:300] if docs else ""
    }
        
        
