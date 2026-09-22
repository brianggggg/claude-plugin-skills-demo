# Reporting

Repository activity: recent commits and who's contributing.

**Total commits:** 27 · **Contributors:** 2

## Usage Metrics — Planned

Skill and team adoption metrics aren't wired up yet. Here's what's planned, roughly in order of how feasible each one is to actually pull:

| Metric | Level | Source | Status |
|---|---|---|---|
| Claude requests, tokens, spend | Org-wide | Anthropic Usage & Cost Admin API | Feasible once API access is set up |
| Requests by team | Team (workspace) | Anthropic Usage & Cost Admin API, if each team has its own workspace | Feasible, needs workspace-per-team setup |
| Skills invoked, most-used skill | Skill | Custom instrumentation — Anthropic's API doesn't track "skills" as a concept | Needs a logging layer around skill invocation |
| Individual usage stats | Person | Custom authenticated proxy in front of Claude | Under evaluation — see note below |

### A note on individual usage stats

Storing usage events for 40k people isn't a scale problem — any normal database handles that volume easily. The real constraints are:

- **Anthropic's own reporting is by API key and workspace, not by named individual.** Attributing a request to a specific person needs our own layer in front of Claude (an authenticated gateway or proxy) that tags and logs each request — that's a real build, not a reporting toggle.
- **Privacy and HR review.** Individual-level usage dashboards read like productivity monitoring and typically need legal/HR sign-off before they're shown broadly, especially at a regulated company.

Recommendation: start with team-level aggregates (lower lift, no privacy review needed) and treat named-individual stats as a separate initiative pending its own approval.

## Recent Commits

| Commit | Author | Date | Message |
|---|---|---|---|
| `1d5f093` | Claude | 2026-09-22 | Drop homepage CTA buttons, reflow sections, add Additional Resources |
| `7c96441` | Claude | 2026-09-22 | Restructure nav into CitDev Resources / CitDev Inventory, rework homepage |
| `57fdae9` | Claude | 2026-09-22 | Drop What's Claude, widen New here?, reframe as a citizen developer site |
| `e6f7bf9` | Claude | 2026-09-21 | Keep the top nav bar visible down to tablet width |
| `d87b448` | Claude | 2026-09-21 | Add Reporting as the 7th top-level nav tab |
| `6787ba7` | Claude | 2026-09-21 | Add top-level nav for Important links, Report an issue, and Contribute |
| `ad75459` | Claude | 2026-09-21 | Shrink the Skills & Teams column and move the date to the Teams page |
| `3d08543` | Claude | 2026-09-21 | Force the 3-column hero layout and fold the tracker into it |
| `996364d` | Claude | 2026-09-21 | Lay out What's Claude / New here / Skills & Teams as 3 columns |
| `e4ae454` | Claude | 2026-09-21 | Rename site to Claude COE, drop the masthead to save space |

## Contributors

| Name | Commits |
|---|---|
| brianjgonza | 15 |
| Claude | 12 |

[:octicons-arrow-left-24: Back to Home](index.md)
