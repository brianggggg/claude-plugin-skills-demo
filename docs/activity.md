# Reporting

Placeholder — pulled from Anthropic's Usage & Cost API and Organization Analytics API once each is wired up. See Next Steps below.

## Usage Metrics — Planned

Team and org-wide adoption metrics aren't wired up yet. Here's the full set of what's worth pulling once they are, roughly in order of how feasible each one is to actually get:

| Metric | Level | Source | Status |
|---|---|---|---|
| Requests, tokens, spend | Org-wide | Anthropic Usage & Cost Admin API | Feasible once API access is set up |
| Requests by team | Team (workspace) | Anthropic Usage & Cost Admin API, if each team has its own workspace | Feasible, needs workspace-per-team setup |
| Token mix (input / output / cache read+write) | Org-wide | Anthropic Usage API | Feasible once API access is set up |
| Prompt cache hit rate & savings | Org-wide | Anthropic Usage API (cache_read_input_tokens vs. total) | Feasible once API access is set up |
| Average tokens per request | Org-wide or team | Derived from requests + tokens totals, no new data needed | Feasible once API access is set up |
| Request volume trend (daily / weekly) | Org-wide or team | Anthropic Usage API, time-bucketed | Feasible once API access is set up |
| Batch vs. real-time API split | Org-wide | Anthropic Usage API, if the Message Batches API is in use | Feasible, only useful once batch usage exists |

No per-model cost breakdown here — every team is required to use Sonnet, so there's no model mix to compare.

Skill-level detail (which skill, how often) isn't in the table above — that's general org-wide usage, and [Anthropic's own enterprise Skills guidance confirms the Skills API itself has no usage analytics](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise#skill-lifecycle-management). But a separate, purpose-built endpoint does cover it — see Next Steps below.

## Next Steps

Anthropic's [Organization Analytics API for Skills](https://platform.claude.com/docs/en/api/http/beta/organization/analytics/skills) (`GET /v1/organizations/analytics/skills`, currently in beta) covers most of what this page needs natively — no custom logging layer required. This replaces the MCP-server-and-SharePoint build previously planned here with a single API integration.

### Immediate next step: evaluate the API

Before building anything, test the endpoint directly against this org's account:

1. Confirm the org is on a Claude Enterprise plan and provision an API key scoped `read:analytics` (an org-admin-level credential).
2. Call the endpoint filtered to a few known catalog skill names over a recent date range, e.g. `filter[]=skill_name:expense-policy-checker` with `starting_date` set 30 days back.
3. Check specifically:
    - Whether `skill_display_name` resolves to the real skill name for our plugin-delivered skills — the docs say it should, since they come from the org's own plugin marketplace, but worth confirming against real data.
    - Whether `invocation_count` and `enable_count` come back populated or null. Both are documented as null "when invocation/enable reporting is not enabled for this organization" — that reads like a separate admin toggle may be required beyond just having API access.
    - Whether `chat`-product rows include Claude Desktop usage. Desktop isn't listed as its own `product` value (only `chat`, `claude_code`, `cowork`, `office_agent`), so this needs to be confirmed rather than assumed, since Desktop is how this org actually uses Claude.

### If it checks out

- **Scope:** filter every query to this catalog's skill names (`filter[]=skill_name:...`), so reporting reflects the published catalog specifically, not every skill in the org.
- **Team-level breakdown:** `group_by[]=rbac_group_id` gives per-team numbers natively, if teams are organized as RBAC groups in the Enterprise admin console. If not, that's the one setup dependency — and it's far lighter than the workspace-per-team requirement in the table above.
- **Pipeline:** a scheduled job — can extend the existing "Docs" GitHub Action — calls the endpoint and writes an aggregated rollup into a small data file in this repo. `generate_repo_summary.py` reads it the same way it already reads the catalog, and the placeholders in the table below become real numbers. No MCP server, no SharePoint, no Power Automate, no logging instructions to inject into skills — and no user-approval question, since no tool call is involved at all.

Per-user data is technically available too (`group_by[]=user_id` / `filter[]=user_id:...`) but stays a separate initiative pending privacy/HR review, same as before — the API supports it whenever that's greenlit, with no additional engineering needed then either.

## Team Breakdown — Planned

The slice that matters most once usage is wired up: every team in the catalog, side by side. Skills Published is real (pulled from the catalog); the rest are placeholders for the Organization Analytics API breakdown, grouped by team (RBAC group, pending confirmation above).

| Team | Skills Published | Requests (30d) | Cost (30d) | Active Users (30d) |
|---|---|---|---|---|
| crm-sync | 0 | — | — | — |
| expense-audit | 2 | — | — | — |
| hr-onboarding | 1 | — | — | — |
| invoice-processor | 2 | — | — | — |
| meeting-ops | 2 | — | — | — |

[:octicons-arrow-left-24: Back to Home](index.md)
