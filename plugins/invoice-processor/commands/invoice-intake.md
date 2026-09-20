---
description: Extract structured data from an invoice attachment and check it against the PO
---

Process the invoice attached to this conversation (or referenced in `$ARGUMENTS`).

1. Use the `invoice-extractor` skill to pull vendor, invoice number, line items, and total.
2. Look up the matching purchase order, if one is referenced.
3. Flag any mismatch between invoiced amount and PO amount.
4. Use the `expense-policy-checker` skill to flag any line item outside policy.
5. Summarize findings and ask for approval before filing.
