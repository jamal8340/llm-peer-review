
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, model_validator


class Recommendation(str, Enum):
    ACCEPT = "accept"
    REJECT = "reject"


class DecisionStrategy(str, Enum):
    MAJORITY = "majority"
    EXPERTISE_WEIGHTED = "expertise_weighted"


class Paper(BaseModel):
    id: str
    title: str
    abstract: str
    content: str = ""
    version: int = Field(default=1, ge=1)


class ReviewerProfile(BaseModel):
    id: str
    name: str
    expertise: float = Field(ge=0.0, le=1.0)
    criticality: float = Field(default=0.5, ge=0.0, le=1.0)
    agreeableness: float = Field(default=0.5, ge=0.0, le=1.0)
    dominance: float = Field(default=0.5, ge=0.0, le=1.0)


class ReviewIssue(BaseModel):
    description: str
    severity: int = Field(ge=1, le=5)
    justification: str = ""


class Review(BaseModel):
    paper_id: str
    reviewer_id: str
    recommendation: Recommendation
    issues: list[ReviewIssue] = Field(default_factory=list)
    justification: str = ""


class EditorialDecision(BaseModel):
    paper_id: str
    strategy: DecisionStrategy
    recommendation: Recommendation
    justification: str
    score: float = Field(ge=0.0, le=1.0)


class ReviewCase(BaseModel):
    paper: Paper
    reviewers: list[ReviewerProfile]
    reviews: list[Review]
    expected_decision: Recommendation

    @model_validator(mode="after")
    def validate_case(self):
        reviewer_ids = [reviewer.id for reviewer in self.reviewers]

        if len(reviewer_ids) != 3 or len(set(reviewer_ids)) != 3:
            raise ValueError("POC wymaga dokładnie 3 różnych recenzentów")

        if len(self.reviews) != 3:
            raise ValueError("POC wymaga dokładnie 3 recenzji")

        review_ids = [review.reviewer_id for review in self.reviews]

        if set(review_ids) != set(reviewer_ids):
            raise ValueError("Każdy recenzent musi dostarczyć jedną recenzję")

        if len(set(review_ids)) != 3:
            raise ValueError("Recenzje nie mogą się powtarzać")

        if any(review.paper_id != self.paper.id for review in self.reviews):
            raise ValueError("Recenzje muszą dotyczyć tego samego artykułu")

        return self
