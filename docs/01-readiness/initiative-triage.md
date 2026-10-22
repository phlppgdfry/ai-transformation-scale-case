# Triage of existing AI initiatives

Discovery found <!--n:inv.total-->37<!--/n--> AI initiatives: pilots, vendor features switched on by default, production systems and shadow tools. Together they cost <!--n:inv.monthly-->€45k<!--/n--> a month. Only <!--n:inv.production-->3<!--/n--> are in production and <!--n:inv.measured-->11<!--/n--> have a measured result; <!--n:inv.shadow-->5<!--/n--> are shadow tools.

## The rules

Agreed with the CIO and CFO **before** anyone saw the outcome for their own initiative. First match wins.

1. **Pause**: linked to a use case whose EU AI Act triage says "to be assessed" or "high-risk". Assessment first.
2. **Stop**: unsanctioned (shadow) tool. Its users move to the sanctioned alternative.
3. **Merge**: solves the same problem as another initiative. One owner, one tool.
4. **Stop**: no owner and no evidence of value.
5. **Scale**: owned, with measured value and data access.
6. **Fix**: everything else, with what is missing named.

The rules are code ([`aitx/inventory.py`](../../aitx/inventory.py)), so they apply the same way to every initiative and to new ones.

## Result

| Decision | Count |
|---|---|
| Scale | <!--n:inv.scale-->8<!--/n--> |
| Fix | <!--n:inv.fix-->14<!--/n--> |
| Merge | <!--n:inv.merge-->4<!--/n--> |
| Pause | <!--n:inv.pause-->3<!--/n--> |
| Stop | <!--n:inv.stop-->8<!--/n--> |

Stopping and merging frees about <!--n:inv.freed-->€54k<!--/n--> a year in direct costs. That is small; the real gain is attention. Twelve fewer things to steer means the squads and the council can focus on the portfolio.

