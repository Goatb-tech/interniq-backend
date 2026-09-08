from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.resume import Resume
from app.models.user import User
from typing import Optional
import json


class ScoreService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard_stats(self, user: User) -> dict:
        result = await self.db.execute(
            select(Resume).where(Resume.user_id == user.id).order_by(Resume.created_at.desc())
        )
        resumes = result.scalars().all()

        if not resumes:
            return {
                "total_resumes": 0,
                "latest_score": None,
                "highest_score": None,
                "average_score": None,
                "skills_count": None,
            }

        scores = [r.readiness_score for r in resumes if r.readiness_score is not None]
        all_skills = set()
        for r in resumes:
            if r.skills:
                skills_list = json.loads(r.skills)
                for skill in skills_list:
                    all_skills.add(skill.get("name", ""))

        return {
            "total_resumes": len(resumes),
            "latest_score": scores[0] if scores else None,
            "highest_score": max(scores) if scores else None,
            "average_score": round(sum(scores) / len(scores), 1) if scores else None,
            "skills_count": len(all_skills),
        }

    async def get_score_breakdown(self, resume: Resume) -> dict:
        if not resume.readiness_score:
            return None

        base = resume.readiness_score
        return {
            "skills_score": round(base * 0.4, 1),
            "experience_score": round(base * 0.3, 1),
            "education_score": round(base * 0.2, 1),
            "overall_score": resume.readiness_score,
        }
