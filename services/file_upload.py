import os
from uuid import uuid4
from fastapi import UploadFile, HTTPException
from core.config import settings

UPLOAD_DIR = "uploaded_logs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(file: UploadFile, log_type: str) -> str:
    """
    Validates file size and saves it locally.
    Returns the saved file path.
    """
    content = file.file.read()
    file_size_mb = len(content) / (1024 * 1024)

    if file_size_mb > settings.max_file_size_mb:
        raise HTTPException(status_code=413, detail="File too large")

    ext = file.filename.split(".")[-1]
    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.{ext}")

    with open(file_path, "wb") as f:
        f.write(content)

    return file_path