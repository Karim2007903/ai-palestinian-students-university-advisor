from __future__ import annotations

from typing import Iterable
from pathlib import Path

import yaml

from app.models.domain import UniversityProgram, StudentProfile


def _matches_profile(p: UniversityProgram, profile: StudentProfile) -> bool:
    if profile.degree_level and p.degree_level != profile.degree_level:
        return False
    if profile.field_of_study:
        if p.fields and profile.field_of_study not in p.fields:
            return False
    if profile.location_preference and profile.location_preference != p.country:
        return False
    return True


def load_programs() -> list[UniversityProgram]:
    data_path = Path(__file__).with_name("universities_data.yaml")
    with data_path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return [UniversityProgram(**item) for item in raw]


def list_programs(profile: StudentProfile) -> Iterable[UniversityProgram]:
    programs = load_programs()
    return [p for p in programs if _matches_profile(p, profile)]
