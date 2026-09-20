# Publishing a Skill

A skill is a single-purpose instruction set that teaches Claude how to do one job well — like "summarize a meeting" or "check an expense against policy." Anyone on the team can propose one. Here's how it goes from idea to something everyone can use.

## 1. Write the skill

Create a new folder under `skills/` named after your skill — lowercase, hyphens instead of spaces — with one file inside called `SKILL.md`:

```
skills/your-skill-name/SKILL.md
```

Start from this template:

```markdown
---
name: your-skill-name
description: One or two sentences describing what this does AND when Claude should use it.
---

# Your Skill Name

Plain-language instructions for how to do the task well: the steps to
follow, what to check, what "good" looks like, and any edge cases to
watch for.
```

## 2. Get the `description` right

The `description` field does double duty — it's both the summary shown in the catalog **and** the only thing Claude reads to decide *when* to use the skill. Be specific about the trigger: what will the person say or share that should make Claude reach for this skill? Compare:

- Vague: *"Helps with expenses."*
- Specific: *"Checks expense line items against company spend policy and flags anything over limit. Use when a user asks to audit, review, or check expenses against policy."*

## 3. Write instructions Claude can actually follow

Think of the body of `SKILL.md` as onboarding a very capable new teammate who's never done this task before:

- Give the steps in order.
- Call out what "done well" looks like, not just "done."
- Name the edge cases that trip people up (missing data, ambiguous input) and say what to do about them — flag it, ask, or use a stated default. Don't leave Claude to guess silently.

Look at an existing skill's `SKILL.md` file in the `skills/` folder for a worked example.

## 4. Submit it

If you don't use git day-to-day, the easiest path is to ask a teammate with repo access — or ask Claude Code itself, pointing it at this repository — to:

1. Create a new branch
2. Add your `SKILL.md` file under `skills/<your-skill-name>/`
3. Open a pull request so the team can review it

## 5. What happens next

Once your pull request is approved and merged, the site rebuilds automatically. Your skill appears within a couple of minutes on the [Teams catalog](../plugins/index.md) — nested under whichever team bundles it, or under "Unassigned Skills" if it isn't bundled by a team yet. No manual publishing step.

Want your team's skills published together under one name, or wired up as a slash command? See [Registering a Team](publishing-a-plugin.md).
