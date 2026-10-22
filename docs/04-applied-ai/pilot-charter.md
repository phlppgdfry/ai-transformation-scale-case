# Pilot charter: fresh markdown advisor (UC-01)

*Written in week 2, approved by the head of fresh and the COO stores before the baseline started. Nothing in this charter was changed after the data came in.*

## Why this pilot

- The highest-priority use case, and robust to the scoring weights (top five in <!--n:pf.UC-01.top5-->93%<!--/n--> of re-weightings).
- Differentiating: it uses data only Ardena has, on what customers choose Ardena for.
- It turns an existing initiative that never measured anything (I-02, I-20) into evidence.
- Minimal risk under the AI Act; no personal data beyond staff ids on the handheld.

## Hypothesis

If fresh teams get a daily list of suggested markdowns, fresh waste falls by at least 0.5 percentage points of fresh sales, without hurting fresh margin or availability.

## Design

| Element | Choice | Why |
|---|---|---|
| Unit | Store | Markdowns are a store process |
| Comparison | 12 matched pairs (similar size, region, baseline waste); one pilot and one control store per pair | Removes season, promotions and weather, which a before/after cannot |
| Baseline | 8 weeks, both arms | Enough weeks to see each store's normal level |
| Pilot | 10 weeks | Covers ramp-up and a stable period |
| Analysis | Difference-in-differences per pair; 90% bootstrap interval over pairs | The pair is the unit that was assigned |

## Success criteria (pre-registered)

| KPI | Rule |
|---|---|
| **Primary:** fresh waste % of fresh sales | Reduction ≥ 0.5 pp, and the 90% interval excludes reductions smaller than 0.2 pp |
| Guardrail: fresh gross margin % | Not worse than −0.10 pp (lower bound of the interval) |
| Guardrail: out-of-stock % | Not worse than +0.30 pp (upper bound of the interval) |
| Adoption: suggestions accepted by staff | ≥ 60% |

**GO** if all four hold; otherwise **NO-GO** with a decision whether to redesign or stop.

## Scope and limits

- Fresh produce, dairy, meat and bakery; not flowers.
- The pilot uses a daily data extract built by the squad, not a production feed. That is a known gap for production (gate G02).
- Store staff confirm every markdown. No automatic price changes.
