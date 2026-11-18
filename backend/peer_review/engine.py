
import json
from pathlib import Path

from peer_review.models import ReviewCase
from peer_review.strategies.editorial import (
    majority_based,
    expertise_weighted,
)


def run_experiment(case_path: str | Path) -> dict:
    path = Path(case_path)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    case = ReviewCase.model_validate(data)

    majority = majority_based(case)
    weighted = expertise_weighted(case)

    return {
        "paper_id": case.paper.id,
        "expected_decision": case.expected_decision.value,
        "results": [
            {
                **decision.model_dump(mode="json"),
                "correct": (
                    decision.recommendation
                    == case.expected_decision
                ),
            }
            for decision in (majority, weighted)
        ],
    }


if __name__ == "__main__":
    case_file = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "cases"
        / "case_001.json"
    )

    result = run_experiment(case_file)
    print(json.dumps(result, indent=2, ensure_ascii=False))
