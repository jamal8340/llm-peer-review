
import json

from groq import Groq

from config import settings
from peer_review.models import Paper, ReviewerProfile, Review


class ReviewerAgent:
    def __init__(self, profile: ReviewerProfile):
        self.profile = profile

        if (
            not settings.groq_api_key
            or settings.groq_api_key == "your_groq_api_key_here"
        ):
            raise ValueError(
                "Brak GROQ_API_KEY w backend/.env"
            )

        self.client = Groq(
            api_key=settings.groq_api_key,
            timeout=60.0,
        )

    def _system_prompt(self) -> str:
        p = self.profile

        return f"""
You are an independent scientific peer reviewer.

Reviewer name: {p.name}

Your reviewer profile:
- Expertise: {p.expertise}/1.0
- Criticality: {p.criticality}/1.0
- Agreeableness: {p.agreeableness}/1.0
- Dominance: {p.dominance}/1.0

Behavioral guidelines:
- Higher expertise means more attention to methodology,
  statistics, logic and scientific validity.
- Higher criticality means stricter evaluation of weaknesses.
- Higher agreeableness means a more constructive review style.
- Dominance affects confidence of expression, not accuracy.
- Adapt your review style to this profile.
- Do not invent evidence or methodological details.
- If information is missing, explicitly mention it.
- Evaluate the submitted text, not its author's identity.
- Do not assume the paper is correct.
- Judge substantive scientific quality, not just writing style.

Return ONLY a valid JSON object with this structure:

{{
  "recommendation": "accept or reject",
  "justification": "Detailed explanation",
  "issues": [
    {{
      "description": "Specific scientific issue",
      "severity": 1,
      "justification": "Evidence from the submitted text"
    }}
  ]
}}

Severity must be an integer from 1 to 5.
Do not add Markdown code fences or other text.
"""

    def review(self, paper: Paper) -> Review:
        user_prompt = f"""
Review the following scientific submission.

TITLE:
{paper.title}

ABSTRACT:
{paper.abstract}

CONTENT:
{paper.content}

Assess the methodology, reasoning, evidence,
limitations and scientific conclusions.

Return your review as JSON.
"""

        response = self.client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {
                    "role": "system",
                    "content": self._system_prompt(),
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.4,
            max_tokens=1200,
        )

        raw = response.choices[0].message.content

        if not raw:
            raise ValueError(
                f"Recenzent {self.profile.id} zwrócił pustą odpowiedź"
            )

        clean = raw.strip()

        # Obsługa ewentualnych bloków ```json ... ```
        if clean.startswith("```"):
            lines = clean.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            clean = "\n".join(lines).strip()

        try:
            parsed = json.loads(clean)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Niepoprawny JSON od recenzenta "
                f"{self.profile.id}: {exc}"
            ) from exc

        if not isinstance(parsed, dict):
            raise ValueError(
                "Odpowiedź recenzenta musi być obiektem JSON"
            )

        # Identyfikatory ustawia aplikacja, nie model LLM.
        # Pydantic sprawdzi recommendation i severity.
        return Review.model_validate({
            "paper_id": paper.id,
            "reviewer_id": self.profile.id,
            "recommendation": parsed.get("recommendation"),
            "issues": parsed.get("issues", []),
            "justification": parsed.get("justification", ""),
        })
