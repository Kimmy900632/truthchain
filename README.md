# TruthChain — On-Chain Fake News Detector
> Built on GenLayer | AI-powered fact-checking recorded on-chain

## What is TruthChain?
TruthChain is a decentralized fact-checking platform where anyone can submit a news claim and have it verified by AI — with the verdict recorded on-chain.

GenLayer's Intelligent Contract uses LLM reasoning plus validator consensus to determine whether a claim is **TRUE**, **FALSE**, or **UNVERIFIABLE**, and stores a human-readable explanation alongside the verdict.

## How it Works
1. User submits a claim
2. The Intelligent Contract runs LLM reasoning on the claim
3. GenLayer validators reach consensus on the verdict
4. The verdict and reasoning are stored on-chain

## Project Structure
- `news_verifier.py` — Intelligent Contract (deployed on GenLayer)
- `index.html` — Frontend app
- `README.md`

## Intelligent Contract
**Deployed on the GenLayer Studio network:**
`0x2585AEadC307620DE22Ee7576e0018511D9b2Ceb`

### Methods
| Method | Type | Description |
|---|---|---|
| `verify_claim(claim)` | Write | Submits a claim for AI verification |
| `get_status()` | Read | Returns the latest verdict and reasoning |

## Tech Stack
- **GenLayer Studio** — Intelligent Contract deployment
- **Python** — Contract language
- **HTML / CSS / JS + genlayer-js** — Frontend
- `gl.nondet.exec_prompt` — LLM reasoning
- `gl.eq_principle.prompt_comparative` — Validator consensus on free-text output

## How to Run
1. Open the live demo (or `index.html` in a browser)
2. Type any news claim
3. Click **Verify this claim**
4. Wait for GenLayer consensus
5. See the verdict and reasoning, recorded on-chain

## Example Claims Tested
| Claim | Verdict |
|---|---|
| Bitcoin was created in 2009 | TRUE |
| Elon Musk owns Twitter | TRUE |
| The Moon is made of cheese | FALSE |

## GenLayer Builder Program
Built as part of the **GenLayer Builder Program**.
- Platform: [studio.genlayer.com](https://studio.genlayer.com)
- Contract: `0x2585AEadC307620DE22Ee7576e0018511D9b2Ceb`
