
import unittest
from pathlib import Path

from peer_review.engine import run_experiment
from peer_review.models import (
    Recommendation,
    ReviewCase,
    ReviewerProfile,
)
from peer_review.strategies.editorial import (
    majority_based,
    expertise_weighted,
)


CASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "cases"
    / "case_001.json"
)


class TestEditorialStrategies(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import json

        with CASE_PATH.open("r", encoding="utf-8") as f:
            cls.case = ReviewCase.model_validate(json.load(f))

    def test_majority_accepts(self):
        result = majority_based(self.case)
        self.assertEqual(result.recommendation, Recommendation.ACCEPT)

    def test_weighted_rejects(self):
        result = expertise_weighted(self.case)
        self.assertEqual(result.recommendation, Recommendation.REJECT)

    def test_scores(self):
        majority = majority_based(self.case)
        weighted = expertise_weighted(self.case)

        self.assertAlmostEqual(majority.score, 2 / 3)
        self.assertAlmostEqual(weighted.score, 0.8 / 1.7)

    def test_three_reviewers_required(self):
        invalid = self.case.model_dump()
        invalid["reviewers"] = invalid["reviewers"][:2]

        with self.assertRaises(ValueError):
            ReviewCase.model_validate(invalid)

    def test_expertise_out_of_range(self):
        with self.assertRaises(ValueError):
            ReviewerProfile(
                id="invalid",
                name="Invalid reviewer",
                expertise=1.5,
            )

    def test_experiment_correctness(self):
        output = run_experiment(CASE_PATH)
        results = {r["strategy"]: r for r in output["results"]}

        self.assertFalse(results["majority"]["correct"])
        self.assertTrue(results["expertise_weighted"]["correct"])


if __name__ == "__main__":
    unittest.main()
