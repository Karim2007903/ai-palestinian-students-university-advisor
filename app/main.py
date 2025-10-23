from __future__ import annotations

from fastapi import FastAPI, HTTPException

from app.config import settings
from app.models.domain import (
    SearchRequest,
    SearchResponse,
    EligibilityRequest,
    EligibilityResponse,
    AdviceRequest,
    AdviceResponse,
)
from app.services.search import SearchService
from app.services.eligibility import EligibilityService
from app.services.llm import AdviceService


def create_app() -> FastAPI:
    app = FastAPI(
        title="Palestinian Student Guidance API",
        version="0.1.0",
        description=(
            "Search universities and scholarships, assess eligibility, and get tailored advice "
            "for Palestinian students pursuing undergraduate and postgraduate studies."
        ),
    )

    search_service = SearchService()
    eligibility_service = EligibilityService()
    advice_service = AdviceService()

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "environment": settings.environment}

    @app.post("/search", response_model=SearchResponse)
    def search(request: SearchRequest) -> SearchResponse:
        try:
            return search_service.search(request)
        except Exception as exc:  # pragma: no cover - guardrail
            raise HTTPException(status_code=500, detail=str(exc))

    @app.post("/eligibility", response_model=EligibilityResponse)
    def eligibility(request: EligibilityRequest) -> EligibilityResponse:
        try:
            return eligibility_service.evaluate(request)
        except Exception as exc:  # pragma: no cover - guardrail
            raise HTTPException(status_code=500, detail=str(exc))

    @app.post("/advice", response_model=AdviceResponse)
    def advice(request: AdviceRequest) -> AdviceResponse:
        try:
            return advice_service.advise(request)
        except Exception as exc:  # pragma: no cover - guardrail
            raise HTTPException(status_code=500, detail=str(exc))

    return app


app = create_app()

if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
