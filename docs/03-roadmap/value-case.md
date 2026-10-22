# Value case

Per use case and for the roadmap, computed by [`aitx/value.py`](../../aitx/value.py) from [`data/finance.json`](../../data/finance.json). Illustrative: every input is in the assumption register.

## Key assumptions

| Assumption | Value | Why |
|---|---|---|
| Realisation haircut on workshop estimates | 30% | Workshop estimates are optimistic; most portfolios deliver less |
| Benefit ramp after go-live | 25%, 75%, 100% over three years | Adoption takes time, especially in stores |
| Build cost | €55k per squad-month | Blended internal and partner rate |
| Adoption cost (buy/configure) | €18k per month | IT, business and change effort |
| Run cost | 15% of build per year, plus licences at 10% of benefit for bought tools | |
| Discount rate | 8% | Ardena's hurdle rate |

## Portfolio

| | Value |
|---|---|
| NPV of the 19 scheduled use cases (three years from each go-live) | <!--n:val.use_case_npv-->€14.7m<!--/n--> |
| Foundations: one-off | <!--n:val.foundations_one_off-->€1.0m<!--/n--> |
| Foundations: run per year | <!--n:val.foundations_run-->€460k<!--/n--> |
| **Portfolio NPV including foundations** | **<!--n:val.portfolio_npv-->€12.5m<!--/n-->** |

The foundations are funded centrally and charged to no single use case. Charged to the markdown advisor alone, they would make it look marginal; spread over the portfolio, they are what makes the portfolio possible. That is the argument for the ExCo to fund them as a platform, not as project costs.

## Per use case
<!--t:value-->
| Id | Use case | One-off | Run/year | Benefit/year (after haircut) | NPV 3 yrs | Payback |
|---|---|---|---|---|---|---|
| UC-02 | Store-level automated ordering | €495k | €74k | €2.5m | €3.4m | 11 m |
| UC-05 | Personalised promotions in the app | €440k | €66k | €1.8m | €2.3m | 13 m |
| UC-01 | Fresh markdown advisor | €220k | €33k | €1.4m | €2.0m | 8 m |
| UC-11 | Promotion planning optimiser | €330k | €50k | €1.1m | €1.4m | 14 m |
| UC-08 | Store staff scheduling | €108k | €100k | €840k | €1.0m | 12 m |
| UC-07 | DC labour planning | €90k | €76k | €630k | €771k | 12 m |
| UC-16 | Customer churn and win-back | €165k | €25k | €490k | €601k | 14 m |
| UC-12 | Refrigeration energy optimisation (all stores) | €54k | €51k | €427k | €531k | 12 m |
| UC-03 | Customer-service assistant (one tool) | €54k | €46k | €374k | €457k | 12 m |
| UC-09 | Office productivity assistant | €36k | €35k | €298k | €372k | 11 m |
| UC-04 | Supplier invoice processing at scale | €72k | €42k | €315k | €350k | 14 m |
| UC-06 | Product content generation (web and labels) | €36k | €32k | €262k | €323k | 12 m |
| UC-17 | Product master-data enrichment | €54k | €32k | €238k | €265k | 14 m |
| UC-10 | Developer assistant for all IT | €18k | €21k | €182k | €233k | 9 m |
| UC-13 | Fleet predictive maintenance (fix) | €54k | €25k | €168k | €166k | 16 m |
| UC-14 | IT service-desk automation | €36k | €19k | €136k | €145k | 15 m |
| UC-20 | Supplier contract analysis | €54k | €19k | €112k | €87k | 20 m |
| UC-15 | HR policy assistant (checked) | €36k | €14k | €88k | €76k | 19 m |
| UC-26 | Review insights for category managers | €36k | €13k | €80k | €66k | 19 m |
<!--/t-->

## Check against the pilot

The workshop estimate for the markdown advisor was €1.4–2.6m a year. The pilot's measured effect, scaled to all stores with a 20% net capture of avoided waste (markdowns are sold at a discount, some sales would have happened anyway), implies <!--n:pilot.value-->€2.2m<!--/n--> a year. The estimate holds; the business case uses the workshop mid-point minus the 30% haircut, which is now conservative.
