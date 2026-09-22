# Registering a Team

A team is how you package and publish your skills for everyone else to use — it's not a separate workflow, just the publishing unit. Commands are optional, for when you want something runnable as a slash command too. Here's how to add one.

*(Technical note: under the hood this still uses a `plugins/` folder structure — the site just presents it as "Teams.")*

## 1. Create the team's folder

```
plugins/your-team-name/
  .claude-plugin/
    plugin.json
```

## 2. Fill in `plugin.json`

```json
{
  "name": "your-team-name",
  "description": "One sentence describing what this team publishes.",
  "version": "1.0.0",
  "author": { "name": "Your Team" }
}
```

## 3. Bundle your team's skills

List the skills this team publishes — already published under another team on the [CitDev Inventory](../plugins/index.md) (or under "Unassigned Skills" there), or new ones you're adding alongside it in the `skills/` folder — in a `skills.json` file next to `plugin.json`:

```
plugins/your-team-name/skills.json
```

```json
["skill-one", "skill-two"]
```

This is what powers the accordion and "used by" cross-links you see on the catalog pages — it's read automatically, you don't need to update anything else.

## 4. (Optional) Add a slash command

If you want a skill (or a sequence of them) runnable directly as a slash command, add a `commands/` folder:

```
plugins/your-team-name/commands/your-command.md
```

```markdown
---
description: One-line description shown in the catalog
---

Step-by-step instructions for what this command should do when it runs,
including which skill(s) to lean on for the actual reasoning.
```

The filename becomes the command name — `commands/audit-expenses.md` becomes `/audit-expenses`.

## 5. Register it in the marketplace

Add an entry to `.claude-plugin/marketplace.json` at the repo root so your team is discoverable:

```json
{
  "name": "your-team-name",
  "source": "./plugins/your-team-name",
  "description": "Same one-sentence description as above."
}
```

## 6. Submit it

Same as skills — open a pull request with your new files, or ask a teammate (or Claude, pointed at this repository) to do the git mechanics for you.

## 7. What happens next

Once merged, the site rebuilds automatically. Your team appears on the [CitDev Inventory](../plugins/index.md) with its published skills (and any commands) nested inside its accordion entry.
