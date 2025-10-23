from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class LanguageProficiency(BaseModel):
    language: str = Field(..., description="Language name, e.g., English, Arabic, Turkish")
    level: Optional[str] = Field(None, description="CEFR level (A1-C2) or 'native'")
    ielts: Optional[float] = None
    toefl: Optional[int] = None


class TestScores(BaseModel):
    sat: Optional[int] = None
    act: Optional[int] = None
    gre: Optional[int] = None
    gmat: Optional[int] = None


class Preference(BaseModel):
    fields_of_study: List[str] = []
    preferred_countries: List[str] = []
    budget_usd_per_year: Optional[int] = None


StudyLevel = Literal["undergraduate", "masters", "phd"]


class StudentProfile(BaseModel):
    full_name: Optional[str] = None
    nationality: str = "Palestinian"
    residency_country: Optional[str] = None
    refugee_status: Optional[bool] = None
    study_level: StudyLevel
    gpa: Optional[float] = None
    gpa_scale: float = 4.0
    languages: List[LanguageProficiency] = []
    test_scores: TestScores = TestScores()
    interests: List[str] = []
    financial_need: Optional[bool] = None
