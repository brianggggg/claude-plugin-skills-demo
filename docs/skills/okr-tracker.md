# okr-tracker

*Skill*

Turns a status update or set of raw metrics into progress deltas against existing OKRs (on track / at risk / behind, with the delta since last update). Use when a user shares a status update and asks how it maps to their OKRs, or asks for an OKR progress update.

## Used by

Not currently bundled by any plugin — available standalone.

## Full skill definition

??? note "SKILL.md contents"

    ```markdown
    # OKR Tracker

    Map a status update onto existing objectives and key results.

    ## Process

    1. Ask for (or use, if already provided) the current OKR set with baseline and target values.
    2. For each key result mentioned in the update, compute the new value and the delta from the last known value.
    3. Classify each key result: `on track`, `at risk`, or `behind` — based on whether the current pace would hit the target by the deadline, not just current-vs-target snapshot.
    4. Call out any key result with **no update** this period as a gap, not a silent pass.
    5. Output a table: Key Result | Baseline | Target | Current | Delta | Status.
    ```

[:octicons-arrow-left-24: Back to Skills catalog](index.md)
