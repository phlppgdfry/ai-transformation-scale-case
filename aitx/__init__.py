"""aitx: the analysis toolkit behind the Ardena Group AI transformation case.

Each module turns engagement data into a decision-ready result, so that
every number in the documents can be traced and recomputed:

readiness   maturity per business unit and dimension, gaps to target
inventory   triage of existing AI initiatives: scale, fix, merge, pause, stop
governance  EU AI Act triage per use case and the obligations that follow
portfolio   use-case scoring, classification, robustness to the weights
roadmap     dependency- and capacity-aware sequencing over 18 months
value       business case per use case and for the roadmap
pilot       difference-in-differences evaluation of the markdown pilot
production  pilot-to-production gates and blockers

Standard library only.
"""

import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


@lru_cache(maxsize=None)
def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))
