# Reporting

Repository activity: recent commits and who's contributing.

**Total commits:** 28 · **Contributors:** 2

## Usage Metrics — Planned

Team and org-wide adoption metrics aren't wired up yet. Here's what's planned, roughly in order of how feasible each one is to actually pull:

| Metric | Level | Source | Status |
|---|---|---|---|
| Requests, tokens, spend | Org-wide | Anthropic Usage & Cost Admin API | Feasible once API access is set up |
| Requests by team | Team (workspace) | Anthropic Usage & Cost Admin API, if each team has its own workspace | Feasible, needs workspace-per-team setup |
| Token mix (input / output / cache read+write) | Org-wide | Anthropic Usage API | Feasible once API access is set up |
| Cost by model (Opus / Sonnet / Haiku mix) | Org-wide | Anthropic Cost Admin API | Feasible once API access is set up |
| Prompt cache hit rate & savings | Org-wide | Anthropic Usage API (cache_read_input_tokens vs. total) | Feasible once API access is set up |
| Individual usage stats | Person | Custom authenticated proxy in front of Claude | Under evaluation — see note below |

Skill-level detail (which skill, how often) isn't in this table — Anthropic's API has no concept of "skills," so that needs its own logging layer regardless of level. See the homepage's Top Skills preview for where that will surface once it exists.

### A note on individual usage stats

Storing usage events for 40k people isn't a scale problem — any normal database handles that volume easily. The real constraints are:

- **Anthropic's own reporting is by API key and workspace, not by named individual.** Attributing a request to a specific person needs our own layer in front of Claude (an authenticated gateway or proxy) that tags and logs each request — that's a real build, not a reporting toggle.
- **Privacy and HR review.** Individual-level usage dashboards read like productivity monitoring and typically need legal/HR sign-off before they're shown broadly, especially at a regulated company.

Recommendation: start with team-level aggregates (lower lift, no privacy review needed) and treat named-individual stats as a separate initiative pending its own approval.

## Team Breakdown — Planned

The slice that matters most once usage is wired up: every team in the catalog, side by side. Skills Published is real (pulled from the catalog); the rest are placeholders for the same Usage & Cost API breakdown, per team workspace.

| Team | Skills Published | Requests (30d) | Cost (30d) | Active Users (30d) |
|---|---|---|---|---|
| crm-sync | 0 | — | — | — |
| expense-audit | 2 | — | — | — |
| hr-onboarding | 1 | — | — | — |
| invoice-processor | 2 | — | — | — |
| meeting-ops | 2 | — | — | — |

## Recent Commits

| Commit | Author | Date | Message |
|---|---|---|---|
| `2bbab3b` | Claude | 2026-09-22 | Curate homepage metrics, add a real usage-metrics roadmap to Reporting |
| `1d5f093` | Claude | 2026-09-22 | Drop homepage CTA buttons, reflow sections, add Additional Resources |
| `7c96441` | Claude | 2026-09-22 | Restructure nav into CitDev Resources / CitDev Inventory, rework homepage |
| `57fdae9` | Claude | 2026-09-22 | Drop What's Claude, widen New here?, reframe as a citizen developer site |
| `e6f7bf9` | Claude | 2026-09-21 | Keep the top nav bar visible down to tablet width |
| `d87b448` | Claude | 2026-09-21 | Add Reporting as the 7th top-level nav tab |
| `6787ba7` | Claude | 2026-09-21 | Add top-level nav for Important links, Report an issue, and Contribute |
| `ad75459` | Claude | 2026-09-21 | Shrink the Skills & Teams column and move the date to the Teams page |
| `3d08543` | Claude | 2026-09-21 | Force the 3-column hero layout and fold the tracker into it |
| `996364d` | Claude | 2026-09-21 | Lay out What's Claude / New here / Skills & Teams as 3 columns |

## Contributors

| Name | Commits |
|---|---|
| brianjgonza | 15 |
| Claude | 13 |

[:octicons-arrow-left-24: Back to Home](index.md)
