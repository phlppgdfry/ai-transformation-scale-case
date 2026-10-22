"""Pilot-to-production gates for UC-01.

The 'pilot-to-production gap' is mostly not about the model: it is data
feeds that were manual in the pilot, monitoring nobody set up, a support
model nobody agreed, and a budget that ends with the pilot. Each gate has
an owner; blocking gates must be done before wave 1.
"""

from __future__ import annotations

from aitx import load

POINTS = {"done": 1.0, "partial": 0.5, "open": 0.0}


def status() -> dict:
    g = load("production_gates.json")["gates"]
    score = sum(POINTS[x["status"]] for x in g) / len(g)
    blockers = [x for x in g if x["blocking"] and x["status"] != "done"]
    by_area: dict[str, list[str]] = {}
    for x in g:
        by_area.setdefault(x["area"], []).append(x["status"])
    return {
        "gates": g,
        "readiness": round(score, 3),
        "done": sum(x["status"] == "done" for x in g),
        "total": len(g),
        "blockers": blockers,
        "verdict": "Ready for wave 1" if not blockers else f"Not ready: {len(blockers)} blocking gates open",
        "model_gates_open": sum(x["area"] == "Model" and x["status"] != "done" for x in g),
    }
