# Teams

5 teams have published skills here. Click a team to see what they've shared.

??? note "crm-sync — v1.0.0 · no skills yet"

    Pull, push, and de-duplicate CRM contacts and deals from Claude.

    No skills published yet.

    **Commands**

    | Command | Description |
    |---|---|
    | `/crm-dedupe` | Find likely duplicate contacts/companies and propose merges |
    | `/crm-pull` | Fetch contacts or deals matching a filter from the CRM |
    | `/crm-push` | Create or update a CRM record from data in the conversation |

    [Full team page →](crm-sync.md)

??? note "expense-audit — v1.0.0 · 2 skills"

    Review expense reports and new vendors against company policy.

    ??? example "expense-policy-checker"

        Checks expense line items (from a report, invoice, or receipt) against the company spend policy and flags anything over limit, missing a receipt, or in a disallowed category. Use when a user asks to audit, review, or check expenses against policy.

        Also on: invoice-processor

    ??? example "vendor-risk-review"

        Runs a new vendor through a standard risk checklist covering data access, financial stability signals, and contract terms, then gives an approve/conditional/escalate recommendation. Use when a user asks to vet, review, or assess a new vendor before onboarding.

    **Commands**

    | Command | Description |
    |---|---|
    | `/audit-expenses` | Review a batch of expense line items against policy and flag exceptions |
    | `/review-vendor` | Run a new vendor through the standard risk checklist before onboarding them |

    [Full team page →](expense-audit.md)

??? note "hr-onboarding — v1.0.0 · 1 skill"

    Generate role-specific onboarding checklists and provisioning requests for new hires.

    ??? example "onboarding-checklist"

        Builds a role-specific new-hire onboarding checklist (accounts, equipment, training, introductions) grouped by before day one / week one / first 30 days. Use when a user asks to onboard a new hire or generate an onboarding plan.

    **Commands**

    | Command | Description |
    |---|---|
    | `/onboard-new-hire` | Generate a full onboarding checklist for a new hire's role and team |
    | `/provision-access` | Draft the IT/access-request tickets implied by an onboarding checklist |

    [Full team page →](hr-onboarding.md)

??? note "invoice-processor — v1.2.0 · 2 skills"

    Extract, validate, and file vendor invoices from PDFs and emails.

    ??? example "invoice-extractor"

        Extracts vendor, invoice number, line items, totals, and due date from an invoice PDF, image, or forwarded email. Use when a user shares an invoice and asks to log, extract, or process it.

    ??? example "expense-policy-checker"

        Checks expense line items (from a report, invoice, or receipt) against the company spend policy and flags anything over limit, missing a receipt, or in a disallowed category. Use when a user asks to audit, review, or check expenses against policy.

        Also on: expense-audit

    **Commands**

    | Command | Description |
    |---|---|
    | `/invoice-file` | File a validated invoice into the accounting system under the right cost center |
    | `/invoice-intake` | Extract structured data from an invoice attachment and check it against the PO |

    [Full team page →](invoice-processor.md)

??? note "meeting-ops — v1.1.0 · 2 skills"

    Prep agendas, summarize calls, and turn discussions into weekly reports.

    ??? example "meeting-summarizer"

        Condenses a meeting transcript or raw notes into decisions, action items with owners, and open questions. Use when a user pastes a transcript, forwards meeting notes, or asks "summarize this meeting" / "what did we decide".

    ??? example "weekly-report-writer"

        Rolls scattered updates (Slack messages, meeting notes, ticket status) into one structured weekly status report with highlights, risks, and next steps. Use when a user asks to write, draft, or compile a weekly/status update.

    **Commands**

    | Command | Description |
    |---|---|
    | `/meeting-followup` | Turn a transcript or notes into a summary, action items, and a status update |
    | `/meeting-prep` | Draft an agenda from the meeting's goal and recent related threads |

    [Full team page →](meeting-ops.md)

??? note "Unassigned Skills — 2 skills"

    Not yet published under any team.

    ??? example "contract-redline"

        Reviews a contract draft and flags clauses that are risky, non-standard, or missing entirely (indemnification, liability caps, termination, auto-renewal, data handling). Use when a user shares a contract/agreement and asks for a review, redline, or risk flag.

    ??? example "okr-tracker"

        Turns a status update or set of raw metrics into progress deltas against existing OKRs (on track / at risk / behind, with the delta since last update). Use when a user shares a status update and asks how it maps to their OKRs, or asks for an OKR progress update.
