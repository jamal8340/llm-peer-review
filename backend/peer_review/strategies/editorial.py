
from peer_review.models import (
    ReviewCase,
    Recommendation,
    DecisionStrategy,
    EditorialDecision,
)


def majority_based(case: ReviewCase) -> EditorialDecision:
    accept_count = sum(
        review.recommendation == Recommendation.ACCEPT
        for review in case.reviews
    )

    reject_count = len(case.reviews) - accept_count

    recommendation = (
        Recommendation.ACCEPT
        if accept_count > reject_count
        else Recommendation.REJECT
    )

    return EditorialDecision(
        paper_id=case.paper.id,
        strategy=DecisionStrategy.MAJORITY,
        recommendation=recommendation,
        justification=(
            f"Majority vote: ACCEPT={accept_count}, "
            f"REJECT={reject_count}"
        ),
        score=accept_count / len(case.reviews),
    )


def expertise_weighted(case: ReviewCase) -> EditorialDecision:
    expertise_by_id = {
        reviewer.id: reviewer.expertise
        for reviewer in case.reviewers
    }

    total_weight = sum(expertise_by_id.values())

    if total_weight <= 0:
        raise ValueError(
            "At least one reviewer must have expertise > 0"
        )

    accept_weight = sum(
        expertise_by_id[review.reviewer_id]
        for review in case.reviews
        if review.recommendation == Recommendation.ACCEPT
    )

    reject_weight = total_weight - accept_weight

    recommendation = (
        Recommendation.ACCEPT
        if accept_weight > reject_weight
        else Recommendation.REJECT
    )

    return EditorialDecision(
        paper_id=case.paper.id,
        strategy=DecisionStrategy.EXPERTISE_WEIGHTED,
        recommendation=recommendation,
        justification=(
            f"Weighted vote: ACCEPT={accept_weight:.2f}, "
            f"REJECT={reject_weight:.2f}"
        ),
        score=accept_weight / total_weight,
    )
