# v0.2.16
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
            "is_verified": self.is_verified
        }

    @gl.public.write
    def verify_claim(self, claim: str) -> typing.Any:
        self.claim = claim
        self.is_verified = False
        self.verdict = "PENDING"
        self.reasoning = ""

        def get_verdict() -> str:
            web_data = gl.nondet.web.render(
                "https://en.wikipedia.org/wiki/Elon_Musk",
                mode="text"
            )

            task = f"""
You are a fact-checker. Verify this claim: "{claim}"

Wikipedia content:
{web_data[:3000]}

Reply with ONLY one word: TRUE, FALSE, or UNVERIFIABLE
No punctuation. No explanation. Just one word.
            """

            result = gl.nondet.exec_prompt(task).strip().upper()

            # Extract just the verdict word
            for word in ["TRUE", "FALSE", "UNVERIFIABLE"]:
                if word in result:
                    return word
            return "UNVERIFIABLE"

        # strict_eq works perfectly for a single word
        verdict = gl.eq_principle.strict_eq(get_verdict)

        self.verdict = verdict
        self.reasoning = f"AI verified based on Wikipedia content about: {claim}"
        self.is_verified = True

        return {"verdict": self.verdict, "reasoning": self.reasoning}