"""Sequence foundations and use cases over 18 months.

Foundations start in month 1, except master-data quality (month 4, after
governance has named the data owners). A use case starts when every
foundation it needs is ready and a slot on its track is free, highest
priority first. Two tracks with their own capacity:

  build      custom solutions, three product squads
  adopt      buy or configure: vendor tools rolled out by IT with the
             business, three adoption slots

Separating them matters: if commodity tools compete with the strategic
bets for the same squads, the quick wins crowd out the work that creates
an advantage. Parked use cases are not scheduled; anything that cannot
finish within 18 months moves to the next horizon.
"""

from __future__ import annotations

from aitx import load
from aitx.portfolio import scored

HORIZON = 18
CAPACITY = {"build": 3, "adopt": 3}
FOUNDATION_START = {"F3": 1, "F5": 1, "F2": 1, "F1": 1, "F4": 4}


def foundations() -> dict[str, dict]:
    out = {}
    for f in load("foundations.json"):
        start = FOUNDATION_START[f["id"]]
        out[f["id"]] = {**f, "start": start, "end": start + f["months"] - 1}
    return out


def track(u: dict) -> str:
    return "build" if u["sourcing"] == "build" else "adopt"


def plan() -> dict:
    fnd = foundations()
    free = {t: [0] * n for t, n in CAPACITY.items()}  # month each slot becomes free
    items, later = [], []
    for u in sorted((u for u in scored() if u["class"] != "park"), key=lambda u: u["rank"]):
        t = track(u)
        ready = max([fnd[n]["end"] + 1 for n in u["needs"]] + [1])
        slot = min(range(CAPACITY[t]), key=lambda i: max(free[t][i] + 1, ready))
        start = max(free[t][slot] + 1, ready)
        end = start + u["effort_months"] - 1
        if end > HORIZON:
            later.append({"id": u["id"], "name": u["name"], "class": u["class"], "track": t, "earliest_start": start})
            continue
        free[t][slot] = end
        items.append({"id": u["id"], "name": u["name"], "class": u["class"], "bu": u["bu"], "needs": u["needs"],
                      "track": t, "start": start, "end": end, "slot": slot + 1, "value_mid": u["value_mid"],
                      "gate": "AI Act and DPO assessment before build" if u["ai_act_input"] == "review" else None})
    return {"foundations": list(fnd.values()), "use_cases": sorted(items, key=lambda x: (x["start"], x["id"])),
            "next_horizon": later, "horizon": HORIZON, "capacity": CAPACITY}


def check(p: dict | None = None) -> list[str]:
    """Every scheduled use case starts after the foundations it needs, and no
    track runs more use cases at once than it has capacity for."""
    p = p or plan()
    fnd = {f["id"]: f for f in p["foundations"]}
    problems = []
    for u in p["use_cases"]:
        for n in u["needs"]:
            if u["start"] <= fnd[n]["end"]:
                problems.append(f"{u['id']} starts before {n} is ready")
    for t, cap in p["capacity"].items():
        for m in range(1, p["horizon"] + 1):
            running = sum(u["track"] == t and u["start"] <= m <= u["end"] for u in p["use_cases"])
            if running > cap:
                problems.append(f"month {m}: {running} {t} use cases for {cap} slots")
    return problems
