# Claude Plugin & Skills Demo

A demo repository showing what a small internal **Claude plugin marketplace** and **skill library** look like for a business-operations team.

- `plugins/` — 5 plugins, each a bundle of commands (and sometimes skills) around one workflow (CRM, invoicing, meetings, onboarding, expense audit).
- `skills/` — 8 standalone skills, each a single-purpose capability that plugins (or users directly) can invoke.
- `.claude-plugin/marketplace.json` — the marketplace manifest listing all 5 plugins.

See the auto-generated [repo summary site](docs/index.md) for a live catalog of everything in here — it rebuilds on every push via `scripts/generate_repo_summary.py` and GitHub Actions.
