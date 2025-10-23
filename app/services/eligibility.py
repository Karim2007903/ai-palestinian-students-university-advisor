from __future__ import annotations

from app.models.domain import EligibilityRequest, EligibilityResponse, Scholarship, StudentProfile, UniversityProgram


def _normalize_gpa(gpa: float, scale: float) -> float:
    if scale == 4.0:
        return gpa
    if scale == 100:
        return (gpa / 100.0) * 4.0
    return gpa


def _english_ok(profile: StudentProfile) -> bool:
    if profile.english_test is None or profile.english_score is None:
        return True
    # Very rough thresholds
    if profile.english_test == "IELTS":
        return profile.english_score >= 6.0
    if profile.english_test == "TOEFL":
        return profile.english_score >= 80
    if profile.english_test == "Duolingo":
        return profile.english_score >= 105
    return True


class EligibilityService:
    def evaluate(self, request: EligibilityRequest) -> EligibilityResponse:
        profile = request.profile
        item = request.opportunity

        score = 0.0
        reasons: list[str] = []

        # GPA heuristic
        gpa4 = _normalize_gpa(profile.gpa, profile.gpa_scale)
        if gpa4 >= 3.2:
            score += 0.4
            reasons.append("Strong GPA")
        elif gpa4 >= 2.6:
            score += 0.25
            reasons.append("Adequate GPA")
        else:
            reasons.append("GPA may be below many requirements")

        # English
        if _english_ok(profile):
            score += 0.2
            reasons.append("English requirement likely met or flexible")
        else:
            reasons.append("English score may need improvement")

        # Degree alignment
        if hasattr(item, "degree_level") and item.degree_level == profile.degree_level:
            score += 0.2
            reasons.append("Degree level fits")

        # Field alignment
        field = getattr(item, "fields", [])
        if profile.field_of_study and field and profile.field_of_study in field:
            score += 0.1
            reasons.append("Field alignment")

        # Need-based
        if isinstance(item, Scholarship) and profile.financial_need == "high":
            score += 0.1
            reasons.append("High financial need may prioritize scholarships")

        eligible = score >= 0.5
        return EligibilityResponse(eligible=eligible, score=round(score, 3), reasons=reasons)
