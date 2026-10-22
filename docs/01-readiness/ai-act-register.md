# EU AI Act register (first pass)

A triage of every use case in the portfolio, for the AI register. It reflects the AI Act as amended by the Digital Omnibus on AI (Regulation (EU) 2026/1744): transparency duties (Art. 50) apply from 2 August 2026; Annex III high-risk obligations from 2 December 2027. **This is a first pass for legal and the DPO, not legal advice.**

| Tier | Count |
|---|---|
| Minimal | <!--n:gov.minimal-->15<!--/n--> |
| Transparency | <!--n:gov.transparency-->8<!--/n--> |
| To be assessed | <!--n:gov.to-->2<!--/n--> |
| High-risk (Annex III) | <!--n:gov.high-risk-->1<!--/n--> |
<!--t:register-->
| Id | Use case | Tier | Decision |
|---|---|---|---|
| UC-01 | Fresh markdown advisor | Minimal | Proceed |
| UC-02 | Store-level automated ordering | Minimal | Proceed |
| UC-03 | Customer-service assistant (one tool) | Transparency | Proceed with transparency |
| UC-04 | Supplier invoice processing at scale | Minimal | Proceed |
| UC-05 | Personalised promotions in the app | Transparency | Proceed with transparency |
| UC-06 | Product content generation (web and labels) | Transparency | Proceed with transparency |
| UC-07 | DC labour planning | Transparency | Proceed with transparency |
| UC-08 | Store staff scheduling | To be assessed | Legal and DPO assessment before build |
| UC-09 | Office productivity assistant | Minimal | Proceed |
| UC-10 | Developer assistant for all IT | Minimal | Proceed |
| UC-11 | Promotion planning optimiser | Minimal | Proceed |
| UC-12 | Refrigeration energy optimisation (all stores) | Minimal | Proceed |
| UC-13 | Fleet predictive maintenance (fix) | Minimal | Proceed |
| UC-14 | IT service-desk automation | Minimal | Proceed |
| UC-15 | HR policy assistant (checked) | Transparency | Proceed with transparency |
| UC-16 | Customer churn and win-back | Transparency | Proceed with transparency |
| UC-17 | Product master-data enrichment | Minimal | Proceed |
| UC-18 | Store operations copilot | Transparency | Proceed with transparency |
| UC-19 | Loss-prevention video analytics | To be assessed | Legal and DPO assessment before build |
| UC-20 | Supplier contract analysis | Minimal | Proceed |
| UC-21 | Shrinkage anomaly detection | Minimal | Proceed |
| UC-22 | CV screening in recruitment | High-risk (Annex III) | Park unless the business case carries full compliance |
| UC-23 | Delivery-slot pricing | Minimal | Proceed |
| UC-24 | Voice ordering for B2B | Transparency | Proceed with transparency |
| UC-25 | Supplier risk monitoring (fix) | Minimal | Proceed |
| UC-26 | Review insights for category managers | Minimal | Proceed |
<!--/t-->

## Notes on the hard cases

- **UC-22 CV screening:** ranking applicants is listed in Annex III point 4(a). Ardena would be a deployer with Art. 26 duties (human oversight, monitoring, logging, informing candidates and workers), and the vendor must show conformity. Parked: the value is small and the human-first principles exclude it.
- **UC-08 store staff scheduling:** depends on design. Scheduling from forecast footfall and stated preferences is not the same as allocating work based on individual behaviour or personal traits (Annex III 4(b)). Assessment before build, with the works council.
- **UC-19 loss-prevention video analytics:** if it identifies individuals by biometrics it falls into Annex III point 1 and raises GDPR article 9 questions; some forms are prohibited. Parked pending assessment.
- **All use cases:** AI literacy (Art. 4) applies to every deployer since 2 February 2025; F5 covers it.
