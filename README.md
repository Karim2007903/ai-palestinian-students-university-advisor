# Palestinian Student Academic Guidance Agent (FastAPI)

**Attribution:**
This project draws inspiration from agentic design patterns like ReAct (Reasoning + Acting), originally popularized by Simon Willison's Python ReAct pattern and expanded in the AI Agents in LangGraph course by DeepLearning.AI. While this repository currently implements a rules-based core with a lightweight search layer, it is structured to be extended into a full ReAct-style agent.

This project helps Palestinian students find suitable universities, programs, and scholarships for both undergraduate and postgraduate study. It focuses on clear eligibility guidance, budget-aware matching, and pragmatic, up-to-date recommendations.

## Project Structure
- `app/main.py`: FastAPI application entrypoint and router mounting
- `app/config.py`: Application settings using Pydantic Settings
- `app/api/routes.py`: Health and (future) API endpoints
- `app/models/`: Typed Pydantic models
  - `profile.py`: `StudentProfile`, language proficiency, test scores
  - `university.py`: `University`
  - `program.py`: `Program`
  - `scholarship.py`: `Scholarship`, `ScholarshipCoverage`
- `app/services/`: Business logic (eligibility, ranking, search) [to be expanded]
- `app/data/`: Seed datasets for universities, programs, scholarships
- `requirements.txt`: Python dependencies
- `LICENSE`: MIT License

## Features
- **Student-centric modeling**: Clear schema for profile, preferences, tests, and languages
- **Rules-based eligibility**: GPA, language, and test thresholds with human-readable explanations
- **Matching and ranking**: Score programs and scholarships against profile and preferences
- **Budget awareness**: Filter and score by tuition and estimated costs
- **Lightweight search**: Local TF‑IDF over datasets and knowledge snippets (extensible)
- **FastAPI service**: Ready for deployment, with JSON APIs and simple health check
- **Extensible to ReAct**: Structure prepared for tool-calling (search, calculate, fetch) and LLM orchestration

## Available Endpoints (initial)
- `GET /` — Service metadata
- `GET /api/health` — Health check

Planned endpoints:
- `POST /api/match/programs` — Return top‑K program matches with eligibility notes
- `POST /api/match/scholarships` — Return top‑K scholarship matches with eligibility notes
- `GET /api/search` — Lightweight search over local datasets/KB

## Setup
1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Create a `.env` for future integrations:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## Run the API Server
Start a local development server (auto‑reload):
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check:
```bash
curl http://localhost:8000/api/health
```

Service info:
```bash
curl http://localhost:8000/
```

## Example: Student Profile JSON
Use this shape for future match endpoints:
```json
{
  "full_name": "Layla A.",
  "nationality": "Palestinian",
  "residency_country": "Jordan",
  "refugee_status": true,
  "study_level": "masters",
  "gpa": 3.5,
  "gpa_scale": 4.0,
  "languages": [
    { "language": "Arabic", "level": "native" },
    { "language": "English", "level": "C1", "ielts": 7.0 }
  ],
  "test_scores": { "gre": 312 },
  "interests": ["Computer Science", "AI"],
  "financial_need": true
}
```

## Usage Ideas
- Send a `StudentProfile` to `/api/match/programs` to receive ranked program options, eligibility notes, and deadlines.
- Send the same profile to `/api/match/scholarships` to discover funding that matches eligibility, field, and need.
- Use `/api/search` to surface locally indexed guidance and FAQs.

## Data and Freshness
- Seed datasets in `app/data/` act as a baseline for matching.
- For current scholarship calls and deadlines, integrate an external search/fetch tool (e.g., Tavily, SERP/Bing) and keep a refresh schedule.
- Keep provenance: store source URLs and last‑checked timestamps alongside entries.

## Testing
This repository is structured for `pytest`. After adding tests under `tests/`, run:
```bash
python -m pytest -q
```

## Roadmap / Suggested Improvements
- Add full eligibility explanation traces (which rule passed/failed and why)
- Implement TF‑IDF index and semantic reranking for search
- Integrate optional live web search (Tavily or Bing) with caching
- Build program/scholarship match endpoints with scoring and filters
- Add CLI for offline matching and dataset curation
- Add streaming LLM guidance via OpenRouter and a ReAct loop for tool use
- Add pre‑commit hooks and CI (lint, type check, tests)

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
