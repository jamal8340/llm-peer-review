
import json
from pathlib import Path

from peer_review.models import ReviewCase
from peer_review.agents.reviewer import ReviewerAgent
from peer_review.strategies.editorial import (
    majority_based,
    expertise_weighted,
)


CASES_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "cases"
)


def run_llm_experiment(case_id: str = "case_001") -> dict:
    if case_id != "case_001":
        raise ValueError("Nieznany przypadek testowy")

    case_path = CASES_DIR / f"{case_id}.json"

    with case_path.open("r", encoding="utf-8") as file:
        case_data = json.load(file)

    original_case = ReviewCase.model_validate(case_data)

    paper = original_case.paper
    generated_reviews = []

    # Trzej recenzenci oceniają ten sam artykuł.
    # Nie widzą recenzji pozostałych agentów.
    for profile in original_case.reviewers:
        print(f"[LLM] Generowanie recenzji: {profile.name}")

        agent = ReviewerAgent(profile)
        review = agent.review(paper)

        generated_reviews.append(review)

    # Budujemy nowy przypadek z recenzjami LLM.
    # Nie modyfikujemy oryginalnego pliku JSON.
    llm_case = ReviewCase.model_validate({
        "paper": original_case.paper.model_dump(),
        "reviewers": [
            p.model_dump()
            for p in original_case.reviewers
        ],
        "reviews": [
            r.model_dump(mode="json")
            for r in generated_reviews
        ],
        "expected_decision": (
            original_case.expected_decision.value
        ),
    })

    # Korzystamy z istniejących strategii.
    decisions = [
        majority_based(llm_case),
        expertise_weighted(llm_case),
    ]

    return {
        "paper_id": paper.id,
        "mode": "llm",
        "model": __import__("config").settings.groq_model,
        "expected_decision": (
            llm_case.expected_decision.value
        ),
        "reviews": [
            review.model_dump(mode="json")
            for review in generated_reviews
        ],
        "results": [
            {
                **decision.model_dump(mode="json"),
                "correct": (
                    decision.recommendation
                    == llm_case.expected_decision
                ),
            }
            for decision in decisions
        ],
    }


if __name__ == "__main__":
    result = run_llm_experiment()

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        )
    )
