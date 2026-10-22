"""Business case per use case and for the 18-month roadmap.

Benefits use the mid-point of the value range from the workshops, minus a
realisation haircut (most portfolios deliver less than the workshop
estimate; 30% is a planning assumption, see data/finance.json), ramped up
over three years from go-live. Costs: build squads or adoption effort per
month, plus run cost (a share of build) and licences for bought tools.
Foundations are costed once, for the whole portfolio, because they serve
many use cases; that is the argument for funding them centrally.
"""

from __future__ import annotations

from aitx import load
from aitx.portfolio import scored
from aitx.roadmap import plan


def _f() -> dict:
    return load("finance.json")


def npv(cashflows: list[float], rate: float) -> float:
    return sum(cf / (1 + rate) ** (t + 1) for t, cf in enumerate(cashflows))


def use_case_case(u: dict) -> dict:
    f = _f()
    benefit = u["value_mid"] * (1 - f["realisation_haircut"])
    build = u["effort_months"] * (f["squad_month_eur"] if u["sourcing"] == "build" else f["adopt_month_eur"])
    licence = benefit * f["licence_share_of_value_for_buy"] if u["sourcing"] != "build" else 0.0
    run = build * f["run_share_of_build"] + licence
    operating = [benefit * r - run for r in f["ramp"]]
    flows = operating[:]
    flows[0] -= build
    # Payback: months until the cumulative cash, starting at minus the
    # one-off cost, turns positive (operating cash spread evenly over a year).
    payback, cum = None, -build
    for year, op in enumerate(operating, start=1):
        if payback is None and op > 0 and cum + op >= 0:
            payback = round((year - 1) * 12 + 12 * (-cum / op))
        cum += op
    return {"id": u["id"], "one_off": round(build), "run_per_year": round(run), "benefit_full_year": round(benefit),
            "npv": round(npv(flows, f["discount_rate"])), "payback_months": payback}


def portfolio_case() -> dict:
    f = _f()
    rate = f["discount_rate"]
    roadmap = plan()
    scheduled = {u["id"] for u in roadmap["use_cases"]}
    cases = {u["id"]: use_case_case(u) for u in scored()}
    foundations = load("foundations.json")
    fnd_one_off = sum(x["one_off_eur"] for x in foundations)
    fnd_run = sum(x["run_eur"] for x in foundations)
    uc_npv = sum(cases[i]["npv"] for i in scheduled)
    fnd_npv = -fnd_one_off / (1 + rate) - sum(fnd_run / (1 + rate) ** t for t in (1, 2, 3))
    return {
        "per_use_case": cases,
        "scheduled": sorted(scheduled),
        "use_case_npv": round(uc_npv),
        "foundations_one_off": fnd_one_off,
        "foundations_run": fnd_run,
        "foundations_npv": round(fnd_npv),
        "portfolio_npv": round(uc_npv + fnd_npv),
        "commodity_only_npv": round(sum(cases[i]["npv"] for i in scheduled
                                        if next(u for u in scored() if u["id"] == i)["differentiation"] == "commodity")),
    }
