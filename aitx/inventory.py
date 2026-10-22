"""Triage of the AI initiatives found in discovery.

Rules, applied in order (first match wins), agreed with the CIO and CFO:

1. pause  linked to a use case whose AI Act triage says 'review' or 'high'
2. stop   unsanctioned (shadow) tool: move its users to a sanctioned one
3. merge  duplicates another initiative: fold into it
4. stop   no owner and no evidence of value
5. scale  owned, with measured value and data access (live or not)
6. fix    otherwise: name what is missing (owner, measurement, data access)

The point is not the label but the reason: every initiative leaves the
triage with one sentence that its sponsor can act on.
"""

from __future__ import annotations

from aitx import load


def _risk_links() -> dict[str, str]:
    out = {}
    for u in load("use_cases.json"):
        if u["ai_act_input"] in ("review", "high"):
            for i in u["from_initiatives"]:
                out[i] = u["id"]
    return out


def triage_one(i: dict, risky: dict[str, str]) -> tuple[str, str]:
    if i["id"] in risky:
        return "pause", f"Linked to {risky[i['id']]}: EU AI Act and DPO assessment first"
    if i["kind"] == "shadow-tool":
        data = "personal or confidential data" if i["personal_data"] else "company data"
        return "stop", f"Unsanctioned tool with {data}: move its users to the sanctioned alternative"
    if i["duplicate_of"]:
        return "merge", f"Same problem as {i['duplicate_of']}: one owner, one tool"
    if not i["owner"] and i["evidence"] == "none":
        return "stop", "No owner and no evidence of value"
    if i["owner"] and i["evidence"] == "measured" and i["data_access"] == "ok":
        return "scale", "Owner, measured value and data access are in place"
    missing = []
    if not i["owner"]:
        missing.append("a business owner")
    if i["evidence"] != "measured":
        missing.append("a baseline and outcome KPI")
    if i["data_access"] != "ok":
        missing.append("reliable data access")
    return "fix", "Missing " + ", ".join(missing)


def triage() -> list[dict]:
    risky = _risk_links()
    out = []
    for i in load("initiatives.json"):
        decision, reason = triage_one(i, risky)
        out.append({**i, "decision": decision, "reason": reason})
    return out


def summary() -> dict:
    rows = triage()
    counts: dict[str, int] = {}
    cost: dict[str, int] = {}
    for r in rows:
        counts[r["decision"]] = counts.get(r["decision"], 0) + 1
        cost[r["decision"]] = cost.get(r["decision"], 0) + r["monthly_cost_eur"]
    return {
        "total": len(rows),
        "counts": counts,
        "monthly_cost": cost,
        "monthly_cost_total": sum(r["monthly_cost_eur"] for r in rows),
        "freed_per_year": 12 * (cost.get("stop", 0) + cost.get("merge", 0)),
        "with_measured_value": sum(r["evidence"] == "measured" for r in rows),
        "in_production": sum(r["kind"] == "production" for r in rows),
        "shadow": sum(r["kind"] == "shadow-tool" for r in rows),
        "personal_data_in_shadow": sum(r["kind"] == "shadow-tool" and r["personal_data"] for r in rows),
    }
