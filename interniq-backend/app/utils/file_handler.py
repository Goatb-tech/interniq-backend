import os
from fastapi import UploadFile
from app.config import settings


def validate_file_extension(filename: str) -> bool:
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    return ext in settings.ALLOWED_EXTENSIONS


def get_file_size(file: UploadFile) -> int:
    return file.size or 0
