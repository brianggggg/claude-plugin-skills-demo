# Reporting

Placeholder — pulled from Anthropic's Usage & Cost API once each team is set up as its own workspace, plus a logging layer for skill-level detail.

## Usage Metrics — Planned

Team and org-wide adoption metrics aren't wired up yet. Here's the full set of what's worth pulling once they are, roughly in order of how feasible each one is to actually get:

| Metric | Level | Source | Status |
|---|---|---|---|
| Requests, tokens, spend | Org-wide | Anthropic Usage & Cost Admin API | Feasible once API access is set up |
| Requests by team | Team (workspace) | Anthropic Usage & Cost Admin API, if each team has its own workspace | Feasible, needs workspace-per-team setup |
| Token mix (input / output / cache read+write) | Org-wide | Anthropic Usage API | Feasible once API access is set up |
| Cost by model (Opus / Sonnet / Haiku mix) | Org-wide | Anthropic Cost Admin API | Feasible once API access is set up |
| Prompt cache hit rate & savings | Org-wide | Anthropic Usage API (cache_read_input_tokens vs. total) | Feasible once API access is set up |
| Average tokens per request | Org-wide or team | Derived from requests + tokens totals, no new data needed | Feasible once API access is set up |
| Request volume trend (daily / weekly) | Org-wide or team | Anthropic Usage API, time-bucketed | Feasible once API access is set up |
| Model version / mix adoption | Org-wide or team | Anthropic Usage API, broken out by model | Feasible — flags teams still on older models |
| Batch vs. real-time API split | Org-wide | Anthropic Usage API, if the Message Batches API is in use | Feasible, only useful once batch usage exists |
| Individual usage stats | Person | Custom authenticated proxy in front of Claude | Under evaluation — see note below |

Skill-level detail (which skill, how often) isn't in this table — Anthropic's API has no concept of "skills," so that needs its own logging layer regardless of level. See Next Steps below for the plan to build that layer.

### A note on individual usage stats

Storing usage events for 40k people isn't a scale problem — any normal database handles that volume easily. The real constraints are:

- **Anthropic's own reporting is by API key and workspace, not by named individual.** Attributing a request to a specific person needs our own layer in front of Claude (an authenticated gateway or proxy) that tags and logs each request — that's a real build, not a reporting toggle.
- **Privacy and HR review.** Individual-level usage dashboards read like productivity monitoring and typically need legal/HR sign-off before they're shown broadly, especially at a regulated company.

Recommendation: start with team-level aggregates (lower lift, no privacy review needed) and treat named-individual stats as a separate initiative pending its own approval.

## Next Steps

None of the above is built yet — this is the plan, not a status update. It would ship as a feature of the required plugin the catalog already distributes, not a separate app.

### Scope

Track usage of **catalog-published skills only** — skills that go through this repo's publish/review process and are bundled into a team's plugin. Not third-party or ad-hoc user-created skills, and not named-individual usage (a separate initiative — see the note above).

### The plugin

1. **MCP server**, bundled with the required main plugin already pushed to every user — same distribution mechanism the catalog itself uses. Exposes one tool: `log_skill_usage(skill_name, team, timestamp)`.
2. **Logging instructions injected at build time, not hand-authored per skill.** The publishing pipeline wraps each catalog skill with the logging call automatically when it's packaged for distribution. Source `SKILL.md` files stay untouched, so this applies to every already-published skill with zero edits, and to every future skill automatically.

### The data path

3. **Ingestion:** a Power Automate flow triggered by an HTTP request (not email — instant, structured, no mailbox-polling overhead) writes each event to a SharePoint list.
4. **Retention:** a separate scheduled Power Automate flow purges list items older than 30 days.
5. **Rollup into this site:** a scheduled job (can extend the existing "Docs" GitHub Action) pulls an aggregated summary — counts, not raw events — from the SharePoint list into a small data file in this repo. `generate_repo_summary.py` reads it the same way it already reads the catalog, and the placeholders in the table above become real numbers.

### Open questions before building

- **Approval friction:** does a centrally-required plugin get pre-trusted (silent from the first use), or does each user see a one-time "Always Allow" prompt the first time it fires? Unconfirmed — needs a direct answer from the Enterprise/Cowork admin console or Anthropic account team, since it affects rollout messaging.
- **Distribution mechanism:** confirm Cowork's actual mandatory-plugin push behavior. claude.ai itself doesn't support org-wide admin-pushed custom Skills — Cowork may differ, but that's worth verifying directly rather than assuming.
- **SharePoint throttling at scale:** fine at modest volume; if usage grows large, batch events client-side (a few minutes at a time) rather than firing the webhook per invocation.

## Team Breakdown — Planned

The slice that matters most once usage is wired up: every team in the catalog, side by side. Skills Published is real (pulled from the catalog); the rest are placeholders for the same Usage & Cost API breakdown, per team workspace.

| Team | Skills Published | Requests (30d) | Cost (30d) | Active Users (30d) |
|---|---|---|---|---|
| crm-sync | 0 | — | — | — |
| expense-audit | 2 | — | — | — |
| hr-onboarding | 1 | — | — | — |
| invoice-processor | 2 | — | — | — |
| meeting-ops | 2 | — | — | — |

[:octicons-arrow-left-24: Back to Home](index.md)
