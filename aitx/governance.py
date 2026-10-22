"""EU AI Act triage per use case.

A first-pass classification for the AI register, not legal advice: every
'review' and 'high' outcome goes to legal and the DPO before any build.
Reflects the AI Act as amended by the Digital Omnibus on AI (2026): Annex
III obligations apply from 2 December 2027, transparency duties (Art. 50)
from 2 August 2026.

Inputs per use case (set in the discovery workshops):
  minimal  no specific AI Act duty beyond AI literacy (Art. 4)
  limited  people interact with AI or see AI-generated content: Art. 50
  review   could fall under Annex III depending on design (e.g. work
           allocation based on personal traits, biometric identification)
  high     falls under Annex III as described (e.g. recruitment, 4(a))
"""

from __future__ import annotations

from aitx import load

OUTCOME = {
    "minimal": ("Minimal", "Proceed", ["AI literacy for users (Art. 4)", "Entry in the AI register"]),
    "limited": ("Transparency", "Proceed with transparency",
                ["Tell people they interact with AI or see AI-generated content (Art. 50)",
                 "AI literacy (Art. 4)", "Entry in the AI register"]),
    "review": ("To be assessed", "Legal and DPO assessment before build",
               ["Assess against Annex III with legal and the DPO",
                "Design to stay out of scope where possible (e.g. no individual profiling)",
                "DPIA if personal data is processed", "Works council consultation where staff are affected"]),
    "high": ("High-risk (Annex III)", "Park unless the business case carries full compliance",
             ["Deployer duties (Art. 26): human oversight, logging, monitoring, informing workers",
              "Provider conformity evidence from the vendor", "DPIA",
              "Obligations apply from 2 December 2027 for Annex III systems"]),
}


def triage(use_case: dict) -> dict:
    tier, decision, duties = OUTCOME[use_case["ai_act_input"]]
    return {"id": use_case["id"], "name": use_case["name"], "tier": tier, "decision": decision, "duties": duties}


def register() -> list[dict]:
    return [triage(u) for u in load("use_cases.json")]


def summary() -> dict:
    reg = register()
    counts: dict[str, int] = {}
    for r in reg:
        counts[r["tier"]] = counts.get(r["tier"], 0) + 1
    return {"counts": counts, "attention": [r for r in reg if r["tier"] in ("To be assessed", "High-risk (Annex III)")]}
