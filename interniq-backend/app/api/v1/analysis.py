from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.resume import AnalysisResponse, AnalysisResult, SkillItem, ExperienceItem, EducationItem
from app.services.resume import ResumeService
from app.services.analysis import AnalysisService
from app.dependencies import current_user_dependency
from app.models.user import User

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.post("/resumes/{resume_id}", response_model=AnalysisResponse)
async def analyze_resume(
    resume_id: int,
    user: User = current_user_dependency,
    db: AsyncSession = Depends(get_db),
):
    resume_service = ResumeService(db)
    resume = await resume_service.get_resume(resume_id, user)

    analysis_service = AnalysisService(db)
    analyzed = await analysis_service.analyze(resume)

    import json
    skills_list = json.loads(analyzed.skills or "[]")
    exp_list = json.loads(analyzed.experience or "[]")
    edu_list = json.loads(analyzed.education or "[]")
    analysis_dict = json.loads(analyzed.analysis_result or "{}")

    analysis = AnalysisResult(
        skills=[SkillItem(**s) for s in skills_list],
        experience=[ExperienceItem(**e) for e in exp_list],
        education=[EducationItem(**e) for e in edu_list],
        strengths=analysis_dict.get("strengths", []),
        gaps=analysis_dict.get("gaps", []),
        suggestions=analysis_dict.get("suggestions", []),
        readiness_score=analyzed.readiness_score or 0.0,
    )

    return AnalysisResponse(resume_id=analyzed.id, analysis=analysis)
