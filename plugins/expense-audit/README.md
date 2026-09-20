# expense-audit

Reviews spend — both employee expense reports and new vendors — against company policy.

## Commands

| Command | Description |
|---|---|
| `/audit-expenses` | Review a batch of expense line items against policy and flag exceptions. |
| `/review-vendor` | Run a new vendor through the standard risk checklist before onboarding them. |

## Bundled skills

- `expense-policy-checker` — the policy rules engine both commands rely on.
- `vendor-risk-review` — the vendor-specific risk checklist.
