"""Build: keep numbers, tables, docs and site in step with the analysis.

    python3 scripts/build.py           # regenerate
    python3 scripts/build.py --check   # CI: fail if anything is stale

Two kinds of markers in README.md, docs/**/*.md and site/**/*.html:

    <!--n:key-->value<!--/n-->          a single number or phrase
    <!--t:key-->...table...<!--/t-->    a whole markdown table

Both are rewritten from aitx on every build, so no document can quote a
number the analysis no longer produces.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from aitx import governance, inventory, load, pilot, portfolio, production, readiness, roadmap, value  # noqa: E402

N = re.compile(r"<!--n:([\w.\-]+)-->(.*?)<!--/n-->", re.S)
T = re.compile(r"<!--t:([\w.\-]+)-->(.*?)<!--/t-->", re.S)
BU = {k: v["label"] for k, v in load("client.json")["business_units"].items()}


def eur(x: float) -> str:
    if abs(x) >= 1_000_000:
        return f"€{x / 1e6:.1f}m"
    if abs(x) >= 1000:
        return f"€{x / 1e3:.0f}k"
    return f"€{x:.0f}"


def pct(x: float) -> str:
    return f"{x * 100:.0f}%"


def analysis() -> dict:
    return {
        "readiness": readiness.scores(),
        "inventory": inventory.summary(),
        "triage": inventory.triage(),
        "governance": governance.summary(),
        "register": governance.register(),
        "portfolio": portfolio.scored(),
        "robustness": portfolio.robustness(),
        "differentiation": portfolio.differentiation(),
        "roadmap": roadmap.plan(),
        "value": value.portfolio_case(),
        "pilot": pilot.evaluate(),
        "pilot_series": pilot.weekly_series(),
        "production": production.status(),
    }


def numbers(a: dict) -> dict[str, str]:
    n: dict[str, str] = {}
    r = a["readiness"]
    n.update({"rd.overall": f"{r['overall']:.1f}", "rd.level": r["overall_level"], "rd.target": f"{r['target_overall']:.1f}",
              "rd.respondents": str(r["respondents"])})
    for d, v in r["group"].items():
        n[f"rd.group.{d}"] = f"{v:.1f}"
        n[f"rd.gap.{d}"] = f"{r['gaps'][d]:.1f}"
    for bu, dims in r["by_bu"].items():
        n[f"rd.bu.{bu}"] = f"{sum(dims.values()) / len(dims):.1f}"
    n["rd.top_gap"] = r["dimensions"][r["priority_gaps"][0]]
    i = a["inventory"]
    n.update({"inv.total": str(i["total"]), "inv.measured": str(i["with_measured_value"]),
              "inv.production": str(i["in_production"]), "inv.shadow": str(i["shadow"]),
              "inv.freed": eur(i["freed_per_year"]), "inv.monthly": eur(i["monthly_cost_total"])})
    for k in ("scale", "fix", "merge", "pause", "stop"):
        n[f"inv.{k}"] = str(i["counts"].get(k, 0))
    for k, v in a["governance"]["counts"].items():
        n["gov." + k.split()[0].lower()] = str(v)
    pf = a["portfolio"]
    n["pf.count"] = str(len(pf))
    for c in ("quick win", "strategic bet", "fill-in", "park"):
        n["pf." + c.replace(" ", "_")] = str(sum(u["class"] == c for u in pf))
    n["pf.first"] = pf[0]["name"]
    for uid, rb in a["robustness"].items():
        n[f"pf.{uid}.top5"] = pct(rb["top5"])
        n[f"pf.{uid}.top1"] = pct(rb["top1"])
    for k, v in a["differentiation"].items():
        n[f"pf.diff.{k}"] = str(len(v))
    rm = a["roadmap"]
    n["rm.scheduled"] = str(len(rm["use_cases"]))
    n["rm.later"] = str(len(rm["next_horizon"]))
    n["rm.first_live"] = str(min(u["end"] for u in rm["use_cases"]))
    uc01 = next(u for u in rm["use_cases"] if u["id"] == "UC-01")
    n["rm.uc01"] = f"months {uc01['start']}–{uc01['end']}"
    v = a["value"]
    n.update({"val.portfolio_npv": eur(v["portfolio_npv"]), "val.use_case_npv": eur(v["use_case_npv"]),
              "val.foundations_one_off": eur(v["foundations_one_off"]), "val.foundations_run": eur(v["foundations_run"]),
              "val.commodity_npv": eur(v["commodity_only_npv"]),
              "val.uc01.npv": eur(v["per_use_case"]["UC-01"]["npv"]),
              "val.uc01.payback": f"{v['per_use_case']['UC-01']['payback_months']} months"})
    p = a["pilot"]
    w = p["results"]["waste_pct"]
    n.update({"pilot.effect": f"{-w['effect_pp']:.2f} pp", "pilot.ci_lo": f"{-w['ci90'][1]:.2f}", "pilot.ci_hi": f"{-w['ci90'][0]:.2f}",
              "pilot.relative": pct(p["relative_waste_reduction"]), "pilot.adoption": f"{p['adoption_pct']:.0f}%",
              "pilot.decision": p["decision"], "pilot.pairs_improved": f"{w['pairs_improved']} of {p['pairs']}",
              "pilot.naive": f"{-p['naive_before_after_pp']:.2f} pp", "pilot.baseline": f"{p['baseline_waste_pct']:.1f}%",
              "pilot.margin": f"{p['results']['fresh_margin_pct']['effect_pp']:+.2f} pp",
              "pilot.oos": f"{p['results']['oos_pct']['effect_pp']:+.2f} pp",
              "pilot.value": eur(p["implied_annual_value_eur"])})
    pr = a["production"]
    n.update({"prod.readiness": pct(pr["readiness"]), "prod.done": f"{pr['done']} of {pr['total']}",
              "prod.blockers": str(len(pr["blockers"])), "prod.verdict": pr["verdict"]})
    return n


def md_table(header: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n" + "\n".join(out) + "\n"


def tables(a: dict) -> dict[str, str]:
    r = a["readiness"]
    t = {}
    t["readiness"] = md_table(
        ["Dimension", *BU.values(), "Group", "Target", "Gap"],
        [[r["dimensions"][d], *[f"{r['by_bu'][bu][d]:.1f}" for bu in BU], f"**{r['group'][d]:.1f}**",
          f"{r['target'][d]:.1f}", f"{r['gaps'][d]:.1f}"] for d in r["dimensions"]])
    t["weakest"] = md_table(["Dimension", "Lowest-scoring statement", "Score"],
                            [[r["dimensions"][d], x["statement"], f"{x['score']:.1f}"] for d, x in r["weakest_statement"].items()])
    t["triage"] = md_table(["Id", "Initiative", "Unit", "Kind", "Evidence", "€/month", "Decision", "Reason"],
                           [[x["id"], x["name"], BU[x["bu"]], x["kind"], x["evidence"], f"{x['monthly_cost_eur']:,}".replace(",", "."),
                             f"**{x['decision']}**", x["reason"]] for x in a["triage"]])
    rb = a["robustness"]
    t["portfolio"] = md_table(["Rank", "Id", "Use case", "Unit", "Value", "Fit", "Feasibility", "Priority", "Class", "Top-5 share"],
                              [[u["rank"], u["id"], u["name"], BU[u["bu"]], f"{u['value_score']:.1f}", u["fit"],
                                f"{u['feasibility']:.1f}", f"{u['priority']:.2f}", u["class"], pct(rb[u['id']]['top5'])]
                               for u in a["portfolio"]])
    t["differentiation"] = md_table(["Category", "What it means", "Sourcing default", "Use cases"], [
        ["Differentiating", "Uses Ardena's own data and processes in a way competitors cannot copy quickly", "Build (own squads, own models)",
         ", ".join(a["differentiation"]["differentiating"])],
        ["Parity", "Competitors have it or will; customers notice if Ardena lacks it", "Configure a platform, own the data and the process",
         ", ".join(a["differentiation"]["parity"])],
        ["Commodity", "Everyone gets it from the same vendors", "Buy, standardise, negotiate", ", ".join(a["differentiation"]["commodity"])],
    ])
    rm = a["roadmap"]
    t["foundations"] = md_table(["Id", "Foundation", "What", "Months", "One-off", "Run/year"],
                                [[f["id"], f["name"], f["detail"], f"{f['start']}–{f['end']}", eur(f["one_off_eur"]), eur(f["run_eur"])]
                                 for f in rm["foundations"]])
    t["roadmap"] = md_table(["Months", "Id", "Use case", "Class", "Track", "Needs", "Gate"],
                            [[f"{u['start']}–{u['end']}", u["id"], u["name"], u["class"], u["track"], ", ".join(u["needs"]),
                              u["gate"] or ""] for u in rm["use_cases"]])
    t["next_horizon"] = md_table(["Id", "Use case", "Class", "Earliest start (month)"],
                                 [[x["id"], x["name"], x["class"], x["earliest_start"]] for x in rm["next_horizon"]])
    v = a["value"]["per_use_case"]
    t["value"] = md_table(["Id", "Use case", "One-off", "Run/year", "Benefit/year (after haircut)", "NPV 3 yrs", "Payback"],
                          [[u["id"], u["name"], eur(v[u["id"]]["one_off"]), eur(v[u["id"]]["run_per_year"]),
                            eur(v[u["id"]]["benefit_full_year"]), eur(v[u["id"]]["npv"]),
                            f"{v[u['id']]['payback_months']} m" if v[u["id"]]["payback_months"] is not None else "—"]
                           for u in sorted(a["portfolio"], key=lambda x: -v[x["id"]]["npv"]) if u["id"] in a["value"]["scheduled"]])
    p = a["pilot"]
    t["pilot"] = md_table(["KPI", "Effect (pilot − control, pp)", "90% CI", "Rule", "Result"], [
        ["Fresh waste % of fresh sales (primary)", f"{p['results']['waste_pct']['effect_pp']:+.2f}",
         f"[{p['results']['waste_pct']['ci90'][0]:+.2f}, {p['results']['waste_pct']['ci90'][1]:+.2f}]",
         "reduction ≥ 0.5 pp and CI excludes < 0.2 pp", "pass" if p["checks"]["primary_effect"] and p["checks"]["primary_confidence"] else "fail"],
        ["Fresh gross margin % (guardrail)", f"{p['results']['fresh_margin_pct']['effect_pp']:+.2f}",
         f"[{p['results']['fresh_margin_pct']['ci90'][0]:+.2f}, {p['results']['fresh_margin_pct']['ci90'][1]:+.2f}]",
         "not worse than −0.10 pp", "pass" if p["checks"]["margin_guardrail"] else "fail"],
        ["Out-of-stock % (guardrail)", f"{p['results']['oos_pct']['effect_pp']:+.2f}",
         f"[{p['results']['oos_pct']['ci90'][0]:+.2f}, {p['results']['oos_pct']['ci90'][1]:+.2f}]",
         "not worse than +0.30 pp", "pass" if p["checks"]["availability_guardrail"] else "fail"],
        ["Suggestions accepted by staff", f"{p['adoption_pct']:.1f}%", "—", "≥ 60%", "pass" if p["checks"]["adoption"] else "fail"],
    ])
    t["gates"] = md_table(["Id", "Area", "Gate", "Status", "Blocking", "Owner"],
                          [[g["id"], g["area"], g["gate"], g["status"], "yes" if g["blocking"] else "no", g["owner"]]
                           for g in a["production"]["gates"]])
    t["register"] = md_table(["Id", "Use case", "Tier", "Decision"],
                             [[x["id"], x["name"], x["tier"], x["decision"]] for x in a["register"]])
    return t


def site_data(a: dict) -> dict[Path, str]:
    d = ROOT / "site" / "data"
    pf = [{k: u[k] for k in ("id", "name", "bu", "value_score", "feasibility", "priority", "class", "value_mid", "differentiation",
                             "sourcing", "effort_months", "owner", "kpi", "rank")} | {"top5": a["robustness"][u["id"]]["top5"]}
          for u in a["portfolio"]]
    return {
        d / "portfolio.json": json.dumps({"units": BU, "use_cases": pf}),
        # Rounded here, with Python's rounding, so the heatmap shows exactly the
        # numbers in the docs (JavaScript's toFixed rounds some halves differently).
        d / "readiness.json": json.dumps({
            "dimensions": a["readiness"]["dimensions"], "units": BU, "overall": a["readiness"]["overall"],
            "by_bu": {bu: {k: float(f"{v:.1f}") for k, v in dims.items()} for bu, dims in a["readiness"]["by_bu"].items()},
            "group": {k: float(f"{v:.1f}") for k, v in a["readiness"]["group"].items()},
            "target": a["readiness"]["target"]}),
        d / "roadmap.json": json.dumps(a["roadmap"]),
        d / "pilot.json": json.dumps({"evaluation": a["pilot"], "series": a["pilot_series"]}),
        d / "triage.json": json.dumps({"summary": a["inventory"], "rows": a["triage"], "units": BU}),
    }


def targets() -> list[Path]:
    return [p for p in [ROOT / "README.md", ROOT / "EVIDENCE.md", *sorted((ROOT / "docs").rglob("*.md")),
                        *sorted((ROOT / "site").rglob("*.html"))] if p.exists()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    a = analysis()
    problems = [f"roadmap: {p}" for p in roadmap.check(a["roadmap"])]
    nums, tabs = numbers(a), tables(a)
    outputs = {p: text + "\n" for p, text in site_data(a).items()}
    for path in targets():
        text = path.read_text(encoding="utf-8")

        def rn(m: re.Match) -> str:
            if m.group(1) not in nums:
                problems.append(f"{path.relative_to(ROOT)}: unknown number key {m.group(1)}")
                return m.group(0)
            return f"<!--n:{m.group(1)}-->{nums[m.group(1)]}<!--/n-->"

        def rt(m: re.Match) -> str:
            if m.group(1) not in tabs:
                problems.append(f"{path.relative_to(ROOT)}: unknown table key {m.group(1)}")
                return m.group(0)
            return f"<!--t:{m.group(1)}-->{tabs[m.group(1)]}<!--/t-->"

        new = T.sub(rt, N.sub(rn, text))
        if new != text:
            outputs[path] = new
    for path, text in outputs.items():
        if path.exists() and path.read_text(encoding="utf-8") == text:
            continue
        if args.check:
            problems.append(f"stale: {path.relative_to(ROOT)} (run python3 scripts/build.py)")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)}")
    for p in problems:
        print("BUILD:", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
