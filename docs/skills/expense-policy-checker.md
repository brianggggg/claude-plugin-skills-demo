# expense-policy-checker

*Skill*

Checks expense line items (from a report, invoice, or receipt) against the company spend policy and flags anything over limit, missing a receipt, or in a disallowed category. Use when a user asks to audit, review, or check expenses against policy.

## Used by

- [expense-audit](../plugins/expense-audit.md)
- [invoice-processor](../plugins/invoice-processor.md)

## Full skill definition

??? note "SKILL.md contents"

    ```markdown
    # Expense Policy Checker

    Evaluate expense line items against standard policy thresholds.

    ## Default policy rules (override with the company's actual policy doc if provided)

    - Meals: flag if a single meal exceeds $75/person, or if alcohol is itemized separately.
    - Travel: flag any airfare above economy class without a stated exception.
    - Lodging: flag nightly rates above the metro-tier cap ($250 standard / $400 high-cost city).
    - Software/subscriptions: flag anything not already on the approved-vendor list.
    - Receipts: flag any line item over $25 with no attached receipt.

    ## Process

    1. Evaluate every line item independently — one violation doesn't invalidate the rest of the report.
    2. Classify each item as `clean`, `needs receipt`, or `policy violation`, with the specific rule cited.
    3. Total the dollar amount in each classification bucket.
    4. Never approve or reject a report yourself — present findings for a human to decide on.
    ```

[:octicons-arrow-left-24: Back to catalog](../index.md)
