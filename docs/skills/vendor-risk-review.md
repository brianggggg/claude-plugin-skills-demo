# vendor-risk-review

*Skill*

Runs a new vendor through a standard risk checklist covering data access, financial stability signals, and contract terms, then gives an approve/conditional/escalate recommendation. Use when a user asks to vet, review, or assess a new vendor before onboarding.

## Used by

- [expense-audit](../plugins/expense-audit.md)

## Full skill definition

??? note "SKILL.md contents"

    ```markdown
    # Vendor Risk Review

    Assess a prospective vendor before they're onboarded.

    ## Checklist

    - **Data access** — what company/customer data would this vendor touch? Flag any PII or financial data access.
    - **Security posture** — do they have a SOC 2 (or equivalent) report, or a documented security policy?
    - **Financial stability** — any public signals of distress (layoffs, funding issues, negative press)?
    - **Contract terms** — check against the `contract-redline` skill's standard clause list if a draft agreement exists.
    - **Concentration risk** — is this vendor a single point of failure for something business-critical?

    ## Process

    1. Work through the checklist in order; don't skip a section just because early ones look fine.
    2. Mark each item `pass`, `needs more info`, or `concern` with a one-line reason.
    3. Recommend one of: **approve**, **approve with conditions** (name them), or **escalate** (name who/why).
    4. Never recommend "approve" if data access and security posture haven't both been checked.
    ```

[:octicons-arrow-left-24: Back to Skills catalog](index.md)
