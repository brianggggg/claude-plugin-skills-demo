# expense-audit

*Team · v1.0.0 · Business Ops Team*

Review expense reports and new vendors against company policy.

## Commands

| Command | Description |
|---|---|
| `/audit-expenses` | Review a batch of expense line items against policy and flag exceptions |
| `/review-vendor` | Run a new vendor through the standard risk checklist before onboarding them |

## Bundled skills

<div class="grid cards" markdown>

-   :material-flash-outline:{ .lg .middle } __expense-policy-checker__

    ---

    Checks expense line items (from a report, invoice, or receipt) against the company spend policy and flags anything over limit, missing a receipt, or in a disallowed category. Use when a user asks to audit, review, or check expenses against policy.

    Also on: invoice-processor

    [:octicons-arrow-right-24: View skill](../skills/expense-policy-checker.md)


-   :material-flash-outline:{ .lg .middle } __vendor-risk-review__

    ---

    Runs a new vendor through a standard risk checklist covering data access, financial stability signals, and contract terms, then gives an approve/conditional/escalate recommendation. Use when a user asks to vet, review, or assess a new vendor before onboarding.

    Published by this team

    [:octicons-arrow-right-24: View skill](../skills/vendor-risk-review.md)


</div>

[:octicons-arrow-left-24: Back to Teams catalog](index.md)
