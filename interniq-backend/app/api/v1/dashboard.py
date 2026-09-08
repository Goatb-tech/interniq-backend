from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.dashboard import DashboardStats, ScoreBreakdown
from app.services.score import ScoreService
from app.services.resume import ResumeService
from app.dependencies import current_user_dependency
from app.models.user import User
from typing import Optional

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    user: User = current_user_dependency,
    db: AsyncSession = Depends(get_db),
):
    service = ScoreService(db)
    return await service.get_dashboard_stats(user)


@router.get("/score/{resume_id}", response_model=Optional[ScoreBreakdown])
async def get_score_breakdown(
    resume_id: int,
    user: User = current_user_dependency,
    db: AsyncSession = Depends(get_db),
):
    resume_service = ResumeService(db)
    resume = await resume_service.get_resume(resume_id, user)

    score_service = ScoreService(db)
    return await score_service.get_score_breakdown(resume)
