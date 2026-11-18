
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from peer_review.engine import run_experiment


router = APIRouter(
    prefix="/api/peer-review",
    tags=["Peer Review POC"],
)

CASES_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "cases"
)


class RunExperimentRequest(BaseModel):
    case_id: str = "case_001"


@router.post("/experiments/run")
def run_peer_review_experiment(request: RunExperimentRequest):
    # Na razie udostępniamy tylko zatwierdzony przypadek POC.
    # Nie przyjmujemy dowolnych ścieżek plików od użytkownika.
    if request.case_id != "case_001":
        raise HTTPException(
            status_code=404,
            detail="Nieznany przypadek testowy",
        )

    case_path = CASES_DIR / "case_001.json"

    if not case_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Brak pliku case_001.json",
        )

    return run_experiment(case_path)
