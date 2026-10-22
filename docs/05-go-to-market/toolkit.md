# Toolkit

Templates and tools used in this engagement, ready for the next one.

| Tool | What | Where |
|---|---|---|
| Maturity survey | 7 dimensions × 4 statements, scoring code | `data/assessment.json`, `aitx/readiness.py` |
| Initiative triage | Rules as code, one reason per initiative | `aitx/inventory.py` |
| Use-case canvas | One page per idea (below) | This page |
| Scoring model with robustness test | Weights file, 2,000 re-weightings | `data/weights.json`, `aitx/portfolio.py` |
| Growth map | Interactive value × feasibility map | `site/growth-map/` |
| Roadmap sequencer | Dependencies and capacity checked | `aitx/roadmap.py` |
| Value model | NPV per use case and portfolio, haircut, ramp | `aitx/value.py`, `data/finance.json` |
| AI Act triage | First-pass tier and duties | `aitx/governance.py` |
| Pilot charter template | Hypothesis, design, pre-registered criteria | [pilot charter](../04-applied-ai/pilot-charter.md) |
| Pilot evaluation | Difference-in-differences, bootstrap | `aitx/pilot.py` |
| Production gates | 12 gates with owners | `data/production_gates.json`, `aitx/production.py` |
| AI policy (one page), principles, RACI | Governance starter kit | `docs/01-readiness/` |

## Use-case canvas

| Field | Question |
|---|---|
| Name and owner | Who in the business wants this and will own the result? |
| Process and pain | Which process, and what goes wrong today (waiting, rework, guessing, copying)? |
| What AI does | Predict, classify, draft, search, extract, recommend, act? |
| Who uses it, and how | In which tool, at which moment, with which decision left to a person? |
| Value | Annual value range, and how it is calculated |
| Outcome KPI and baseline | How do we know it worked? What is the number today? |
| Data | Which data, where, in what quality, who owns it? |
| Risks | People affected, personal data, AI Act tier, what if it is wrong? |
| Differentiation | Data only we have? Something customers choose us for? Hard to copy? |
| Sourcing | Buy, configure or build? |
| Effort | Rough months and team |
