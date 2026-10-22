"""Use-case portfolio: score, classify, test the ranking.

value score   1-5, from the mid-point of the annual value range on a log
              scale (a €2m use case is not 20x more attractive than a
              €100k one once risk and effort are counted)
fit           strategic fit 1-5 from the executive workshop
feasibility   weighted mean of data, technology and organisational readiness
priority      weighted sum, minus a penalty for an open AI Act review

Classes (growth map quadrants):
  quick win      feasibility >= 3.5 and effort <= 3 months
  strategic bet  value >= 3.5 or fit >= 4, but harder or longer
  fill-in        the rest that is feasible (>= 3)
  park           high-risk under the AI Act, or low value and low feasibility
"""

from __future__ import annotations

import math
import random

from aitx import load


def _weights() -> dict:
    return load("weights.json")


def value_score(u: dict, mids: list[float]) -> float:
    lo, hi = math.log(min(mids)), math.log(max(mids))
    mid = (u["value_low"] + u["value_high"]) / 2
    return round(1 + 4 * (math.log(mid) - lo) / (hi - lo), 2)


def feasibility(u: dict, parts: dict | None = None) -> float:
    p = parts or _weights()["feasibility_parts"]
    return round(sum(u[k] * w for k, w in p.items()) / sum(p.values()), 2)


def priority(u: dict, v: float, f: float, w: dict) -> float:
    penalty = w["review_penalty"] if u["ai_act_input"] == "review" else 0.0
    return round(w["value"] * v + w["fit"] * u["fit"] + w["feasibility"] * f - penalty, 3)


def classify(u: dict, v: float, f: float) -> str:
    if u["ai_act_input"] == "high" or (v < 2.5 and f < 3):
        return "park"
    if f >= 3.5 and u["effort_months"] <= 3:
        return "quick win"
    if v >= 3.5 or u["fit"] >= 4:
        return "strategic bet"
    if f >= 3:
        return "fill-in"
    return "park"


def scored() -> list[dict]:
    w = _weights()
    ucs = load("use_cases.json")
    mids = [(u["value_low"] + u["value_high"]) / 2 for u in ucs]
    out = []
    for u in ucs:
        v, f = value_score(u, mids), feasibility(u)
        out.append({**u, "value_mid": (u["value_low"] + u["value_high"]) / 2, "value_score": v,
                    "feasibility": f, "priority": priority(u, v, f, w), "class": classify(u, v, f)})
    ranked = sorted(out, key=lambda x: (-x["priority"], x["id"]))
    for i, x in enumerate(ranked, start=1):
        x["rank"] = i
    return ranked


def robustness(samples: int = 2000, seed: int = 7) -> dict[str, dict]:
    """Re-draw all weights at random (uniform on the simplex) and record how
    often each use case lands in the top 5. A use case that is top-5 under
    almost any weighting is a robust choice; one that needs a specific
    weighting is a judgement call to make explicit."""
    rng = random.Random(seed)
    ucs = load("use_cases.json")
    mids = [(u["value_low"] + u["value_high"]) / 2 for u in ucs]
    base = _weights()
    top5 = {u["id"]: 0 for u in ucs}
    top1 = {u["id"]: 0 for u in ucs}
    for _ in range(samples):
        g = [rng.gammavariate(1, 1) for _ in range(6)]
        s = sum(g)
        w = {"value": g[0] / s, "fit": g[1] / s, "feasibility": g[2] / s, "review_penalty": base["review_penalty"]}
        parts = {"data": g[3], "tech": g[4], "org": g[5]}
        prios = []
        for u in ucs:
            if u["ai_act_input"] == "high":
                continue
            v, f = value_score(u, mids), feasibility(u, parts)
            prios.append((priority(u, v, f, w), u["id"]))
        prios.sort(reverse=True)
        for _, uid in prios[:5]:
            top5[uid] += 1
        top1[prios[0][1]] += 1
    return {uid: {"top5": round(top5[uid] / samples, 3), "top1": round(top1[uid] / samples, 3)} for uid in top5}


def differentiation() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {"differentiating": [], "parity": [], "commodity": []}
    for u in scored():
        if u["class"] != "park":
            out[u["differentiation"]].append(u["id"])
    return out
