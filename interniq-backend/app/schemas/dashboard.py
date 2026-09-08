from pydantic import BaseModel
from typing import Optional


class DashboardStats(BaseModel):
    total_resumes: int
    latest_score: Optional[float] = None
    highest_score: Optional[float] = None
    average_score: Optional[float] = None
    skills_count: Optional[int] = None


class ScoreBreakdown(BaseModel):
    skills_score: float
    experience_score: float
    education_score: float
    overall_score: float
