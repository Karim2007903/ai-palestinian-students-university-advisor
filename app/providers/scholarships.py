from __future__ import annotations

from typing import Iterable

from app.models.domain import Scholarship, StudentProfile


def _matches_profile(s: Scholarship, profile: StudentProfile) -> bool:
    if profile.degree_level and s.degree_levels and profile.degree_level not in s.degree_levels:
        return False
    if profile.field_of_study and s.fields and profile.field_of_study not in s.fields:
        return False
    return True


def list_scholarships(profile: StudentProfile) -> Iterable[Scholarship]:
    # Seed with a few commonly relevant entries; in production scrape/APIs
    data = [
        Scholarship(
            id="amideast-hope-fund",
            name="AMIDEAST Hope Fund",
            provider="AMIDEAST",
            country="USA",
            degree_levels=["undergraduate"],
            fields=[],
            amount="Partial/Full",
            deadline=None,
            url="https://www.amideast.org/",
        ),
        Scholarship(
            id="chevening",
            name="Chevening Scholarships",
            provider="UK FCDO",
            country="UK",
            degree_levels=["postgraduate"],
            fields=[],
            amount="Full",
            deadline=None,
            url="https://www.chevening.org/",
        ),
        Scholarship(
            id="erasmus-mundus",
            name="Erasmus Mundus Joint Masters",
            provider="EU",
            country="EU",
            degree_levels=["postgraduate"],
            fields=[],
            amount="Full",
            deadline=None,
            url="https://www.eacea.ec.europa.eu/scholarships/emjmd-catalogue",
        ),
    ]

    return [s for s in data if _matches_profile(s, profile)]
