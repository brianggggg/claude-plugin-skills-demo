# Publishing a Plugin

A plugin is how your team packages and publishes its skills for everyone else to use — it's not a separate workflow, just the publishing unit. Commands are optional, for when you want something runnable as a slash command too. Here's how to add one.

## 1. Create the plugin folder

```
plugins/your-plugin-name/
  .claude-plugin/
    plugin.json
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

## 3. Bundle your team's skills

List the skills this plugin publishes — already in the [Skills catalog](../skills/index.md), or new ones you're adding alongside it — in a `skills.json` file next to `plugin.json`:

```
plugins/your-plugin-name/skills.json
```

```json
["skill-one", "skill-two"]
```

This is what powers the "bundled skills" and "used by" cross-links you see on the catalog pages — it's read automatically, you don't need to update anything else.

## 4. (Optional) Add a slash command

If you want a skill (or a sequence of them) runnable directly as a slash command, add a `commands/` folder:

```
plugins/your-plugin-name/commands/your-command.md
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

Once merged, the site rebuilds automatically. Your plugin appears on the [Plugins catalog](../plugins/index.md) with its bundled skills (and any commands), and each bundled skill's own page updates to show it's now "used by" your plugin too.
