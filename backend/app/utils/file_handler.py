from pathlib import Path
import shutil
from fastapi import UploadFile

# Get the project root
BASE_DIR = Path(__file__).resolve().parent.parent

# backend/app/uploads
UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_uploaded_file(file: UploadFile) -> Path:
    """
    Save uploaded file to uploads directory.
    """

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path