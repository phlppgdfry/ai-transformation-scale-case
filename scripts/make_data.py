"""Generate the synthetic engagement data for Ardena Group.

Hand-written facts (business units, initiatives, use cases, foundations,
competitors) live in this file; survey answers and pilot measurements are
drawn from a seeded generator, so every run gives the same files. CI runs
``--check`` and fails if the committed data differs.

Ardena Group, its people, stores, competitors and numbers are fictional.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data"
SEED = 20261022

CLIENT = {
    "name": "Ardena Group",
    "domain": "ardena.example",
    "sector": "Grocery retail and distribution, Belgium",
    "revenue_eur_m": 3600,
    "ebit_margin": 0.028,
    "employees": 11000,
    "business_units": {
        "stores": {"label": "Stores", "detail": "240 supermarkets", "employees": 8200},
        "supply": {"label": "Supply chain", "detail": "3 distribution centres, own fleet", "employees": 1600},
        "ecom": {"label": "E-commerce", "detail": "Home delivery and click & collect", "employees": 450},
        "office": {"label": "Head office", "detail": "Finance, HR, marketing, IT, customer service", "employees": 750},
    },
    "fresh_sales_share": 0.34,
}

DIMENSIONS = [
    ("strategy", "Strategy and leadership", [
        "Leadership has stated what AI should achieve for the business, in measurable terms.",
        "AI initiatives are funded through a portfolio decision, not ad hoc budgets.",
        "Business units know which AI bets the group makes and which it does not.",
        "There is an executive owner for AI with the mandate to stop initiatives.",
    ]),
    ("governance", "Governance and risk", [
        "There is an approved AI policy that staff know and use.",
        "All AI systems in use are in an inventory with an owner and a risk tier.",
        "New AI use goes through an intake with a proportionate risk review.",
        "EU AI Act and GDPR obligations are assessed per system.",
    ]),
    ("data", "Data foundations", [
        "Sales, stock and waste data are available at item-store-day level within 24 hours.",
        "Product master data is complete and trusted.",
        "Data ownership and quality rules are defined for key domains.",
        "Teams can get governed access to data without months of requests.",
    ]),
    ("platform", "Technology and platform", [
        "There is a sanctioned way to use foundation models (gateway, contracts, logging).",
        "Models and AI features are monitored in production.",
        "Reusable components (search, document processing, agents' tools) exist and are shared.",
        "Security reviews for AI vendors and tools are routine.",
    ]),
    ("skills", "Skills and talent", [
        "Staff who use AI have had basic AI literacy training.",
        "There are people who can design, build and evaluate AI solutions in-house or with partners.",
        "Product owners can write success criteria for an AI use case.",
        "There is a network of AI champions in the business.",
    ]),
    ("adoption", "Ways of working and adoption", [
        "Frontline staff are involved in designing AI tools they will use.",
        "Pilots have a plan for production and support from the start.",
        "Change management is part of AI projects.",
        "People trust AI suggestions enough to use them, and know when not to.",
    ]),
    ("value", "Value management", [
        "Every AI initiative has a baseline and an outcome KPI.",
        "Benefits are tracked after go-live.",
        "Initiatives that do not deliver are stopped.",
        "Cost of AI (licences, cloud, people) is visible per initiative.",
    ]),
]

# The "true" maturity per business unit and dimension (1-5) that the survey
# answers are drawn around. Discovery interviews are summarised in
# docs/01-readiness/maturity-assessment.md.
TRUE_LEVEL = {
    "stores": {"strategy": 1.8, "governance": 1.4, "data": 2.4, "platform": 1.6, "skills": 1.5, "adoption": 1.9, "value": 1.7},
    "supply": {"strategy": 2.4, "governance": 1.8, "data": 3.1, "platform": 2.6, "skills": 2.5, "adoption": 2.6, "value": 2.7},
    "ecom": {"strategy": 2.9, "governance": 2.0, "data": 3.0, "platform": 3.1, "skills": 3.2, "adoption": 2.8, "value": 2.6},
    "office": {"strategy": 2.2, "governance": 1.9, "data": 2.0, "platform": 2.2, "skills": 2.1, "adoption": 1.8, "value": 1.6},
}
TARGET = {"strategy": 3.5, "governance": 3.5, "data": 3.5, "platform": 3.5, "skills": 3.0, "adoption": 3.0, "value": 3.5}
RESPONDENTS = {"stores": 9, "supply": 6, "ecom": 5, "office": 8}

# Existing AI efforts found in discovery: (id, name, bu, kind, owner, evidence,
# data_access, personal_data, monthly_cost_eur, age_months, duplicate_of, note)
INITIATIVES = [
    ("I-01", "Vendor demand-forecasting module", "supply", "production", True, "measured", "ok", False, 9500, 30, None, "Live in 3 DCs; forecast error down 11% vs. old method"),
    ("I-02", "Store fresh-waste dashboard with ML alerts", "stores", "pilot", True, "anecdotal", "partial", False, 1800, 14, None, "12 stores; managers like it; nobody measured waste"),
    ("I-03", "ChatGPT accounts paid on credit cards (marketing)", "office", "shadow-tool", False, "none", "ok", True, 640, 11, None, "Customer data pasted for campaign copy"),
    ("I-04", "Copilot licences for 120 office users", "office", "vendor-feature", True, "anecdotal", "ok", True, 3600, 7, None, "Usage 34% after 3 months"),
    ("I-05", "Customer-service email triage (vendor add-on)", "office", "pilot", True, "measured", "ok", True, 2100, 9, None, "Handling time -18% in pilot team"),
    ("I-06", "Second email-triage tool (e-com team)", "ecom", "pilot", False, "none", "ok", True, 900, 5, "I-05", "Started independently of I-05"),
    ("I-07", "Route optimisation for home delivery", "ecom", "production", True, "measured", "ok", True, 4200, 26, None, "Vendor SaaS; 9% fewer km per order"),
    ("I-08", "Shelf-image recognition PoC", "stores", "pilot", False, "none", "blocked", False, 0, 19, None, "Vendor PoC ended; no data feed from stores"),
    ("I-09", "HR CV-screening plug-in in the ATS", "office", "vendor-feature", True, "none", "ok", True, 750, 6, None, "Switched on by default by the vendor"),
    ("I-10", "Supplier invoice extraction", "office", "pilot", True, "measured", "partial", False, 1300, 8, None, "Finance: 62% straight-through on 2 suppliers"),
    ("I-11", "Promotion-uplift model (data science team)", "office", "pilot", True, "anecdotal", "partial", False, 0, 22, None, "Notebook; used twice for planning"),
    ("I-12", "Generative product descriptions for webshop", "ecom", "pilot", True, "measured", "ok", False, 600, 6, None, "Copywriting time -60% on 800 SKUs"),
    ("I-13", "Store staff scheduling optimiser", "stores", "pilot", True, "anecdotal", "partial", True, 2800, 10, None, "4 stores; union not yet consulted"),
    ("I-14", "DC pick-path optimisation", "supply", "pilot", True, "measured", "ok", False, 1500, 12, None, "Walking distance -7% in one DC"),
    ("I-15", "Chatbot on website (FAQ)", "ecom", "production", True, "anecdotal", "ok", True, 1100, 20, None, "Containment rate unknown"),
    ("I-16", "Personal ChatGPT use in IT (code)", "office", "shadow-tool", False, "none", "ok", False, 0, 12, None, "Source code pasted into personal accounts"),
    ("I-17", "Energy optimisation for store refrigeration", "stores", "vendor-feature", True, "measured", "ok", False, 2400, 15, None, "Energy -6% in 30 stores"),
    ("I-18", "Loss-prevention video analytics PoC", "stores", "pilot", False, "none", "partial", True, 0, 9, None, "Camera analytics on customers; no DPIA"),
    ("I-19", "Second invoice-extraction trial (accounts payable)", "office", "pilot", False, "none", "partial", False, 400, 4, "I-10", "Different vendor, same documents"),
    ("I-20", "Markdown price suggestions (spreadsheet + model)", "stores", "pilot", True, "anecdotal", "partial", False, 0, 7, "I-02", "One regional manager's model"),
    ("I-21", "Contract review assistant (legal)", "office", "shadow-tool", False, "none", "ok", True, 180, 5, None, "Supplier contracts in a free online tool"),
    ("I-22", "Transport ETA prediction", "supply", "pilot", True, "anecdotal", "ok", False, 900, 8, None, "Trucks to DCs; not used by DC planning yet"),
    ("I-23", "Product master-data enrichment", "office", "pilot", True, "measured", "partial", False, 700, 5, None, "Attribute completeness 61% → 84% on 2,000 SKUs"),
    ("I-24", "Meeting summaries (various tools)", "office", "shadow-tool", False, "none", "ok", True, 300, 8, None, "Five different tools in use"),
    ("I-25", "Customer churn model (loyalty card)", "ecom", "pilot", True, "none", "ok", True, 0, 16, None, "Model built; no campaign ever used it"),
    ("I-26", "Fleet predictive maintenance", "supply", "vendor-feature", True, "anecdotal", "ok", False, 1200, 11, None, "Alerts arrive; workshop ignores half"),
    ("I-27", "IT service-desk ticket routing", "office", "pilot", True, "measured", "ok", False, 500, 6, None, "First-time-right routing 71% → 88%"),
    ("I-28", "Recipe recommender in app", "ecom", "pilot", True, "anecdotal", "ok", True, 800, 9, None, "Click-through up; basket impact unknown"),
    ("I-29", "Second recipe recommender (marketing agency)", "office", "pilot", False, "none", "ok", True, 2000, 4, "I-28", "Agency proposal, separate budget"),
    ("I-30", "Supplier risk news monitoring", "office", "vendor-feature", True, "none", "ok", False, 450, 3, None, "Alerts nobody reads"),
    ("I-31", "Store-level demand forecasting trial", "stores", "pilot", True, "measured", "partial", False, 1600, 13, None, "Forecast error -9% in 20 stores; feeds no ordering"),
    ("I-32", "Employee HR-policy chatbot", "office", "pilot", True, "anecdotal", "ok", True, 600, 5, None, "HR likes it; answers not checked"),
    ("I-33", "Customer-review sentiment analysis", "ecom", "vendor-feature", True, "anecdotal", "ok", False, 350, 10, None, "Monthly report"),
    ("I-34", "Code assistant pilot (IT, sanctioned)", "office", "pilot", True, "measured", "ok", False, 1900, 4, None, "Licensed tool; 40 developers"),
    ("I-35", "Shrinkage anomaly detection (finance)", "office", "pilot", False, "none", "partial", False, 0, 14, None, "Analyst left; model unused"),
    ("I-36", "Voice ordering for B2B customers", "ecom", "pilot", False, "none", "ok", True, 0, 6, None, "Hackathon prototype"),
    ("I-37", "Translation of product labels (FR/NL/DE)", "office", "shadow-tool", True, "anecdotal", "ok", False, 90, 9, None, "Free web tool; quality unchecked"),
]

FOUNDATIONS = [
    {"id": "F1", "name": "Retail data platform", "detail": "Sales, stock and waste at item-store-day, within 24 h, with owners and quality rules", "months": 6, "one_off_eur": 420000, "run_eur": 160000},
    {"id": "F2", "name": "AI orchestration layer", "detail": "Model gateway, approved model catalogue, tool registry, evaluation and monitoring, cost per initiative", "months": 4, "one_off_eur": 240000, "run_eur": 120000},
    {"id": "F3", "name": "AI governance and policy", "detail": "AI council, policy, intake, inventory, risk tiers, EU AI Act register", "months": 3, "one_off_eur": 90000, "run_eur": 60000},
    {"id": "F4", "name": "Product master-data quality", "detail": "Attribute completeness and ownership for 28,000 SKUs", "months": 5, "one_off_eur": 180000, "run_eur": 50000},
    {"id": "F5", "name": "AI literacy and champions", "detail": "Article 4 literacy for all users, 60 champions, product-owner training", "months": 3, "one_off_eur": 110000, "run_eur": 70000},
]

# Use cases from the workshop series. value: annual benefit range (EUR),
# fit: strategic fit 1-5, data/tech/org: feasibility 1-5, effort: months,
# diff: commodity | parity | differentiating, source: buy | configure | build,
# tier: EU AI Act triage input (see aitx/governance.py), needs: foundations.
USE_CASES = [
    ("UC-01", "Fresh markdown advisor", "stores", "Suggests markdowns on fresh items near expiry per store; staff confirm.", (1_400_000, 2_600_000), 5, 3, 4, 4, 4, "differentiating", "build", "minimal", ["F1", "F3", "F5"], "I-02,I-20", "Head of fresh", "Fresh waste % of fresh sales"),
    ("UC-02", "Store-level automated ordering", "stores", "Store demand forecast feeds replenishment orders.", (2_500_000, 4_500_000), 5, 2, 3, 2, 9, "differentiating", "build", "minimal", ["F1", "F2", "F3", "F4"], "I-31", "Director supply planning", "Availability and stock days"),
    ("UC-03", "Customer-service assistant (one tool)", "office", "Triage and draft replies in one sanctioned tool for all teams.", (420_000, 650_000), 3, 4, 5, 4, 3, "parity", "configure", "limited", ["F2", "F3"], "I-05,I-06", "Head of customer service", "Handling time and first-contact resolution"),
    ("UC-04", "Supplier invoice processing at scale", "office", "Extraction and matching for all suppliers.", (380_000, 520_000), 3, 4, 4, 4, 4, "commodity", "buy", "minimal", ["F3"], "I-10,I-19", "CFO", "Straight-through rate and cost per invoice"),
    ("UC-05", "Personalised promotions in the app", "ecom", "Offers per customer from loyalty data.", (1_800_000, 3_200_000), 5, 3, 3, 2, 8, "differentiating", "build", "limited", ["F1", "F2", "F3"], "I-25,I-28", "CMO", "Incremental margin per active customer"),
    ("UC-06", "Product content generation (web and labels)", "ecom", "Descriptions and translations from master data, reviewed.", (300_000, 450_000), 3, 4, 5, 4, 2, "parity", "configure", "limited", ["F2", "F3", "F4"], "I-12,I-37", "Head of e-commerce", "Time to publish new SKU"),
    ("UC-07", "DC labour planning", "supply", "Forecast work per DC shift from inbound and orders.", (700_000, 1_100_000), 4, 3, 3, 3, 5, "parity", "configure", "limited", ["F1", "F3"], "I-14,I-22", "DC operations director", "Overtime hours and productivity"),
    ("UC-08", "Store staff scheduling", "stores", "Schedules from forecast footfall; employee preferences.", (900_000, 1_500_000), 4, 2, 3, 2, 6, "parity", "buy", "review", ["F1", "F3", "F5"], "I-13", "HR director", "Schedule fit and overtime"),
    ("UC-09", "Office productivity assistant", "office", "Sanctioned assistant for writing, summaries, meetings.", (250_000, 600_000), 2, 5, 5, 3, 2, "commodity", "buy", "minimal", ["F2", "F3", "F5"], "I-03,I-04,I-24", "CIO", "Weekly active use and time saved (survey)"),
    ("UC-10", "Developer assistant for all IT", "office", "Extend the sanctioned code assistant.", (200_000, 320_000), 2, 5, 5, 4, 1, "commodity", "buy", "minimal", ["F3"], "I-16,I-34", "CIO", "Lead time for changes"),
    ("UC-11", "Promotion planning optimiser", "office", "Uplift and cannibalisation per promo, before planning.", (1_100_000, 2_000_000), 4, 3, 3, 2, 6, "differentiating", "build", "minimal", ["F1", "F2"], "I-11", "Commercial director", "Promo ROI"),
    ("UC-12", "Refrigeration energy optimisation (all stores)", "stores", "Roll out the vendor module to 240 stores.", (520_000, 700_000), 3, 4, 5, 4, 3, "commodity", "buy", "minimal", ["F3"], "I-17", "Facilities director", "kWh per m2"),
    ("UC-13", "Fleet predictive maintenance (fix)", "supply", "Make alerts actionable in the workshop process.", (180_000, 300_000), 2, 4, 4, 3, 3, "commodity", "configure", "minimal", ["F3"], "I-26", "Fleet manager", "Unplanned downtime"),
    ("UC-14", "IT service-desk automation", "office", "Routing plus self-service answers.", (150_000, 240_000), 2, 4, 5, 4, 2, "commodity", "configure", "minimal", ["F2", "F3"], "I-27", "CIO", "Tickets resolved without agent"),
    ("UC-15", "HR policy assistant (checked)", "office", "Answers on HR policies with sources and review.", (90_000, 160_000), 2, 4, 5, 4, 2, "commodity", "configure", "limited", ["F2", "F3"], "I-32", "HR director", "HR questions handled without a ticket"),
    ("UC-16", "Customer churn and win-back", "ecom", "Use the model in campaigns, measured with holdouts.", (500_000, 900_000), 3, 4, 4, 3, 3, "parity", "build", "limited", ["F3"], "I-25", "CMO", "Win-back rate vs. holdout"),
    ("UC-17", "Product master-data enrichment", "office", "Fill missing attributes with review.", (260_000, 420_000), 3, 3, 4, 4, 3, "parity", "configure", "minimal", ["F3", "F4"], "I-23", "Head of master data", "Attribute completeness"),
    ("UC-18", "Store operations copilot", "stores", "Answers on procedures, planograms, recalls for store staff.", (600_000, 1_200_000), 4, 2, 4, 3, 6, "differentiating", "build", "limited", ["F2", "F3", "F5"], None, "COO stores", "Time to resolve store questions"),
    ("UC-19", "Loss-prevention video analytics", "stores", "Detect theft patterns from customer video.", (400_000, 900_000), 3, 2, 3, 1, 8, "parity", "buy", "review", ["F3"], "I-18", "Security director", "Shrink %"),
    ("UC-20", "Supplier contract analysis", "office", "Clause extraction and risk flags, sanctioned tool.", (120_000, 200_000), 2, 4, 4, 3, 3, "commodity", "buy", "minimal", ["F2", "F3"], "I-21", "General counsel", "Review time per contract"),
    ("UC-21", "Shrinkage anomaly detection", "office", "Flag store-item anomalies for investigation.", (300_000, 600_000), 3, 3, 4, 3, 4, "parity", "build", "minimal", ["F1", "F3"], "I-35", "CFO", "Recovered shrink"),
    ("UC-22", "CV screening in recruitment", "office", "Rank applicants for store jobs.", (150_000, 250_000), 2, 4, 4, 2, 2, "commodity", "buy", "high", ["F3"], "I-09", "HR director", "Time to hire"),
    ("UC-23", "Delivery-slot pricing", "ecom", "Price home-delivery slots by demand and route cost.", (700_000, 1_300_000), 4, 3, 3, 3, 5, "differentiating", "build", "minimal", ["F1", "F2"], "I-07", "Head of e-commerce", "Delivery cost per order"),
    ("UC-24", "Voice ordering for B2B", "ecom", "Phone ordering for horeca customers.", (60_000, 140_000), 1, 3, 3, 2, 5, "parity", "build", "limited", ["F2", "F3"], "I-36", "B2B sales manager", "Orders by voice"),
    ("UC-25", "Supplier risk monitoring (fix)", "office", "Route alerts to category managers with actions.", (50_000, 120_000), 2, 4, 4, 2, 2, "commodity", "configure", "minimal", ["F3"], "I-30", "CPO", "Risk events acted on"),
    ("UC-26", "Review insights for category managers", "ecom", "Themes from reviews per category, monthly.", (80_000, 150_000), 2, 4, 5, 3, 2, "commodity", "configure", "minimal", ["F2", "F3"], "I-33", "Category director", "Actions from insights"),
]

COMPETITORS = [
    {"name": "Volta Markt", "position": "Discount, 310 stores", "ai_moves": ["Fully automated store ordering", "Electronic shelf labels with dynamic pricing in 2027", "Minimal personalisation"]},
    {"name": "Grenvale", "position": "Premium, strong e-commerce", "ai_moves": ["Personalised offers in app (launched 2025)", "Recipe and meal-planning assistant", "Same-day delivery pricing by slot"]},
    {"name": "BuurtBox", "position": "Quick commerce, city centres", "ai_moves": ["Dark-store picking automation", "Demand sensing per neighbourhood"]},
]

# Markdown pilot design: matched store pairs, 8 baseline + 10 pilot weeks.
PILOT = {
    "use_case": "UC-01",
    "pairs": 12,
    "baseline_weeks": 8,
    "pilot_weeks": 10,
    "criteria": {
        "primary": {"kpi": "waste_pct", "direction": "down", "min_effect_pp": 0.5, "ci_lower_bound_pp": 0.2},
        "guardrails": [
            {"kpi": "fresh_margin_pct", "max_worse_pp": 0.10},
            {"kpi": "oos_pct", "max_worse_pp": 0.30},
        ],
        "adoption": {"kpi": "suggestions_accepted_pct", "min": 60.0},
    },
}


def survey(rng: random.Random) -> list[dict]:
    rows = []
    for bu, n in RESPONDENTS.items():
        for r in range(n):
            answers = {}
            for dim, _, statements in DIMENSIONS:
                base = TRUE_LEVEL[bu][dim]
                for i, _ in enumerate(statements):
                    raw = base + rng.gauss(0, 0.7) + (0.3 if i == 0 else 0) - (0.2 if i == 3 else 0)
                    answers[f"{dim}.{i + 1}"] = max(1, min(5, round(raw)))
            rows.append({"respondent": f"{bu}-{r + 1:02d}", "bu": bu, "answers": answers})
    return rows


def pilot_data(rng: random.Random) -> list[dict]:
    rows = []
    weeks = PILOT["baseline_weeks"] + PILOT["pilot_weeks"]
    for p in range(PILOT["pairs"]):
        pair_base = rng.uniform(3.9, 5.4)  # matched on fresh waste level
        margin_base = rng.uniform(24.0, 27.5)
        oos_base = rng.uniform(2.2, 3.4)
        for arm in ("pilot", "control"):
            store = f"S{100 + p * 2 + (arm == 'control')}"
            store_fx = rng.gauss(0, 0.25)
            for w in range(weeks):
                season = 0.35 * (w >= 11)  # warm weeks push waste up in both arms
                treated = arm == "pilot" and w >= PILOT["baseline_weeks"]
                ramp = min(1.0, (w - PILOT["baseline_weeks"] + 1) / 3) if treated else 0.0
                waste = pair_base + store_fx + season - 0.95 * ramp + rng.gauss(0, 0.35)
                margin = margin_base + store_fx * 0.5 + 0.12 * ramp + rng.gauss(0, 0.30)
                oos = oos_base + 0.05 * ramp + rng.gauss(0, 0.25)
                row = {"pair": p + 1, "store": store, "arm": arm, "week": w + 1,
                       "phase": "pilot" if w >= PILOT["baseline_weeks"] else "baseline",
                       "waste_pct": round(waste, 3), "fresh_margin_pct": round(margin, 3), "oos_pct": round(oos, 3)}
                if treated:
                    row["suggestions"] = rng.randint(140, 260)
                    row["accepted"] = round(row["suggestions"] * min(0.92, rng.uniform(0.55, 0.80) + 0.03 * (w - 8)))
                rows.append(row)
    return rows


def build() -> dict[str, object]:
    rng = random.Random(SEED)
    return {
        "client.json": CLIENT,
        "assessment.json": {"dimensions": [{"id": d, "name": n, "statements": s} for d, n, s in DIMENSIONS],
                            "target": TARGET, "responses": survey(rng)},
        "initiatives.json": [dict(zip(["id", "name", "bu", "kind", "owner", "evidence", "data_access", "personal_data",
                                       "monthly_cost_eur", "age_months", "duplicate_of", "note"], row)) for row in INITIATIVES],
        "foundations.json": FOUNDATIONS,
        "use_cases.json": [
            {"id": u[0], "name": u[1], "bu": u[2], "description": u[3], "value_low": u[4][0], "value_high": u[4][1],
             "fit": u[5], "data": u[6], "tech": u[7], "org": u[8], "effort_months": u[9], "differentiation": u[10],
             "sourcing": u[11], "ai_act_input": u[12], "needs": u[13], "from_initiatives": u[14].split(",") if u[14] else [],
             "owner": u[15], "kpi": u[16]}
            for u in USE_CASES
        ],
        "competitors.json": COMPETITORS,
        "pilot_design.json": PILOT,
        "pilot_measurements.json": pilot_data(rng),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    stale = []
    for name, obj in build().items():
        text = json.dumps(obj, indent=1, ensure_ascii=False) + "\n"
        path = OUT / name
        if path.exists() and path.read_text(encoding="utf-8") == text:
            continue
        if args.check:
            stale.append(name)
        else:
            path.write_text(text, encoding="utf-8")
            print(f"wrote data/{name}")
    for s in stale:
        print(f"stale: data/{s} (run python3 scripts/make_data.py)")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
