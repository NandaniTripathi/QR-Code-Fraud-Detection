from pathlib import Path
import shutil


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# backend/app/uploads
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_uploaded_file(file):
    """
    Save uploaded file from either FastAPI or Flask.
    """

    file_path = UPLOAD_DIR / file.filename

    # Flask
    if hasattr(file, "save"):
        file.save(file_path)

    # FastAPI
    elif hasattr(file, "file"):
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    else:
        raise ValueError("Unsupported file type.")

    return file_path