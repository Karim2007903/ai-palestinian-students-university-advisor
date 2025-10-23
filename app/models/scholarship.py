from typing import Optional, List, Literal
from pydantic import BaseModel
from datetime import date


DegreeLevel = Literal["undergraduate", "masters", "phd"]


class ScholarshipCoverage(BaseModel):
    tuition_covered_percent: Optional[int] = None
    stipend_monthly_usd: Optional[int] = None
    airfare: Optional[bool] = None
    housing: Optional[bool] = None
    health_insurance: Optional[bool] = None


class Scholarship(BaseModel):
    id: str
    name: str
    provider: str
    degree_levels: List[DegreeLevel]
    eligible_nationalities: List[str] = ["Any"]
    eligible_residencies: List[str] = []
    fields_supported: List[str] = ["Any"]
    min_gpa: Optional[float] = None
    ielts_min: Optional[float] = None
    toefl_min: Optional[int] = None
    application_deadline: Optional[date] = None
    coverage: ScholarshipCoverage = ScholarshipCoverage()
    description: Optional[str] = None
    application_url: Optional[str] = None
    notes: Optional[str] = None
