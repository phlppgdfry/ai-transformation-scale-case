# Evidence

What in this case is executed, what is simulated, and what was not done.

## Executed (CI on every push)

| Claim | How it is checked |
|---|---|
| Every number and table in the docs comes from the analysis | `python scripts/build.py --check` |
| The data is reproducible from a seed | `python scripts/make_data.py --check` |
| Triage, scoring, roadmap, value, pilot and gate logic behave as documented | `python -m unittest discover -s tests -t .` |
| The roadmap respects dependencies and capacity | `aitx.roadmap.check()`, in the build and the tests |
| The pilot decision follows the pre-registered rules | `tests/test_aitx.py::PilotTest` |

## Simulated (on purpose, and labelled)

| What | How | Why it is still useful |
|---|---|---|
| Ardena Group, its people, competitors and numbers | Fictional | The method, the reasoning and the artefacts carry over; the figures do not |
| Survey answers | Drawn around hand-set "true" levels per unit and dimension | Shows how scoring, spread and gaps work, not what a real retailer would score |
| Pilot measurements | Synthetic store-week data with a planted effect, season and noise | Shows the evaluation design and why a comparison group matters; the effect size is invented |
| Workshop outputs (use cases, values, scores) | Written for the case | Realistic in shape, not validated with a real client |

## Not done

- No real client, workshops, survey or pilot.
- No platform built: the orchestration layer is a design and a buy-vs-build analysis.
- No legal review of the AI Act register; it is a first pass, labelled as such.

## Authorship

Designed and written with substantial help from an AI assistant. The author is responsible for the content and should be able to run every workshop, explain every rule and defend every number without it.