## All initiatives
<!--t:triage-->
| Id | Initiative | Unit | Kind | Evidence | €/month | Decision | Reason |
|---|---|---|---|---|---|---|---|
| I-01 | Vendor demand-forecasting module | Supply chain | production | measured | 9.500 | **scale** | Owner, measured value and data access are in place |
| I-02 | Store fresh-waste dashboard with ML alerts | Stores | pilot | anecdotal | 1.800 | **fix** | Missing a baseline and outcome KPI, reliable data access |
| I-03 | ChatGPT accounts paid on credit cards (marketing) | Head office | shadow-tool | none | 640 | **stop** | Unsanctioned tool with personal or confidential data: move its users to the sanctioned alternative |
| I-04 | Copilot licences for 120 office users | Head office | vendor-feature | anecdotal | 3.600 | **fix** | Missing a baseline and outcome KPI |
| I-05 | Customer-service email triage (vendor add-on) | Head office | pilot | measured | 2.100 | **scale** | Owner, measured value and data access are in place |
| I-06 | Second email-triage tool (e-com team) | E-commerce | pilot | none | 900 | **merge** | Same problem as I-05: one owner, one tool |
| I-07 | Route optimisation for home delivery | E-commerce | production | measured | 4.200 | **scale** | Owner, measured value and data access are in place |
| I-08 | Shelf-image recognition PoC | Stores | pilot | none | 0 | **stop** | No owner and no evidence of value |
| I-09 | HR CV-screening plug-in in the ATS | Head office | vendor-feature | none | 750 | **pause** | Linked to UC-22: EU AI Act and DPO assessment first |
| I-10 | Supplier invoice extraction | Head office | pilot | measured | 1.300 | **fix** | Missing reliable data access |
| I-11 | Promotion-uplift model (data science team) | Head office | pilot | anecdotal | 0 | **fix** | Missing a baseline and outcome KPI, reliable data access |
| I-12 | Generative product descriptions for webshop | E-commerce | pilot | measured | 600 | **scale** | Owner, measured value and data access are in place |
| I-13 | Store staff scheduling optimiser | Stores | pilot | anecdotal | 2.800 | **pause** | Linked to UC-08: EU AI Act and DPO assessment first |
| I-14 | DC pick-path optimisation | Supply chain | pilot | measured | 1.500 | **scale** | Owner, measured value and data access are in place |
| I-15 | Chatbot on website (FAQ) | E-commerce | production | anecdotal | 1.100 | **fix** | Missing a baseline and outcome KPI |
| I-16 | Personal ChatGPT use in IT (code) | Head office | shadow-tool | none | 0 | **stop** | Unsanctioned tool with company data: move its users to the sanctioned alternative |
| I-17 | Energy optimisation for store refrigeration | Stores | vendor-feature | measured | 2.400 | **scale** | Owner, measured value and data access are in place |
| I-18 | Loss-prevention video analytics PoC | Stores | pilot | none | 0 | **pause** | Linked to UC-19: EU AI Act and DPO assessment first |
| I-19 | Second invoice-extraction trial (accounts payable) | Head office | pilot | none | 400 | **merge** | Same problem as I-10: one owner, one tool |
| I-20 | Markdown price suggestions (spreadsheet + model) | Stores | pilot | anecdotal | 0 | **merge** | Same problem as I-02: one owner, one tool |
| I-21 | Contract review assistant (legal) | Head office | shadow-tool | none | 180 | **stop** | Unsanctioned tool with personal or confidential data: move its users to the sanctioned alternative |
| I-22 | Transport ETA prediction | Supply chain | pilot | anecdotal | 900 | **fix** | Missing a baseline and outcome KPI |
| I-23 | Product master-data enrichment | Head office | pilot | measured | 700 | **fix** | Missing reliable data access |
| I-24 | Meeting summaries (various tools) | Head office | shadow-tool | none | 300 | **stop** | Unsanctioned tool with personal or confidential data: move its users to the sanctioned alternative |
| I-25 | Customer churn model (loyalty card) | E-commerce | pilot | none | 0 | **fix** | Missing a baseline and outcome KPI |
| I-26 | Fleet predictive maintenance | Supply chain | vendor-feature | anecdotal | 1.200 | **fix** | Missing a baseline and outcome KPI |
| I-27 | IT service-desk ticket routing | Head office | pilot | measured | 500 | **scale** | Owner, measured value and data access are in place |
| I-28 | Recipe recommender in app | E-commerce | pilot | anecdotal | 800 | **fix** | Missing a baseline and outcome KPI |
| I-29 | Second recipe recommender (marketing agency) | Head office | pilot | none | 2.000 | **merge** | Same problem as I-28: one owner, one tool |
| I-30 | Supplier risk news monitoring | Head office | vendor-feature | none | 450 | **fix** | Missing a baseline and outcome KPI |
| I-31 | Store-level demand forecasting trial | Stores | pilot | measured | 1.600 | **fix** | Missing reliable data access |
| I-32 | Employee HR-policy chatbot | Head office | pilot | anecdotal | 600 | **fix** | Missing a baseline and outcome KPI |
| I-33 | Customer-review sentiment analysis | E-commerce | vendor-feature | anecdotal | 350 | **fix** | Missing a baseline and outcome KPI |
| I-34 | Code assistant pilot (IT, sanctioned) | Head office | pilot | measured | 1.900 | **scale** | Owner, measured value and data access are in place |
| I-35 | Shrinkage anomaly detection (finance) | Head office | pilot | none | 0 | **stop** | No owner and no evidence of value |
| I-36 | Voice ordering for B2B customers | E-commerce | pilot | none | 0 | **stop** | No owner and no evidence of value |
| I-37 | Translation of product labels (FR/NL/DE) | Head office | shadow-tool | anecdotal | 90 | **stop** | Unsanctioned tool with company data: move its users to the sanctioned alternative |
<!--/t-->

## How the triage was received

- **The CV-screening plug-in (I-09)** was the surprise: switched on by the ATS vendor by default, used on every store-job applicant, never assessed. Recruitment is high-risk under Annex III of the AI Act. Paused the same week.
- **Two recipe recommenders and two invoice-extraction trials** were news to the sponsors of each. Merging them was welcomed once the cost per initiative was visible.
- **The store fresh-waste dashboard (I-02)** became the seed of the pilot: managers liked it, but nobody had measured waste. "Fix: missing a baseline" turned into the pilot charter.
