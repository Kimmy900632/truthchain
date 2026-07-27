# v0.4.1
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
from dataclasses import dataclass
import json
import typing


# A per-claim record. @allow_storage makes the dataclass storable inside a TreeMap.
@allow_storage
@dataclass
class VerdictRecord:
    claim: str
    verdict: str
    reasoning: str
    source_url: str
    is_verified: bool


class NewsVerifier(gl.Contract):
    # Per-claim storage keyed by the claim text. Concurrent verifications
    # each get their own entry, so results are never overwritten or confused.
    records: TreeMap[str, VerdictRecord]
    total_verified: u256

    def __init__(self):
        self.total_verified = u256(0)

    # -- Reads ---------------------------------------------------------------

    @gl.public.view
    def get_status(self, claim: str) -> dict:
        """Return the stored verdict for a specific claim."""
        rec = self.records.get(claim.strip(), None)
        if rec is None:
            return {
                "claim": claim,
                "verdict": "NOT_FOUND",
                "reasoning": "This claim has not been verified yet.",
                "source_url": "",
                "is_verified": False,
            }
        return {
            "claim": rec.claim,
            "verdict": rec.verdict,
            "reasoning": rec.reasoning,
            "source_url": rec.source_url,
            "is_verified": rec.is_verified,
        }

    @gl.public.view
    def get_total_verified(self) -> int:
        return self.total_verified

    # -- Write ---------------------------------------------------------------

    @gl.public.write
    def verify_claim(self, claim: str) -> None:
        claim = claim.strip()

        # STEP 1 — Retrieve an attributable source.
        # Search Wikipedia for the most relevant article for this claim.
        def find_source() -> str:
            query = claim.replace(" ", "%20")
            search_url = (
                "https://en.wikipedia.org/w/rest.php/v1/search/page?q="
                + query + "&limit=1"
            )
            return gl.nondet.web.render(search_url, mode="text")

        # strict_eq: validators must agree the retrieved content is identical.
        search_raw = gl.eq_principle.strict_eq(find_source)

        source_title = ""
        try:
            data = json.loads(search_raw)
            pages = data.get("pages", [])
            if pages:
                source_title = pages[0].get("key") or pages[0].get("title") or ""
        except Exception:
            source_title = ""

        # STEP 2 — Insufficient evidence is a deliberate outcome, not a fallback.
        if not source_title:
            self.records[claim] = VerdictRecord(
                claim,
                "UNVERIFIABLE",
                "No attributable source was found to support or refute this claim.",
                "",
                True,
            )
            self.total_verified = u256(self.total_verified + 1)
            return

        source_url = "https://en.wikipedia.org/wiki/" + source_title

        # STEP 3 — Fetch the actual source page as evidence.
        def fetch_page() -> str:
            return gl.nondet.web.render(source_url, mode="text")

        evidence = gl.eq_principle.strict_eq(fetch_page)
        evidence = (evidence or "")[:5000]

        # STEP 4 — Rule on the claim using ONLY the retrieved evidence.
        def rule() -> str:
            task = (
                "You are a fact-checker. Assess the CLAIM using ONLY the EVIDENCE "
                "below, taken from a Wikipedia article. Do not use outside knowledge.\n\n"
                f'CLAIM: "{claim}"\n\n'
                f"EVIDENCE:\n{evidence}\n\n"
                "Rules:\n"
                "- If the evidence clearly supports the claim: verdict = TRUE.\n"
                "- If the evidence clearly contradicts the claim: verdict = FALSE.\n"
                "- If the evidence does not address the claim or is insufficient: "
                "verdict = UNVERIFIABLE.\n\n"
                "Respond with ONLY a JSON object, no markdown fences:\n"
                '{"verdict": "TRUE" | "FALSE" | "UNVERIFIABLE", '
                '"reasoning": "one sentence citing what the evidence shows"}'
            )
            return gl.nondet.exec_prompt(task)

        # prompt_comparative: validators judge whether rulings are equivalent in
        # meaning, so evidence-grounded free-text reasoning can reach consensus.
        raw = gl.eq_principle.prompt_comparative(
            rule,
            principle=(
                "Two results are equivalent if they reach the same verdict "
                "(TRUE, FALSE, or UNVERIFIABLE) and their reasoning is consistent "
                "with the same evidence, even if worded differently."
            ),
        )

        verdict, reasoning = self._parse(raw)
        self.records[claim] = VerdictRecord(
            claim, verdict, reasoning, source_url, True
        )
        self.total_verified = u256(self.total_verified + 1)

    # -- Helpers -------------------------------------------------------------

    def _parse(self, raw: str) -> typing.Tuple[str, str]:
        text = (raw or "").strip()

        # Strip markdown fences like ```json ... ```
        if text.startswith("```"):
            text = text.strip("`")
            if text[:4].lower() == "json":
                text = text[4:]
            text = text.strip()

        verdict = "UNVERIFIABLE"
        reasoning = ""

        # Try clean JSON first; if that fails, slice from first '{' to last '}'
        # (handles the model wrapping or double-encoding its answer).
        parsed = None
        try:
            parsed = json.loads(text)
        except Exception:
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1 and end > start:
                try:
                    parsed = json.loads(text[start:end + 1])
                except Exception:
                    parsed = None

        if isinstance(parsed, dict):
            verdict = str(parsed.get("verdict", "UNVERIFIABLE")).upper().strip()
            reasoning = str(parsed.get("reasoning", "")).strip()
        else:
            upper = text.upper()
            for word in ("TRUE", "FALSE", "UNVERIFIABLE"):
                if word in upper:
                    verdict = word
                    break
            reasoning = text

        # Clean stray escapes/quotes if any survived.
        reasoning = reasoning.replace('\\"', '"').strip().strip('"').strip()

        if verdict not in ("TRUE", "FALSE", "UNVERIFIABLE"):
            verdict = "UNVERIFIABLE"
        if not reasoning:
            reasoning = "No usable explanation was produced."
        return verdict, reasoning

