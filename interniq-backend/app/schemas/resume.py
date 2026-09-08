from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List


class ResumeResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResumeDetailResponse(ResumeResponse):
    parsed_text: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    readiness_score: Optional[float] = None
    analysis_result: Optional[str] = None


class SkillItem(BaseModel):
    name: str
    category: Optional[str] = None
    proficiency: Optional[str] = None


class ExperienceItem(BaseModel):
    title: str
    company: str
    duration: str
    description: Optional[str] = None


class EducationItem(BaseModel):
    degree: str
    institution: str
    year: str


class AnalysisResult(BaseModel):
    skills: List[SkillItem]
    experience: List[ExperienceItem]
    education: List[EducationItem]
    strengths: List[str]
    gaps: List[str]
    suggestions: List[str]
    readiness_score: float


class AnalysisResponse(BaseModel):
    resume_id: int
    analysis: AnalysisResult
