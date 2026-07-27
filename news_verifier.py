# v0.3.0
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json
import typing


class NewsVerifier(gl.Contract):
    claim: str
    verdict: str
    reasoning: str
    is_verified: bool

    def __init__(self):
        self.claim = ""
        self.verdict = "PENDING"
        self.reasoning = ""
        self.is_verified = False

    @gl.public.view
    def get_status(self) -> dict:
        return {
            "claim": self.claim,
            "verdict": self.verdict,
            "reasoning": self.reasoning,
            "is_verified": self.is_verified,
        }

    @gl.public.write
    def verify_claim(self, claim: str) -> None:
        # Reset state for this run
        self.claim = claim
        self.is_verified = False
        self.verdict = "PENDING"
        self.reasoning = ""

        # This function does the LLM work. It mirrors your original get_verdict()
        # pattern (fn calls exec_prompt), so the change from your working code is
        # small — we only swap strict_eq for prompt_comparative and ask for JSON.
        def fact_check() -> str:
            task = (
                'You are a careful fact-checker. Assess this claim based on '
                'well-established, widely-known facts:\n\n'
                f'CLAIM: "{claim}"\n\n'
                'Respond with ONLY a JSON object, no markdown fences, exactly:\n'
                '{"verdict": "TRUE" | "FALSE" | "UNVERIFIABLE", '
                '"reasoning": "one clear sentence explaining the verdict"}'
            )
            return gl.nondet.exec_prompt(task)

        # prompt_comparative: validators use NLP to check the leader's answer is
        # equivalent, so free-text reasoning can still reach consensus.
        raw = gl.eq_principle.prompt_comparative(
            fact_check,
            principle=(
                "Two results are equivalent if they reach the same verdict "
                "(TRUE, FALSE, or UNVERIFIABLE) and give reasoning that is "
                "consistent in meaning, even if worded differently."
            ),
        )

        verdict, reasoning = self._parse(raw)
        self.verdict = verdict
        self.reasoning = reasoning
        self.is_verified = True

    def _parse(self, raw: str) -> typing.Tuple[str, str]:
        """Turn the model's raw string into (verdict, reasoning) safely."""
        text = (raw or "").strip()

        # Strip accidental code fences like ```json ... ```
        if text.startswith("```"):
            text = text.strip("`")
            if text[:4].lower() == "json":
                text = text[4:]
            text = text.strip()

        verdict = "UNVERIFIABLE"
        reasoning = ""

        try:
            data = json.loads(text)
            verdict = str(data.get("verdict", "UNVERIFIABLE")).upper().strip()
            reasoning = str(data.get("reasoning", "")).strip()
        except Exception:
            # Fallback: pull a verdict word out of plain text
            upper = text.upper()
            for word in ("TRUE", "FALSE", "UNVERIFIABLE"):
                if word in upper:
                    verdict = word
                    break
            reasoning = text

        if verdict not in ("TRUE", "FALSE", "UNVERIFIABLE"):
            verdict = "UNVERIFIABLE"
        if not reasoning:
            reasoning = "The model did not return a usable explanation."

        return verdict, reasoning
