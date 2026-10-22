"""AI readiness: maturity per business unit and dimension.

Scale (1-5): 1 Ad hoc, 2 Experimenting, 3 Defined, 4 Scaled, 5 Embedded.
A respondent's dimension score is the mean of the four statements; a
business unit's score is the mean of its respondents; the group score gives
each business unit equal weight, so the 8,200 store staff do not drown out
the 450 people in e-commerce. Disagreement (standard deviation within a
business unit) is reported, because a wide spread is itself a finding.
"""

from __future__ import annotations

from statistics import mean, pstdev

from aitx import load

LEVELS = {1: "Ad hoc", 2: "Experimenting", 3: "Defined", 4: "Scaled", 5: "Embedded"}


def level_name(score: float) -> str:
    return LEVELS[max(1, min(5, int(score + 1e-9)))]


def scores() -> dict:
    a = load("assessment.json")
    dims = [d["id"] for d in a["dimensions"]]
    by_bu: dict[str, dict[str, list[float]]] = {}
    for r in a["responses"]:
        for d in dims:
            vals = [v for k, v in r["answers"].items() if k.startswith(d + ".")]
            by_bu.setdefault(r["bu"], {}).setdefault(d, []).append(mean(vals))
    bu_scores = {bu: {d: round(mean(v), 2) for d, v in ds.items()} for bu, ds in by_bu.items()}
    spread = {bu: {d: round(pstdev(v), 2) for d, v in ds.items()} for bu, ds in by_bu.items()}
    group = {d: round(mean(bu_scores[bu][d] for bu in bu_scores), 2) for d in dims}
    gaps = {d: round(a["target"][d] - group[d], 2) for d in dims}
    weakest = {}
    for d in dims:
        stmt_means = []
        for i in range(len(next(x for x in a["dimensions"] if x["id"] == d)["statements"])):
            key = f"{d}.{i + 1}"
            per_bu = {}
            for r in a["responses"]:
                per_bu.setdefault(r["bu"], []).append(r["answers"][key])
            stmt_means.append((round(mean(mean(v) for v in per_bu.values()), 2), i))
        low, idx = min(stmt_means)
        weakest[d] = {"statement": next(x for x in a["dimensions"] if x["id"] == d)["statements"][idx], "score": low}
    overall = round(mean(group.values()), 2)
    return {
        "dimensions": {x["id"]: x["name"] for x in a["dimensions"]},
        "by_bu": bu_scores,
        "spread": spread,
        "group": group,
        "overall": overall,
        "overall_level": level_name(overall),
        "target": a["target"],
        "target_overall": round(mean(a["target"].values()), 2),
        "gaps": gaps,
        "priority_gaps": sorted(gaps, key=lambda d: -gaps[d])[:3],
        "weakest_statement": weakest,
        "respondents": len(a["responses"]),
    }
