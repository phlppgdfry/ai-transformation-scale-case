"""Evaluation of the fresh markdown pilot (UC-01).

Design (pre-registered in docs/05-applied-ai/pilot-charter.md): 12 matched
pairs of stores, one pilot and one control per pair, 8 baseline weeks and
10 pilot weeks. The effect is a difference-in-differences per pair:

    (pilot store: pilot weeks - baseline weeks) - (control store: same)

which removes what both stores share (season, promotions, weather). The 90%
confidence interval comes from a bootstrap over pairs (the unit that was
randomised), not over store-weeks, which would overstate certainty.

Decision rules were fixed before the data came in; this module only
applies them.
"""

from __future__ import annotations

import random
from statistics import mean

from aitx import load

KPIS = ("waste_pct", "fresh_margin_pct", "oos_pct")


def pair_effects(kpi: str) -> list[float]:
    rows = load("pilot_measurements.json")
    cells: dict[tuple[int, str, str], list[float]] = {}
    for r in rows:
        cells.setdefault((r["pair"], r["arm"], r["phase"]), []).append(r[kpi])
    pairs = sorted({r["pair"] for r in rows})
    out = []
    for p in pairs:
        dp = mean(cells[(p, "pilot", "pilot")]) - mean(cells[(p, "pilot", "baseline")])
        dc = mean(cells[(p, "control", "pilot")]) - mean(cells[(p, "control", "baseline")])
        out.append(dp - dc)
    return out


def bootstrap_ci(values: list[float], level: float = 0.90, samples: int = 5000, seed: int = 11) -> tuple[float, float]:
    rng = random.Random(seed)
    n = len(values)
    means = sorted(mean(rng.choice(values) for _ in range(n)) for _ in range(samples))
    lo = means[int((1 - level) / 2 * samples)]
    hi = means[int((1 + level) / 2 * samples) - 1]
    return round(lo, 3), round(hi, 3)


def naive_before_after(kpi: str = "waste_pct") -> float:
    """What a pilot without a control group would have reported."""
    rows = [r for r in load("pilot_measurements.json") if r["arm"] == "pilot"]
    before = mean(r[kpi] for r in rows if r["phase"] == "baseline")
    after = mean(r[kpi] for r in rows if r["phase"] == "pilot")
    return round(after - before, 3)


def evaluate() -> dict:
    design = load("pilot_design.json")
    crit = design["criteria"]
    results = {}
    for kpi in KPIS:
        effects = pair_effects(kpi)
        lo, hi = bootstrap_ci(effects)
        results[kpi] = {"effect_pp": round(mean(effects), 3), "ci90": [lo, hi], "pairs_improved": None}
    results["waste_pct"]["pairs_improved"] = sum(e < 0 for e in pair_effects("waste_pct"))

    rows = [r for r in load("pilot_measurements.json") if "suggestions" in r]
    adoption = round(100 * sum(r["accepted"] for r in rows) / sum(r["suggestions"] for r in rows), 1)

    p = crit["primary"]
    w = results["waste_pct"]
    checks = {
        "primary_effect": -w["effect_pp"] >= p["min_effect_pp"],
        "primary_confidence": -w["ci90"][1] >= p["ci_lower_bound_pp"],
        "margin_guardrail": results["fresh_margin_pct"]["ci90"][0] >= -crit["guardrails"][0]["max_worse_pp"],
        "availability_guardrail": results["oos_pct"]["ci90"][1] <= crit["guardrails"][1]["max_worse_pp"],
        "adoption": adoption >= crit["adoption"]["min"],
    }
    baseline_waste = mean(r["waste_pct"] for r in load("pilot_measurements.json")
                          if r["arm"] == "pilot" and r["phase"] == "baseline")
    client, fin = load("client.json"), load("finance.json")
    fresh_sales = client["revenue_eur_m"] * 1e6 * client["fresh_sales_share"]
    implied = -w["effect_pp"] / 100 * fresh_sales * fin["markdown_net_capture"]
    return {
        "results": results,
        "implied_annual_value_eur": round(implied, -4),
        "adoption_pct": adoption,
        "checks": checks,
        "decision": "GO" if all(checks.values()) else "NO-GO",
        "baseline_waste_pct": round(baseline_waste, 2),
        "relative_waste_reduction": round(-w["effect_pp"] / baseline_waste, 3),
        "naive_before_after_pp": naive_before_after(),
        "pairs": design["pairs"],
        "weeks": {"baseline": design["baseline_weeks"], "pilot": design["pilot_weeks"]},
    }


def weekly_series() -> list[dict]:
    """Average waste per arm per week, for the chart on the site."""
    rows = load("pilot_measurements.json")
    out = []
    for w in sorted({r["week"] for r in rows}):
        item = {"week": w}
        for arm in ("pilot", "control"):
            item[arm] = round(mean(r["waste_pct"] for r in rows if r["week"] == w and r["arm"] == arm), 3)
        out.append(item)
    return out
