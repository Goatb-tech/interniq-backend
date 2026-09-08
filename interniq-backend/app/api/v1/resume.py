from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.resume import ResumeResponse, ResumeDetailResponse
from app.services.resume import ResumeService
from app.services.analysis import AnalysisService
from app.dependencies import current_user_dependency
from app.models.user import User

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/upload", response_model=ResumeResponse, status_code=201)
async def upload_resume(
    file: UploadFile = File(...),
    user: User = current_user_dependency,
    db: AsyncSession = Depends(get_db),
):
    service = ResumeService(db)
    return await service.upload(file, user)


@router.get("/", response_model=List[ResumeResponse])
async def list_resumes(
    user: User = current_user_dependency,
    db: AsyncSession = Depends(get_db),
):
    service = ResumeService(db)
    return await service.get_user_resumes(user)


@router.get("/{resume_id}", response_model=ResumeDetailResponse)
async def get_resume(
    resume_id: int,
    user: User = current_user_dependency,
    db: AsyncSession = Depends(get_db),
):
    service = ResumeService(db)
    return await service.get_resume(resume_id, user)
