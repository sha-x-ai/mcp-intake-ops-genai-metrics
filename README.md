# MCP Intake Ops – GenAI + Metrics Sample Repo

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/9e25384c-a36e-47c1-8a8a-7038b6f5f83a" />


This repository implements an **MCP-connected intake agent** that routes user requests to specialized tools for:

1. Parts search (synthetic aerospace inventory)  
2. Policy checks (lightweight compliance/policy assertions)

It includes:
- A small **multi-agent graph** (Intake → PartsAgent / PolicyAgent) with a deterministic **MockLLM** so you can demo locally without API keys yet keep a clear LLM seam for later.
- A minimal **MCP-like tool layer** (adapters with typed contracts), designed to feel like “USB‑C for AI” connections (FS, DB, API).
- A **metrics tracker** aligned to adoption/impact/cost primitives (utilization, AI-time-saved, HEH, spend) and a reusable **eval harness**.
- A **FastAPI** microservice exposing endpoints to converse with the agent and to retrieve metrics.

> Why it’s relevant: mirrors real **intake + engineering search/policy** scenarios (e.g., aerospace/PLM/supplier compliance) with an enterprise-ready pattern—design guardrails and measurement—sized for interviews and portfolio.

---

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.app:api --reload
```

Open http://127.0.0.1:8000/docs for Swagger. Try `/chat` with:

```json
{
  "user": "vad",
  "message": "Find rivets for A320 wing panel and check policy for export"
}
```

Then view metrics at `/metrics/snapshot`.

---

## Architecture

**Agent Graph**  
IntakeAgent parses intent → dispatches to PartsAgent and/or PolicyAgent → merges answers → returns sources + confidence.

**MCP Layer**  
`mcp/tools.py` exposes *capabilities* with stable contracts; `mcp/server.py` binds capabilities to concrete adapters (CSV store for parts, JSON for policies). Swap with Postgres, Slack, GitHub, etc. later without touching agent logic.

**LLM Boundary**  
`llm/mock_llm.py` returns deterministic intents and summaries. Replace with OpenAI/Anthropic by implementing the same interface.

**Metrics & Eval**  
`metrics/tracker.py` captures utilization (DAU/WAU proxy, tool calls), impact (seconds saved → HEH), and cost (mock spend + agent hourly rate).  
`eval/evaluator.py` runs scripted tasks and prints a compact report.

---

## Repository Layout

```
.
├── README.md
├── requirements.txt
├── src
│   ├── app.py
│   ├── graph.py
│   ├── llm
│   │   └── mock_llm.py
│   ├── agents
│   │   ├── intake_agent.py
│   │   ├── parts_agent.py
│   │   └── policy_agent.py
│   ├── mcp
│   │   ├── tools.py
│   │   └── server.py
│   ├── metrics
│   │   └── tracker.py
│   └── eval
│       └── evaluator.py
├── data
│   ├── parts.csv
│   └── policies.json
└── tests
    └── test_agents.py
```

---

## Roadmap

- Swap MockLLM with a real model provider and retrieval grounding.
- Add LangGraph-style state and guardrails.
- Plug a real MCP server (Postgres, Slack, GitHub) and authN/Z.
- Add human-in-the-loop review queue and risk scoring.
- Dockerfile + GitHub Actions for CI.

---

## License

MIT
