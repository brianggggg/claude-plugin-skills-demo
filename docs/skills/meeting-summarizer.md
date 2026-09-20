# meeting-summarizer

*Skill*

Condenses a meeting transcript or raw notes into decisions, action items with owners, and open questions. Use when a user pastes a transcript, forwards meeting notes, or asks "summarize this meeting" / "what did we decide".

## Used by

- [meeting-ops](../plugins/meeting-ops.md)

## Full skill definition

??? note "SKILL.md contents"

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

[:octicons-arrow-left-24: Back to Skills catalog](index.md)
