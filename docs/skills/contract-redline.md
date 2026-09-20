# contract-redline

*Skill*

Reviews a contract draft and flags clauses that are risky, non-standard, or missing entirely (indemnification, liability caps, termination, auto-renewal, data handling). Use when a user shares a contract/agreement and asks for a review, redline, or risk flag.

## Used by

Not currently published by any team — available standalone.

## Full skill definition

??? note "SKILL.md contents"

    ```markdown
    # Contract Redline

    Flag risk in a contract draft — this is a first-pass triage, not a legal opinion.

    ## Clauses to always check

    - **Liability cap** — present? Uncapped liability is a flag.
    - **Indemnification** — mutual, or one-sided against your company?
    - **Auto-renewal** — present, and if so, what's the opt-out notice window?
    - **Termination for convenience** — can either party exit, and on what notice?
    - **Data handling / confidentiality** — does it meet your company's minimum data-handling terms?
    - **Governing law / venue** — flag anything outside the company's standard jurisdiction.

    ## Process

    1. Go clause by clause; don't skip boilerplate — that's where risk hides.
    2. For each flagged clause, quote the exact language, state the risk in one sentence, and suggest fallback language.
    3. Explicitly list which of the standard clauses above are **missing** from the draft, not just which are risky.
    4. End with a one-line overall risk rating (low/medium/high) and a note that this is a first-pass flag for legal review, not a substitute for it.
    ```

[:octicons-arrow-left-24: Back to Skills catalog](index.md)
