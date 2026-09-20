# invoice-processor

Turns an inbound invoice (PDF, image, or forwarded email) into a validated, filed expense record.

## Commands

| Command | Description |
|---|---|
| `/invoice-intake` | Extract structured data from an invoice attachment and check it against the PO. |
| `/invoice-file` | File a validated invoice into the accounting system under the right cost center. |

## Bundled skills

- `invoice-extractor` — pulls line items, totals, and vendor details out of the source document.
- `expense-policy-checker` — flags anything that doesn't match spend policy before filing.
