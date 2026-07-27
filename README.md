# TruthChain — On-Chain Fake News Detector
> Built on GenLayer | AI-powered fact-checking with attributable evidence, recorded on-chain

## What is TruthChain?
TruthChain is a decentralized fact-checking platform where anyone can submit a news claim and have it verified by AI — grounded in a real, citable source and recorded on-chain.

Rather than trusting a black-box AI, TruthChain's Intelligent Contract retrieves an attributable source (a Wikipedia article), rules on the claim using only that evidence, and reaches a verdict through GenLayer validator consensus. Every verdict is stored with the source URL it was based on.

## How it Works
1. User submits a claim (e.g. "Elon Musk owns Twitter")
2. The Intelligent Contract searches Wikipedia and retrieves the most relevant article as evidence (under strict-equivalence consensus, so validators agree on the source)
3. The LLM rules on the claim using only that evidence, returning TRUE, FALSE, or UNVERIFIABLE with a one-sentence justification
4. Validators reach consensus on the ruling (comparative equivalence, so evidence-grounded reasoning can agree in meaning)
5. The verdict, reasoning, and source URL are stored on-chain, keyed by claim

## Key Design Points
- **Attributable evidence:** Verdicts are grounded in a retrieved Wikipedia article, and the `source_url` is stored with every result — no ruling from model knowledge alone.
- **Deliberate UNVERIFIABLE:** If no source is found, or the evidence doesn't address the claim, the contract explicitly returns UNVERIFIABLE — a real outcome, not a fallback.
- **Per-claim storage:** State is a `TreeMap[str, VerdictRecord]` keyed by claim, so concurrent verifications never overwrite or confuse each other.

## Project Structure
- `news_verifier.py` — Intelligent Contract (deployed on GenLayer)
- `index.html` — Frontend app
- `README.md`

## Intelligent Contract
**Deployed on the GenLayer Studio network.** (Update with your latest deployed instance address.)

### Methods
| Method | Type | Description |
|---|---|---|
| `verify_claim(claim)` | Write | Retrieves evidence, rules on the claim, and stores the verdict |
| `get_status(claim)` | Read | Returns the stored verdict, reasoning, and source URL for a claim |
| `get_total_verified()` | Read | Returns the number of claims verified so far |

### Stored record (per claim)
| Field | Description |
|---|---|
| `claim` | The claim text |
| `verdict` | TRUE / FALSE / UNVERIFIABLE |
| `reasoning` | One-sentence justification citing the evidence |
| `source_url` | The Wikipedia article used as evidence |
| `is_verified` | Whether verification has completed |

## Tech Stack
- **GenLayer Studio** — Intelligent Contract deployment
- **Python** — Contract language
- **HTML / CSS / JS + genlayer-js** — Frontend
- `gl.nondet.web.render` — Live web retrieval of source evidence
- `gl.nondet.exec_prompt` — LLM reasoning over the retrieved evidence
- `gl.eq_principle.strict_eq` — Consensus on retrieved source content
- `gl.eq_principle.prompt_comparative` — Consensus on evidence-grounded reasoning
- `TreeMap[str, VerdictRecord]` — Per-claim on-chain storage

## Example
`verify_claim("Elon Musk owns Twitter")` →
- **verdict:** TRUE
- **reasoning:** cites that the acquisition closed in October 2022, with Musk becoming owner and CEO
- **source_url:** https://en.wikipedia.org/wiki/Acquisition_of_Twitter_by_Elon_Musk

## How to Run
1. Open the live demo (or `index.html` in a browser)
2. Type any news claim
3. Click **Verify this claim**
4. Wait for GenLayer consensus
5. See the verdict, reasoning, and source, recorded on-chain

## GenLayer Builder Program
Built as part of the **GenLayer Builder Program**.
- Platform: [studio.genlayer.com](https://studio.genlayer.com)
