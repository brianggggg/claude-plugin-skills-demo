# Reporting

## Example: Skill Usage

<div class="bar-chart">
<div class="bar-row" title="Brand & Design Assistant — 958 invocations (30d)">
  <span class="bar-label">Brand &amp; Design Assistant</span>
  <span class="bar-track"><span class="bar-fill" style="width: 100.0%;"></span></span>
  <span class="bar-value">958</span>
</div>
<div class="bar-row" title="Employee Onboarding Assistant — 694 invocations (30d)">
  <span class="bar-label">Employee Onboarding Assistant</span>
  <span class="bar-track"><span class="bar-fill" style="width: 72.4%;"></span></span>
  <span class="bar-value">694</span>
</div>
<div class="bar-row" title="Knowledge & FAQ Assistant — 495 invocations (30d)">
  <span class="bar-label">Knowledge &amp; FAQ Assistant</span>
  <span class="bar-track"><span class="bar-fill" style="width: 51.7%;"></span></span>
  <span class="bar-value">495</span>
</div>
<div class="bar-row" title="Document Creator — 401 invocations (30d)">
  <span class="bar-label">Document Creator</span>
  <span class="bar-track"><span class="bar-fill" style="width: 41.9%;"></span></span>
  <span class="bar-value">401</span>
</div>
<div class="bar-row" title="Enterprise Information Assistant — 379 invocations (30d)">
  <span class="bar-label">Enterprise Information Assistant</span>
  <span class="bar-track"><span class="bar-fill" style="width: 39.6%;"></span></span>
  <span class="bar-value">379</span>
</div>
<div class="bar-row" title="Presentation Builder — 358 invocations (30d)">
  <span class="bar-label">Presentation Builder</span>
  <span class="bar-track"><span class="bar-fill" style="width: 37.4%;"></span></span>
  <span class="bar-value">358</span>
</div>
<div class="bar-row" title="Spreadsheet Assistant — 285 invocations (30d)">
  <span class="bar-label">Spreadsheet Assistant</span>
  <span class="bar-track"><span class="bar-fill" style="width: 29.7%;"></span></span>
  <span class="bar-value">285</span>
</div>
<div class="bar-row" title="Issue Intake Assistant — 153 invocations (30d)">
  <span class="bar-label">Issue Intake Assistant</span>
  <span class="bar-track"><span class="bar-fill" style="width: 16.0%;"></span></span>
  <span class="bar-value">153</span>
</div>
<div class="bar-row" title="PDF Analysis Assistant — 99 invocations (30d)">
  <span class="bar-label">PDF Analysis Assistant</span>
  <span class="bar-track"><span class="bar-fill" style="width: 10.3%;"></span></span>
  <span class="bar-value">99</span>
</div>
</div>

*Sample data for illustration — [download the source workbook](assets/reports/skill-usage-example.xlsx){ download } to see the numbers behind it or drop in real ones later.*

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
