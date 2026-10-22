# AI operating model and governance

The goal is not control for its own sake. It is to make the *right* AI use faster and the wrong one visible. Today, a store manager who wants a sanctioned AI tool has no route at all, so the fastest route is a credit card.

## Structure: hub and spoke

```mermaid
flowchart TB
    exco[Executive committee<br/>portfolio and budget, twice a year]
    council[AI council, bi-weekly<br/>CIO chair, CFO, COO stores, HR, DPO, CISO,<br/>head of AI office]
    office[AI office: the hub, 4 FTE<br/>intake, register, policy, platform product owner,<br/>value tracking, literacy programme]
    platform[Platform team<br/>orchestration layer F2, data platform F1]
    squads[Product squads<br/>build track]
    adopt[Adoption track<br/>buy and configure, with IT]
    spokes[Spokes in each business unit<br/>AI lead, product owners, 60 champions]
    exco --> council --> office
    office --> platform
    office --> squads
    office --> adopt
    spokes <--> office
    spokes --> squads
```

| Choice | Why |
|---|---|
| Hub and spoke, not a fully central CoE | Value sits in the business units; a central team that builds everything becomes the bottleneck. The hub sets the rules and runs the platform; the spokes own the use cases. |
| Not fully federated | With governance at 1.8, letting every unit do its own thing is how Ardena got 37 initiatives. |
| CIO chairs the council, CFO sits on it | AI spend becomes visible per initiative and stoppable. |
| DPO and CISO are members, not reviewers at the end | Risk questions are answered at intake, not after the build. |

## Intake: three lanes by risk

```mermaid
flowchart LR
    idea[Idea or request] --> form[Intake form, 10 questions<br/>purpose, data, users, AI Act triage]
    form --> t{Risk tier}
    t -->|Tier 1: sanctioned tool,<br/>no personal data| fast[Approved by the AI office<br/>within 5 working days]
    t -->|Tier 2: personal data<br/>or customer-facing| std[Council decision<br/>DPIA screening, transparency]
    t -->|Tier 3: possibly high-risk<br/>Annex III| deep[Legal + DPO assessment<br/>works council if staff affected<br/>ExCo if it goes ahead]
    fast --> reg[(AI register)]
    std --> reg
    deep --> reg
```

The fast lane is the point. If Tier 1 takes five weeks, shadow AI comes back.

## RACI for the main decisions

| Decision | ExCo | AI council | AI office | BU owner | DPO / CISO | Works council |
|---|---|---|---|---|---|---|
| Portfolio and budget | **A** | R | C | C | I | I |
| Approve a Tier 1 use | I | I | **A/R** | C | I | — |
| Approve a Tier 2 use | I | **A** | R | C | C | I |
| Approve a Tier 3 use | **A** | R | R | C | C | C |
| Stop an initiative | I | **A** | R | C | I | — |
| Choose a model or vendor for the platform | I | **A** | R | C | C | — |
| Go-live of a use case | I | C | C | **A/R** | C | I |

(A = accountable, exactly one per decision; R = responsible; C = consulted; I = informed.)

## Policy and principles

- [AI policy](ai-policy.md): one page for every employee
- [Human-first principles](human-first-principles.md): what Ardena will and will not do with AI towards staff and customers
- [AI Act register](ai-act-register.md) and [ISO/IEC 27001 and 42001 alignment](iso-27001-and-42001.md)
- The [orchestration layer](orchestration-layer.md) is how the policy becomes the easy path rather than a document.
