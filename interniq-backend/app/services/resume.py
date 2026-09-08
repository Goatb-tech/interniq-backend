from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.resume import Resume
from app.models.user import User
from app.core.storage import save_upload
from fastapi import UploadFile, HTTPException, status
from typing import Optional


class ResumeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upload(self, file: UploadFile, user: User) -> Resume:
        file_path = await save_upload(file, user.id)

        ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""

        resume = Resume(
            user_id=user.id,
            filename=file.filename,
            file_path=file_path,
            file_size=file.size,
            file_type=ext,
        )
        self.db.add(resume)
        await self.db.flush()
        await self.db.refresh(resume)
        return resume

    async def get_user_resumes(self, user: User) -> list[Resume]:
        result = await self.db.execute(
            select(Resume).where(Resume.user_id == user.id).order_by(Resume.created_at.desc())
        )
        return result.scalars().all()

    async def get_resume(self, resume_id: int, user: User) -> Resume:
        result = await self.db.execute(
            select(Resume).where(Resume.id == resume_id, Resume.user_id == user.id)
        )
        resume = result.scalar_one_or_none()
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found",
            )
        return resume
