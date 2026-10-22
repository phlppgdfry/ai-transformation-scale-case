# Use-case portfolio

<!--n:pf.count-->26<!--/n--> use cases from the workshops, including the existing initiatives worth continuing. Each one is scored on value, strategic fit and feasibility with the weights agreed in workshop 1 ([`data/weights.json`](../../data/weights.json)).

## Method

| Element | How |
|---|---|
| Value score (1–5) | Mid-point of the annual value range from the workshop, on a log scale between the smallest and largest use case |
| Strategic fit (1–5) | ExCo judgement against the three AI outcomes from workshop 1 |
| Feasibility (1–5) | Weighted mean of data readiness (0.40), technical maturity (0.25) and organisational readiness (0.35) |
| Priority | 0.40 × value + 0.20 × fit + 0.40 × feasibility − 0.5 if the AI Act triage says "to be assessed" |
| Class | Quick win (feasible, ≤ 3 months), strategic bet (high value or fit, harder), fill-in, park (high-risk or low/low) |

Why a log scale for value: a €3m use case is not thirty times more attractive than a €100k one once risk and effort are counted, and a linear scale lets one large estimate dominate the whole ranking.

## Ranking
<!--t:portfolio-->
| Rank | Id | Use case | Unit | Value | Fit | Feasibility | Priority | Class | Top-5 share |
|---|---|---|---|---|---|---|---|---|---|
| 1 | UC-01 | Fresh markdown advisor | Stores | 4.4 | 5 | 3.6 | 4.20 | strategic bet | 93% |
| 2 | UC-05 | Personalised promotions in the app | E-commerce | 4.6 | 5 | 2.6 | 3.92 | strategic bet | 79% |
| 3 | UC-02 | Store-level automated ordering | Stores | 5.0 | 5 | 2.2 | 3.90 | strategic bet | 76% |
| 4 | UC-12 | Refrigeration energy optimisation (all stores) | Stores | 3.1 | 3 | 4.2 | 3.55 | quick win | 40% |
| 5 | UC-11 | Promotion planning optimiser | Head office | 4.1 | 4 | 2.6 | 3.51 | strategic bet | 53% |
| 6 | UC-03 | Customer-service assistant (one tool) | Head office | 3.0 | 3 | 4.2 | 3.49 | quick win | 32% |
| 7 | UC-23 | Delivery-slot pricing | E-commerce | 3.6 | 4 | 3.0 | 3.46 | strategic bet | 52% |
| 8 | UC-07 | DC labour planning | Supply chain | 3.5 | 4 | 3.0 | 3.42 | strategic bet | 6% |
| 9 | UC-16 | Customer churn and win-back | E-commerce | 3.3 | 3 | 3.6 | 3.37 | quick win | 0% |
| 10 | UC-18 | Store operations copilot | Stores | 3.5 | 4 | 2.9 | 3.36 | strategic bet | 16% |
| 11 | UC-06 | Product content generation (web and labels) | E-commerce | 2.6 | 3 | 4.2 | 3.34 | quick win | 20% |
| 12 | UC-04 | Supplier invoice processing at scale | Head office | 2.8 | 3 | 4.0 | 3.32 | fill-in | 3% |
| 13 | UC-09 | Office productivity assistant | Head office | 2.7 | 2 | 4.3 | 3.21 | quick win | 10% |
| 14 | UC-10 | Developer assistant for all IT | Head office | 2.2 | 2 | 4.7 | 3.14 | quick win | 17% |
| 15 | UC-17 | Product master-data enrichment | Head office | 2.5 | 3 | 3.6 | 3.04 | quick win | 0% |
| 16 | UC-21 | Shrinkage anomaly detection | Head office | 2.8 | 3 | 3.2 | 3.02 | fill-in | 0% |
| 17 | UC-14 | IT service-desk automation | Head office | 1.9 | 2 | 4.2 | 2.86 | quick win | 1% |
| 18 | UC-08 | Store staff scheduling | Stores | 3.9 | 4 | 2.2 | 2.74 | strategic bet | 0% |
| 19 | UC-13 | Fleet predictive maintenance (fix) | Supply chain | 2.1 | 2 | 3.6 | 2.71 | quick win | 0% |
| 20 | UC-15 | HR policy assistant (checked) | Head office | 1.4 | 2 | 4.2 | 2.66 | quick win | 0% |
| 21 | UC-20 | Supplier contract analysis | Head office | 1.7 | 2 | 3.6 | 2.53 | quick win | 0% |
| 22 | UC-26 | Review insights for category managers | E-commerce | 1.3 | 2 | 3.9 | 2.49 | quick win | 0% |
| 23 | UC-22 | CV screening in recruitment | Head office | 1.9 | 2 | 3.3 | 2.49 | park | 0% |
| 24 | UC-19 | Loss-prevention video analytics | Stores | 3.2 | 3 | 1.9 | 2.14 | park | 0% |
| 25 | UC-25 | Supplier risk monitoring (fix) | Head office | 1.0 | 2 | 3.3 | 2.12 | fill-in | 0% |
| 26 | UC-24 | Voice ordering for B2B | E-commerce | 1.2 | 1 | 2.6 | 1.73 | park | 0% |
<!--/t-->

**Classes:** <!--n:pf.quick_win-->12<!--/n--> quick wins, <!--n:pf.strategic_bet-->8<!--/n--> strategic bets, <!--n:pf.fill-in-->3<!--/n--> fill-ins, <!--n:pf.park-->3<!--/n--> parked.

## Robustness

Workshop weights are a negotiation, not a law. We re-drew all six weights at random 2,000 times and recorded how often each use case lands in the top five.

- **<!--n:pf.first-->Fresh markdown advisor<!--/n-->** is in the top five in <!--n:pf.UC-01.top5-->93%<!--/n--> of weightings and first in <!--n:pf.UC-01.top1-->57%<!--/n-->. That is a robust first choice, and why it became the pilot.
- **Personalised promotions (UC-05)** and **store-level ordering (UC-02)** are in the top five in <!--n:pf.UC-05.top5-->79%<!--/n--> and <!--n:pf.UC-02.top5-->76%<!--/n-->: robust strategic bets, but they need the data platform first.
- Use cases that need a specific weighting to rank high are flagged in the table; the ExCo decides them explicitly, not by accident of the formula.

## What the portfolio is not

A score is a conversation starter, not a decision. Three use cases got an explicit decision in workshop 5 that the score alone would not have given:

- **Store operations copilot (UC-18)** scored mid-table, but the COO argued it is the way to bring AI to 8,200 store staff. Kept as a strategic bet, after F2 and F5.
- **Customer churn (UC-16)** has a model already built (I-25) that nobody used. Kept as a quick win only with a holdout group in the first campaign; otherwise it is the same failure again.
- **Loss-prevention video analytics (UC-19)** had sponsors and a vendor. Parked on the human-first principles and the AI Act assessment, not on its score.
