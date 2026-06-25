# TruthChain — On-Chain Fake News Detector

> Built on GenLayer | AI-powered fact-checking permanently recorded on the blockchain

## What is TruthChain?

TruthChain is a decentralized fact-checking platform where anyone can submit a news claim and have it verified by AI — with the verdict recorded permanently on-chain.

GenLayer's Intelligent Contract uses web browsing + LLM reasoning + validator consensus to determine if a claim is **TRUE**, **FALSE**, or **UNVERIFIABLE**.

## How it Works

```
User submits claim
       ↓
Intelligent Contract fetches web data
       ↓
AI analyzes and returns verdict
       ↓
GenLayer validators reach consensus
       ↓
Verdict permanently stored on-chain
```

## Project Structure

```
truthchain/
├── news_verifier.py   ← Intelligent Contract (deployed on GenLayer)
├── index.html         ← Frontend app
└── README.md
```

## Intelligent Contract

**Deployed on GenLayer Testnet:**
`0xB4BffeF577e289E8AD2bABC59cFDB153E2B715EA`

### Methods

| Method | Type | Description |
|---|---|---|
| `verify_claim(claim)` | Write | Submits a claim for AI verification |
| `get_status()` | Read | Returns current verdict and reasoning |

## Tech Stack

- **GenLayer Studio** — Intelligent Contract deployment
- **Python** — Contract language
- **HTML/CSS/JS** — Frontend
- `gl.nondet.web.render` — Live web browsing inside the contract
- `gl.nondet.exec_prompt` — LLM reasoning
- `gl.eq_principle.strict_eq` — Validator consensus

## How to Run

1. Open `index.html` in your browser
2. Type any news claim
3. Click **Verify this claim**
4. Wait for GenLayer consensus
5. See the verdict on-chain

## Example Claims Tested

| Claim | Verdict |
|---|---|
| Elon Musk owns Twitter | ✅ TRUE |
| The Eiffel Tower is in Paris | ✅ TRUE |

## GenLayer Builder Program

This project was built as part of the **GenLayer Builder Program**.

- Platform: [studio.genlayer.com](https://studio.genlayer.com)
- Contract: `0xB4BffeF577e289E8AD2bABC59cFDB153E2B715EA`
