# Roadmap: 18 months

Foundations and use cases, sequenced by [`aitx/roadmap.py`](../../aitx/roadmap.py) with two rules: a use case starts only when the foundations it needs are ready, and each track has a fixed capacity (three product squads for **build**, three adoption slots for **buy and configure**). The check that both rules hold runs in CI.

## Why two tracks

In a first version, all use cases competed for the same squads. The quick wins (mostly commodity tools) filled the squads and pushed the markdown advisor, the highest-ranked use case, to month 11. Separating commodity adoption from building differentiating solutions keeps both moving: tools roll out through IT and the business, squads build what creates an advantage.

## Foundations
<!--t:foundations-->
| Id | Foundation | What | Months | One-off | Run/year |
|---|---|---|---|---|---|
| F1 | Retail data platform | Sales, stock and waste at item-store-day, within 24 h, with owners and quality rules | 1–6 | €420k | €160k |
| F2 | AI orchestration layer | Model gateway, approved model catalogue, tool registry, evaluation and monitoring, cost per initiative | 1–4 | €240k | €120k |
| F3 | AI governance and policy | AI council, policy, intake, inventory, risk tiers, EU AI Act register | 1–3 | €90k | €60k |
| F4 | Product master-data quality | Attribute completeness and ownership for 28,000 SKUs | 4–8 | €180k | €50k |
| F5 | AI literacy and champions | Article 4 literacy for all users, 60 champions, product-owner training | 1–3 | €110k | €70k |
<!--/t-->

Governance (F3) and literacy (F5) start in month 1: they cost little and unblock almost everything. Master-data quality (F4) starts in month 4, after governance has named the data owners.

## Use cases
<!--t:roadmap-->
| Months | Id | Use case | Class | Track | Needs | Gate |
|---|---|---|---|---|---|---|
| 4–7 | UC-04 | Supplier invoice processing at scale | fill-in | adopt | F3 |  |
| 4–6 | UC-12 | Refrigeration energy optimisation (all stores) | quick win | adopt | F3 |  |
| 5–7 | UC-03 | Customer-service assistant (one tool) | quick win | adopt | F2, F3 |  |
| 7–10 | UC-01 | Fresh markdown advisor | strategic bet | build | F1, F3, F5 |  |
| 7–14 | UC-05 | Personalised promotions in the app | strategic bet | build | F1, F2, F3 |  |
| 7–11 | UC-07 | DC labour planning | strategic bet | adopt | F1, F3 |  |
| 8–9 | UC-09 | Office productivity assistant | quick win | adopt | F2, F3, F5 |  |
| 9–17 | UC-02 | Store-level automated ordering | strategic bet | build | F1, F2, F3, F4 |  |
| 9–10 | UC-06 | Product content generation (web and labels) | quick win | adopt | F2, F3, F4 |  |
| 10–10 | UC-10 | Developer assistant for all IT | quick win | adopt | F3 |  |
| 11–16 | UC-11 | Promotion planning optimiser | strategic bet | build | F1, F2 |  |
| 11–12 | UC-14 | IT service-desk automation | quick win | adopt | F2, F3 |  |
| 11–13 | UC-17 | Product master-data enrichment | quick win | adopt | F3, F4 |  |
| 12–17 | UC-08 | Store staff scheduling | strategic bet | adopt | F1, F3, F5 | AI Act and DPO assessment before build |
| 13–15 | UC-13 | Fleet predictive maintenance (fix) | quick win | adopt | F3 |  |
| 14–15 | UC-15 | HR policy assistant (checked) | quick win | adopt | F2, F3 |  |
| 15–17 | UC-16 | Customer churn and win-back | quick win | build | F3 |  |
| 16–18 | UC-20 | Supplier contract analysis | quick win | adopt | F2, F3 |  |
| 16–17 | UC-26 | Review insights for category managers | quick win | adopt | F2, F3 |  |
<!--/t-->

- The first result is live in month <!--n:rm.first_live-->6<!--/n--> (refrigeration energy optimisation); the customer-service assistant and invoice automation follow a month later.
- The markdown advisor rolls out in <!--n:rm.uc01-->months 7–10<!--/n-->, as soon as the data platform delivers the automated feed the pilot did not have.
- <!--n:rm.scheduled-->19<!--/n--> use cases are scheduled in 18 months.

## Next horizon (does not fit in 18 months)
<!--t:next_horizon-->
| Id | Use case | Class | Earliest start (month) |
|---|---|---|---|
| UC-23 | Delivery-slot pricing | strategic bet | 15 |
| UC-18 | Store operations copilot | strategic bet | 17 |
| UC-21 | Shrinkage anomaly detection | fill-in | 17 |
| UC-25 | Supplier risk monitoring (fix) | fill-in | 18 |
<!--/t-->

## Quick wins versus foundations

| Months | What the organisation sees | What is being built underneath |
|---|---|---|
| 1–3 | Policy, fast-lane intake, shadow tools replaced, literacy module | Governance, gateway, data platform design |
| 4–9 | Energy savings, customer-service assistant, invoice automation, office and code assistants, markdowns in stores | Data platform live, master data improving |
| 10–18 | Promotion planning, delivery-slot pricing, DC labour planning, store ordering under way | Personalisation and ordering on the new data |

## Governance of the roadmap

- The AI council reviews the roadmap monthly; the ExCo twice a year.
- A use case that misses its KPI two reviews in a row is re-scoped or stopped (value management).
- New use cases enter through intake and are scored with the same model; the roadmap is re-run, not re-negotiated.
