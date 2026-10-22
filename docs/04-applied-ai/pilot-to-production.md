# From pilot to production

The pilot proved value. It did not prove that the solution can run in 240 stores without the squad watching it. The gap is mostly not the model.

## Gates

Status at the end of the pilot: <!--n:prod.done-->6 of 12<!--/n--> done, readiness <!--n:prod.readiness-->67%<!--/n-->. **<!--n:prod.verdict-->Not ready: 5 blocking gates open<!--/n-->.**

<!--t:gates-->
| Id | Area | Gate | Status | Blocking | Owner |
|---|---|---|---|---|---|
| G01 | Value | Outcome KPI, baseline and pre-registered decision rules | done | yes | Head of fresh |
| G02 | Data | Automated daily feed of sales, stock and waste per item-store (replaces the pilot extract) | partial | yes | Data platform lead (F1) |
| G03 | Model | Monitoring of suggestion quality and acceptance per store, with alert thresholds | open | yes | Product squad |
| G04 | Model | Retraining and versioning procedure, with rollback to the previous model | open | yes | Product squad |
| G05 | Operations | Store procedure: who confirms markdowns, when, and how labels are printed | done | yes | COO stores |
| G06 | Operations | Support model: first line in stores, second line in IT, third line with the squad | partial | yes | IT service manager |
| G07 | Security | Security review of the service and its integrations | done | yes | CISO |
| G08 | Compliance | AI register entry; AI Act triage (minimal); DPIA screening (staff ids only) | done | yes | AI governance office |
| G09 | People | Training for store fresh teams (30 minutes) and AI literacy module | partial | no | HR learning |
| G10 | People | Works council informed; store staff feedback loop in place | done | yes | HR director |
| G11 | Cost | Run cost per store per month known and inside the business case | done | no | Finance business partner |
| G12 | Ownership | Named product owner and budget for year 1 in the business unit's plan | partial | yes | Head of fresh |
<!--/t-->

## What is blocking, and why it is typical

| Gap | Why pilots have it | Plan |
|---|---|---|
| Automated data feed (G02) | The squad built a daily extract by hand; fine for 24 stores, impossible for 240 | F1 delivers the item-store-day feed in month 6; wave 1 starts after |
| Monitoring (G03) and retraining (G04) | In a pilot, the data scientist *is* the monitoring | Monitoring of acceptance and suggestion quality per store, alert thresholds, a retraining procedure with rollback, built in the squad's first production sprint |
| Support model (G06) | Store questions went straight to the squad on WhatsApp | First line in stores (champions), second line IT service desk, third line the squad; runbook |
| Ownership and budget (G12) | Pilots are funded from the programme; production needs a line in the business unit's plan | Head of fresh carries the run budget from year 1; the AI council confirms |

## Scale plan

| Wave | Stores | Starts when | Measured how |
|---|---|---|---|
| 1 | 60 | All blocking gates done (month 7) | Same matched-pair design, 30 pairs, 8 weeks |
| 2 | 90 | Wave 1 meets the same criteria | Staggered roll-out by region (stepped-wedge) |
| 3 | 90 | Wave 2 meets the criteria | Benefit tracking against the pre-programme trend |

Each wave can stop the roll-out. If wave 1 does not reproduce at least half of the pilot effect, the council decides whether to redesign or stop before more stores follow.

## What we hand over

- The service, its runbook and monitoring dashboards.
- The evaluation code and the pre-registered criteria for the next waves.
- A named product owner and the benefit-tracking report in the AI office's monthly review.
