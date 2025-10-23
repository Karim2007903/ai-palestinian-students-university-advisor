from typing import Optional, List, Literal
from pydantic import BaseModel
from datetime import date


DegreeLevel = Literal["undergraduate", "masters", "phd"]


class Program(BaseModel):
    id: str
    university_id: str
    name: str
    degree_level: DegreeLevel
    field_of_study: str
    language: str = "English"
    tuition_usd_per_year: Optional[int] = None
    min_gpa: Optional[float] = None
    ielts_min: Optional[float] = None
    toefl_min: Optional[int] = None
    required_tests: List[str] = []
    application_deadline: Optional[date] = None
    description: Optional[str] = None
