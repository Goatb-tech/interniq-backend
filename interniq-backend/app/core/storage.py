import os
import aiofiles
from fastapi import UploadFile, HTTPException, status
from app.config import settings


ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}


async def save_upload(file: UploadFile, user_id: int) -> str:
    ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type .{ext} not allowed. Allowed: {settings.ALLOWED_EXTENSIONS}",
        )

    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds max upload size of {settings.MAX_UPLOAD_SIZE // (1024*1024)}MB",
        )

    user_dir = os.path.join(settings.UPLOAD_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)

    file_path = os.path.join(user_dir, file.filename)
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    return file_path
