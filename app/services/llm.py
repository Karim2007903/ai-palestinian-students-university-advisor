from __future__ import annotations

import os
from typing import Any

from app.config import settings
from app.models.domain import AdviceRequest, AdviceResponse

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore


SYSTEM_PROMPT = (
    "You are an education guidance assistant for Palestinian students. Provide practical, current advice "
    "on universities and scholarships, eligibility, and application strategy. Keep answers structured, "
    "actionable, and sensitive to constraints such as travel, finances, and timelines."
)


class AdviceService:
    # Intentionally simple; no initialization needed today
    pass

    def advise(self, request: AdviceRequest) -> AdviceResponse:
        # Fallback if no key
        if not settings.openai_api_key or OpenAI is None:
            return AdviceResponse(
                advice=(
                    "Based on your profile, focus on regional programs and widely accessible scholarships "
                    "(Erasmus Mundus, Chevening, DAAD). Prepare transcripts, recommendation letters, a concise CV, "
                    "and proof of English. Track deadlines 6–12 months ahead. Use AMIDEAST and university portals "
                    "for up-to-date requirements."
                )
            )

        client = OpenAI(api_key=settings.openai_api_key)
        profile = request.profile.model_dump()
        user_prompt = (
            f"Intent: {request.intent}\n"
            f"Profile: {profile}\n"
            f"Context: {request.context or ''}\n\n"
            "Return a numbered action plan with 5-8 steps, followed by a shortlist of 3-6 target scholarships/programs by name if relevant."
        )

        completion = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )
        advice_text = completion.choices[0].message.content or ""
        return AdviceResponse(advice=advice_text)
