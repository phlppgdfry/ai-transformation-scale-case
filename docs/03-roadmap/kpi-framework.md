# KPI and evaluation framework

Every use case is measured on four levels. The first two tell the squad whether the solution works; the last two tell the business whether it was worth it.

| Level | Question | Example (markdown advisor) | Who looks at it |
|---|---|---|---|
| 1. Model / system quality | Is the output good? | Forecast error of sell-through; share of suggestions within margin rules | Squad, weekly |
| 2. Usage and adoption | Do people use it, and trust it appropriately? | Suggestions accepted; overrides and their reasons | Product owner, weekly |
| 3. Process outcome | Does the process improve? | Time spent on markdowns per store per day; markdowns done before noon | BU owner, monthly |
| 4. Business outcome | Does the P&L or the customer notice? | Fresh waste % of fresh sales; fresh gross margin; availability | ExCo, quarterly |

## Rules for KPIs

1. **One primary outcome KPI per use case**, with a baseline measured before go-live. No baseline, no go-live.
2. **Guardrail KPIs** for what must not get worse (margin, availability, customer complaints, staff workload).
3. **A people metric** next to every business KPI ([human-first principles](../01-readiness/human-first-principles.md)).
4. **Pre-register the success criteria** before the data comes in, including the minimum effect that matters.
5. **Use a comparison group** wherever the context changes (season, promotions): before/after alone misleads (see the pilot, where it would have under-reported the effect).
6. **Track benefits after go-live** for at least a year; the AI office reports them to the council.

## Outcome KPI per scheduled use case

| Use case | Primary outcome KPI | Guardrail |
|---|---|---|
| UC-01 Fresh markdown advisor | Fresh waste % of fresh sales | Fresh margin, availability |
| UC-03 Customer-service assistant | Handling time; first-contact resolution | Customer satisfaction, error rate in replies |
| UC-04 Supplier invoice processing | Cost per invoice; straight-through rate | Payment errors |
| UC-07 DC labour planning | Overtime hours | Order fill rate |
| UC-11 Promotion planning | Promotion ROI | Supplier funding |
| UC-12 Refrigeration energy | kWh per m² | Food safety temperature alarms |
| UC-23 Delivery-slot pricing | Delivery cost per order | Order conversion |
| UC-09 Office assistant | Weekly active use; time saved (survey) | Data incidents |
