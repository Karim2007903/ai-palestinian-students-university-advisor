from __future__ import annotations

from difflib import SequenceMatcher
from typing import Iterable

from app.models.domain import (
    AdviceRequest,
    EligibilityRequest,
    EligibilityResponse,
    Scholarship,
    SearchRequest,
    SearchResponse,
    SearchResult,
    StudentProfile,
    UniversityProgram,
)
from app.providers.scholarships import list_scholarships
from app.providers.universities import list_programs


def _text_score(query: str | None, text: str) -> float:
    if not query:
        return 0.5
    return SequenceMatcher(None, query.lower(), text.lower()).ratio()


def _score_program(p: UniversityProgram, profile: StudentProfile, query: str | None) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []

    # Degree match
    if p.degree_level == profile.degree_level:
        score += 0.4
        reasons.append("Degree level matches")

    # Field match
    if profile.field_of_study and p.fields:
        if profile.field_of_study in p.fields:
            score += 0.3
            reasons.append("Field aligns with program")

    # Location preference
    if profile.location_preference and profile.location_preference == p.country:
        score += 0.1
        reasons.append("Preferred location")

    # Textual similarity
    score += 0.2 * _text_score(query, f"{p.university} {p.name} {' '.join(p.fields)}")

    return score, reasons


def _score_scholarship(s: Scholarship, profile: StudentProfile, query: str | None) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []

    if profile.degree_level in s.degree_levels:
        score += 0.4
        reasons.append("Degree level eligible")

    if profile.field_of_study and s.fields:
        if profile.field_of_study in s.fields:
            score += 0.2
            reasons.append("Field eligible")

    if s.country and profile.location_preference and s.country == profile.location_preference:
        score += 0.1
        reasons.append("Country preference match")

    score += 0.3 * _text_score(query, f"{s.name} {s.provider} {' '.join(s.fields)}")
    return score, reasons


class SearchService:
    def search(self, request: SearchRequest) -> SearchResponse:
        results: list[SearchResult] = []
        if not request.types or "program" in request.types:
            for p in list_programs(request.profile):
                score, reasons = _score_program(p, request.profile, request.query)
                results.append(SearchResult(type="program", score=score, item=p, reasons=reasons))
        if not request.types or "scholarship" in request.types:
            for s in list_scholarships(request.profile):
                score, reasons = _score_scholarship(s, request.profile, request.query)
                results.append(SearchResult(type="scholarship", score=score, item=s, reasons=reasons))

        results.sort(key=lambda r: r.score, reverse=True)
        return SearchResponse(results=results[: request.limit])
