# Teams

5 teams have published skills here. Click a team to see what they've shared, or see the [Skills catalog](../skills/index.md) to browse by skill instead.

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

        ??? note "Full skill definition"

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

    ??? example "vendor-risk-review"

        Runs a new vendor through a standard risk checklist covering data access, financial stability signals, and contract terms, then gives an approve/conditional/escalate recommendation. Use when a user asks to vet, review, or assess a new vendor before onboarding.

        ??? note "Full skill definition"

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

        ??? note "Full skill definition"

            ```markdown
            # Onboarding Checklist

            Generate a checklist tailored to the new hire's role, not a generic template.

            ## Inputs needed

            - Role/title and team
            - Start date
            - Manager name
            - Whether the role needs elevated system access (finance, prod infra, customer data, etc.)

            ## Process

            1. Start from the standard baseline: laptop/equipment, email + SSO, org-chart intro, benefits enrollment, first 1:1 with manager.
            2. Add role-specific items — e.g. an engineer needs repo/VPN access and a dev environment; a salesperson needs CRM access and territory assignment.
            3. If the role touches sensitive systems, add the corresponding access-request step rather than assuming standard equipment covers it.
            4. Group the output into **before day one**, **week one**, and **first 30 days**, each as a checkbox list.
            5. Flag any input you didn't get (e.g. no manager name) instead of leaving that step vague.
            ```

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

        ??? note "Full skill definition"

            ```markdown
            # Invoice Extractor

            Pull structured data out of an invoice document.

            ## Fields to extract

            - Vendor name and remit-to address
            - Invoice number and invoice date
            - Due date and payment terms
            - Line items: description, quantity, unit price, line total
            - Subtotal, tax, and grand total
            - Purchase order number, if referenced

            ## Process

            1. Read the entire document before extracting — totals at the bottom confirm line-item math.
            2. If the extracted line-item sum doesn't match the stated total, flag the discrepancy rather than silently trusting either number.
            3. Leave a field blank (not guessed) when it isn't present in the source document.
            4. Output the result as a JSON object matching the fields above, followed by a one-line human-readable summary.
            ```

    ??? example "expense-policy-checker"

        Checks expense line items (from a report, invoice, or receipt) against the company spend policy and flags anything over limit, missing a receipt, or in a disallowed category. Use when a user asks to audit, review, or check expenses against policy.

        Also on: expense-audit

        ??? note "Full skill definition"

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

        ??? note "Full skill definition"

            ````markdown
            # Meeting Summarizer

            Turn unstructured meeting input into a short, scannable summary.

            ## Process

            1. Read the full transcript/notes before summarizing — don't summarize incrementally.
            2. Extract three sections, in this order:
               - **Decisions** — anything the group explicitly agreed on.
               - **Action items** — task, owner, and due date if stated (mark "unassigned" or "no date" rather than guessing).
               - **Open questions** — things raised but not resolved.
            3. Keep each bullet to one line. Don't restate discussion that led nowhere.
            4. If the transcript has no clear decisions or action items, say so rather than inventing them.

            ## Output format

            ```
            ## Decisions
            - ...

            ## Action Items
            - [ ] Task — @owner — due date

            ## Open Questions
            - ...
            ```
            ````

    ??? example "weekly-report-writer"

        Rolls scattered updates (Slack messages, meeting notes, ticket status) into one structured weekly status report with highlights, risks, and next steps. Use when a user asks to write, draft, or compile a weekly/status update.

        ??? note "Full skill definition"

            ```markdown
            # Weekly Report Writer

            Compile scattered inputs into one coherent weekly report.

            ## Process

            1. Gather every input the user provides (notes, meeting summaries, ticket links) before drafting — don't write from partial context.
            2. Organize into three sections:
               - **Highlights** — what shipped or got decided this week.
               - **Risks / blockers** — anything at risk, with what's needed to unblock it.
               - **Next week** — what's planned.
            3. Attribute items to the person or team responsible when that's known.
            4. Keep it to bullets, not paragraphs — this is a status report, not a narrative.
            5. If an input is ambiguous (e.g. unclear whether something shipped or is still in progress), ask rather than guessing the status.
            ```

    **Commands**

    | Command | Description |
    |---|---|
    | `/meeting-followup` | Turn a transcript or notes into a summary, action items, and a status update |
    | `/meeting-prep` | Draft an agenda from the meeting's goal and recent related threads |

    [Full team page →](meeting-ops.md)
