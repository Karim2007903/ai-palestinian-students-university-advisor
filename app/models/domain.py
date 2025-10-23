from __future__ import annotations

from typing import Literal, Optional
from pydantic import BaseModel, Field, HttpUrl


class StudentProfile(BaseModel):
    citizenship: str = Field(default="Palestine", description="Student's nationality")
    gpa_scale: Literal[4.0, 100] = Field(default=4.0)
    gpa: float = Field(ge=0)
    english_test: Optional[Literal["IELTS", "TOEFL", "Duolingo"]] = None
    english_score: Optional[float] = None
    field_of_study: Optional[str] = None
    degree_level: Literal["undergraduate", "postgraduate"]
    graduation_year: Optional[int] = None
    financial_need: Optional[Literal["low", "medium", "high"]] = None
    work_experience_years: Optional[float] = None
    location_preference: Optional[str] = None


class Scholarship(BaseModel):
    id: str
    name: str
    provider: str
    country: Optional[str] = None
    degree_levels: list[str] = []
    fields: list[str] = []
    amount: Optional[str] = None
    deadline: Optional[str] = None
    url: Optional[HttpUrl] = None


class UniversityProgram(BaseModel):
    id: str
    university: str
    country: str
    name: str
    degree_level: Literal["undergraduate", "postgraduate"]
    fields: list[str]
    tuition: Optional[str] = None
    url: Optional[HttpUrl] = None


class SearchRequest(BaseModel):
    profile: StudentProfile
    query: Optional[str] = None
    countries: Optional[list[str]] = None
    degree_levels: Optional[list[str]] = None
    fields: Optional[list[str]] = None
    types: Optional[list[Literal["scholarship", "program"]]] = None
    limit: int = 25


class SearchResult(BaseModel):
    type: Literal["scholarship", "program"]
    score: float = 0.0
    item: Scholarship | UniversityProgram
    reasons: list[str] = []


class SearchResponse(BaseModel):
    results: list[SearchResult]


class EligibilityRequest(BaseModel):
    profile: StudentProfile
    opportunity: Scholarship | UniversityProgram


class EligibilityResponse(BaseModel):
    eligible: bool
    score: float
    reasons: list[str]


class AdviceRequest(BaseModel):
    profile: StudentProfile
    intent: Literal["find_scholarships", "find_programs", "application_tips", "plan_path"] = "find_scholarships"
    context: Optional[str] = None


class AdviceResponse(BaseModel):
    advice: str
