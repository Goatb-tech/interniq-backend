from sqlalchemy.ext.asyncio import AsyncSession
from app.models.resume import Resume
from app.config import settings
import json


class AnalysisService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze(self, resume: Resume) -> Resume:
        parsed = self._parse_resume_text(resume)
        score = self._calculate_readiness_score(parsed)

        resume.parsed_text = parsed.get("raw_text", "")
        resume.skills = json.dumps(parsed.get("skills", []))
        resume.experience = json.dumps(parsed.get("experience", []))
        resume.education = json.dumps(parsed.get("education", []))
        resume.readiness_score = score
        resume.analysis_result = json.dumps(parsed.get("analysis", {}))

        await self.db.flush()
        await self.db.refresh(resume)
        return resume

    def _parse_resume_text(self, resume: Resume) -> dict:
        return {
            "raw_text": f"Parsed content of {resume.filename}",
            "skills": [
                {"name": "Python", "category": "Programming", "proficiency": "Advanced"},
                {"name": "FastAPI", "category": "Framework", "proficiency": "Intermediate"},
                {"name": "PostgreSQL", "category": "Database", "proficiency": "Intermediate"},
            ],
            "experience": [
                {
                    "title": "Software Engineering Intern",
                    "company": "Tech Corp",
                    "duration": "Jun 2024 - Aug 2024",
                    "description": "Built REST APIs with FastAPI and PostgreSQL",
                }
            ],
            "education": [
                {
                    "degree": "B.Tech in Computer Science",
                    "institution": "University of Technology",
                    "year": "2022 - 2026",
                }
            ],
            "analysis": {
                "strengths": ["Strong programming fundamentals", "Relevant internship experience"],
                "gaps": ["Limited cloud experience", "No open source contributions"],
                "suggestions": [
                    "Contribute to open source projects",
                    "Learn AWS or GCP fundamentals",
                ],
            },
        }

    def _calculate_readiness_score(self, parsed: dict) -> float:
        score = 0.0
        skills_count = len(parsed.get("skills", []))
        exp_count = len(parsed.get("experience", []))

        if skills_count >= 5:
            score += 40
        elif skills_count >= 3:
            score += 25
        elif skills_count >= 1:
            score += 10

        if exp_count >= 2:
            score += 30
        elif exp_count >= 1:
            score += 20

        if parsed.get("education"):
            score += 20

        strength_count = len(parsed.get("analysis", {}).get("strengths", []))
        if strength_count >= 3:
            score += 10
        elif strength_count >= 1:
            score += 5

        return min(round(score, 1), 100.0)
