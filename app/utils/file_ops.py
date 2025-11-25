# app/utils/file_ops.py
import os
import aiofiles
from fastapi import UploadFile
from typing import Tuple

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_uploaded_file(upload_file: UploadFile, document_id: str, ext: str) -> str:
    """
    Save an UploadFile to uploads/<document_id><ext>
    Returns the saved file path.
    """
    filename = f"{document_id}{ext}"
    destination_path = os.path.join(UPLOAD_DIR, filename)

    # async write in chunks
    async with aiofiles.open(destination_path, "wb") as out_file:
        while True:
            chunk = await upload_file.read(1024 * 1024)  # 1MB
            if not chunk:
                break
            await out_file.write(chunk)
    await upload_file.close()
    return destination_path
