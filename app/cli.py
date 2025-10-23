from __future__ import annotations

import argparse
import json

from app.models.domain import AdviceRequest, EligibilityRequest, SearchRequest, StudentProfile
from app.services.eligibility import EligibilityService
from app.services.llm import AdviceService
from app.services.search import SearchService


def main() -> None:
    parser = argparse.ArgumentParser(description="Palestinian Student Guidance CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Common profile args
    def add_profile_args(p: argparse.ArgumentParser) -> None:
        p.add_argument("--degree-level", choices=["undergraduate", "postgraduate"], required=True)
        p.add_argument("--gpa", type=float, required=True)
        p.add_argument("--gpa-scale", type=float, choices=[4.0, 100], default=4.0)
        p.add_argument("--field", dest="field", default=None)
        p.add_argument("--english-test", dest="english_test", choices=["IELTS", "TOEFL", "Duolingo"], default=None)
        p.add_argument("--english-score", dest="english_score", type=float, default=None)
        p.add_argument("--location", dest="location", default=None)
        p.add_argument("--need", dest="need", choices=["low", "medium", "high"], default=None)

    p_search = sub.add_parser("search", help="Search scholarships and programs")
    add_profile_args(p_search)
    p_search.add_argument("--query", default=None)
    p_search.add_argument("--types", nargs="*", choices=["scholarship", "program"], default=None)
    p_search.add_argument("--limit", type=int, default=10)

    p_elig = sub.add_parser("eligibility", help="Estimate eligibility for a sample item")
    add_profile_args(p_elig)

    p_adv = sub.add_parser("advice", help="Get LLM advice")
    add_profile_args(p_adv)
    p_adv.add_argument("--intent", choices=["find_scholarships", "find_programs", "application_tips", "plan_path"], default="find_scholarships")
    p_adv.add_argument("--context", default=None)

    args = parser.parse_args()

    profile = StudentProfile(
        degree_level=args.degree_level,
        gpa=args.gpa,
        gpa_scale=args.gpa_scale,
        field_of_study=args.field,
        english_test=args.english_test,
        english_score=args.english_score,
        location_preference=args.location,
        financial_need=args.need,
    )

    if args.cmd == "search":
        req = SearchRequest(profile=profile, query=args.query, types=args.types, limit=args.limit)
        res = SearchService().search(req)
        print(json.dumps(res.model_dump(mode='json'), indent=2))
    elif args.cmd == "eligibility":
        # For demo, use the top search result as the opportunity
        req = SearchRequest(profile=profile, limit=1)
        search_res = SearchService().search(req)
        if not search_res.results:
            print("No results to evaluate")
            return
        opp = search_res.results[0].item
        elig = EligibilityService().evaluate(EligibilityRequest(profile=profile, opportunity=opp))
        print(json.dumps(elig.model_dump(mode='json'), indent=2))
    elif args.cmd == "advice":
        req = AdviceRequest(profile=profile, intent=args.intent, context=args.context)
        res = AdviceService().advise(req)
        print(res.advice)


if __name__ == "__main__":
    main()
