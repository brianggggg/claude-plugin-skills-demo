# invoice-processor

*Team · v1.2.0 · Business Ops Team*

Extract, validate, and file vendor invoices from PDFs and emails.

## Commands

| Command | Description |
|---|---|
| `/invoice-file` | File a validated invoice into the accounting system under the right cost center |
| `/invoice-intake` | Extract structured data from an invoice attachment and check it against the PO |

## Skills

??? example "invoice-extractor"

    Extracts vendor, invoice number, line items, totals, and due date from an invoice PDF, image, or forwarded email. Use when a user shares an invoice and asks to log, extract, or process it.

??? example "expense-policy-checker"

    Checks expense line items (from a report, invoice, or receipt) against the company spend policy and flags anything over limit, missing a receipt, or in a disallowed category. Use when a user asks to audit, review, or check expenses against policy.

    Also on: expense-audit

[:octicons-arrow-left-24: Back to Teams catalog](index.md)
