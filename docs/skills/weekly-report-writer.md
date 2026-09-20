# weekly-report-writer

*Skill*

Rolls scattered updates (Slack messages, meeting notes, ticket status) into one structured weekly status report with highlights, risks, and next steps. Use when a user asks to write, draft, or compile a weekly/status update.

## Used by

- [meeting-ops](../plugins/meeting-ops.md)

## Full skill definition

??? note "SKILL.md contents"

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

[:octicons-arrow-left-24: Back to catalog](../index.md)
