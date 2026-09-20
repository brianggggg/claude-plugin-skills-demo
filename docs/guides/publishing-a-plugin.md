# Publishing a Plugin

A plugin bundles one or more ready-to-run slash commands — and optionally, existing skills — around a single workflow, like "invoice processing" or "meeting ops." Here's how to add one.

## 1. Create the plugin folder

```
plugins/your-plugin-name/
  .claude-plugin/
    plugin.json
  commands/
    your-command.md
```

## 2. Fill in `plugin.json`

```json
{
  "name": "your-plugin-name",
  "description": "One sentence describing what this plugin is for.",
  "version": "1.0.0",
  "author": { "name": "Your Team" }
}
```

## 3. Add one file per command

Each command lives in `commands/` as its own Markdown file. The filename becomes the command name — `commands/audit-expenses.md` becomes `/audit-expenses`.

```markdown
---
description: One-line description shown in the catalog
---

Step-by-step instructions for what this command should do when it runs,
including which skill(s) to lean on for the actual reasoning.
```

## 4. (Optional) Bundle existing skills

If your plugin should use one or more skills already in the [Skills catalog](../skills/index.md), list their names in a `skills.json` file next to `plugin.json`:

```
plugins/your-plugin-name/skills.json
```

```json
["skill-one", "skill-two"]
```

This is what powers the "bundled skills" and "used by" cross-links you see on the catalog pages — it's read automatically, you don't need to update anything else.

## 5. Register it in the marketplace

Add an entry to `.claude-plugin/marketplace.json` at the repo root so the plugin is discoverable:

```json
{
  "name": "your-plugin-name",
  "source": "./plugins/your-plugin-name",
  "description": "Same one-sentence description as above."
}
```

## 6. Submit it

Same as skills — open a pull request with your new files, or ask a teammate (or Claude Code, pointed at this repository) to do the git mechanics for you.

## 7. What happens next

Once merged, the site rebuilds automatically. Your plugin appears on the [Plugins catalog](../plugins/index.md) with its commands and bundled skills, and each bundled skill's own page updates to show it's now "used by" your plugin too.
