#!/usr/bin/env python3
"""Regenerates the generated parts of the docs/ site from the repository's
current state. Run by the "Docs" workflow (and Read the Docs) on every
build, so the catalog is always current:

  docs/_generated/stats.md   one-line stat snippet, included into the
                              hand-written docs/index.md via pymdownx.snippets
  docs/plugins/index.md      "Teams" catalog — a closed accordion, one entry
                              per team (technically a "plugin"), expanding to
                              that team's published skills. Skills not
                              published by any team get a final "Unassigned
                              Skills" entry so nothing is orphaned.
  docs/activity.md           "Reporting" — planned usage metrics and feasibility notes

There are deliberately no standalone Skills catalog, per-skill pages, or
per-team pages — everything about a team lives entirely in its own
accordion entry, so there's nothing left to duplicate by clicking
through to a separate page. Skills also never show their raw SKILL.md
contents, which is considered too detailed for new users. Commands
are tracked (see load_plugins) but deliberately not displayed anywhere
— they didn't add enough over the skill descriptions to earn the space.

docs/index.md and docs/guides/*.md are hand-written and never touched here.
"""
import json
import os
import re
import shutil
from collections import defaultdict
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
GENERATED_DIR = os.path.join(DOCS_DIR, "_generated")
PLUGINS_OUT_DIR = os.path.join(DOCS_DIR, "plugins")
SKILLS_OUT_DIR = os.path.join(DOCS_DIR, "skills")
PLUGINS_DIR = os.path.join(REPO_ROOT, "plugins")
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def parse_frontmatter(text):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    fields = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields, match.group(2).strip()


def load_plugins():
    plugins = []
    if not os.path.isdir(PLUGINS_DIR):
        return plugins
    for name in sorted(os.listdir(PLUGINS_DIR)):
        manifest_path = os.path.join(PLUGINS_DIR, name, ".claude-plugin", "plugin.json")
        if not os.path.isfile(manifest_path):
            continue
        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)

        commands_dir = os.path.join(PLUGINS_DIR, name, "commands")
        commands = []
        if os.path.isdir(commands_dir):
            for cmd_file in sorted(os.listdir(commands_dir)):
                if not cmd_file.endswith(".md"):
                    continue
                with open(os.path.join(commands_dir, cmd_file), encoding="utf-8") as f:
                    fm, _ = parse_frontmatter(f.read())
                commands.append(
                    {
                        "name": "/" + cmd_file[: -len(".md")],
                        "description": fm.get("description", ""),
                    }
                )

        skills_manifest = os.path.join(PLUGINS_DIR, name, "skills.json")
        bundled_skills = []
        if os.path.isfile(skills_manifest):
            with open(skills_manifest, encoding="utf-8") as f:
                bundled_skills = json.load(f)

        plugins.append(
            {
                "name": manifest.get("name", name),
                "description": manifest.get("description", ""),
                "version": manifest.get("version", ""),
                "author": manifest.get("author", {}).get("name", ""),
                "commands": commands,
                "skills": bundled_skills,
            }
        )
    return plugins


def load_skills():
    skills = []
    if not os.path.isdir(SKILLS_DIR):
        return skills
    for name in sorted(os.listdir(SKILLS_DIR)):
        skill_path = os.path.join(SKILLS_DIR, name, "SKILL.md")
        if not os.path.isfile(skill_path):
            continue
        with open(skill_path, encoding="utf-8") as f:
            fm, body = parse_frontmatter(f.read())
        skills.append(
            {
                "name": fm.get("name", name),
                "description": fm.get("description", ""),
                "body": body,
            }
        )
    return skills


def indent(text, prefix="    "):
    """Indent every non-empty line of text — for nesting pymdownx.details
    (accordion) blocks, where each nesting level needs 4 more spaces."""
    return "\n".join((prefix + line if line else "") for line in text.splitlines())


def build_skill_accordion_item(skill, note):
    # Deliberately no raw SKILL.md contents here — that level of detail
    # isn't meant for new users. Name + description + who publishes it.
    lines = [f'??? example "{skill["name"]}"', ""]
    body = [skill["description"]]
    if note:
        body += ["", note]
    lines.append(indent("\n".join(body)))
    return "\n".join(lines)


def build_stats_snippet(plugins, skills):
    # Raw HTML <a> tags bypass MkDocs' markdown link resolution, so these
    # must already be the served paths (with use_directory_urls: true),
    # not the source .md filenames. No "last updated" line here — this
    # snippet is embedded in the compact homepage column; the date lives
    # on the Teams page itself instead.
    return (
        f'<div class="stat-strip reveal">\n'
        f'  <a class="stat" href="plugins/"><span class="stat-number" data-target="{len(plugins)}">0</span>'
        f'<span class="stat-label">Teams</span></a>\n'
        f'  <a class="stat" href="plugins/"><span class="stat-number" data-target="{len(skills)}">0</span>'
        f'<span class="stat-label">Skills</span></a>\n'
        f"</div>\n"
    )


def build_plugins_index(plugins, skills_by_name, skill_to_plugins, friendly_date):
    team_count = len(plugins)
    lines = [
        "# CitDev Inventory",
        "",
        f"{team_count} team{'s' if team_count != 1 else ''} {'have' if team_count != 1 else 'has'} "
        "published skills here. Click a team to see what they've shared.",
        "",
        f"*Last updated {friendly_date}.*",
        "",
    ]

    for plugin in plugins:
        skill_count = len(plugin["skills"])
        skill_note = f"{skill_count} skill{'s' if skill_count != 1 else ''}" if skill_count else "no skills yet"
        summary = f"{plugin['name']} — v{plugin['version']} · {skill_note}"
        lines.append(f'??? note "{summary}"')
        lines.append("")

        body = [plugin["description"], ""]

        if plugin["skills"]:
            for skill_name in plugin["skills"]:
                skill = skills_by_name.get(skill_name)
                if not skill:
                    continue
                other = [p for p in skill_to_plugins.get(skill_name, []) if p != plugin["name"]]
                note = f"Also on: {', '.join(other)}" if other else ""
                body.append(build_skill_accordion_item(skill, note))
                body.append("")
        else:
            body.append("No skills published yet.")
            body.append("")

        lines.append(indent("\n".join(body)))
        lines.append("")

    unassigned = [s for s in skills_by_name.values() if not skill_to_plugins.get(s["name"])]
    if unassigned:
        count = len(unassigned)
        lines.append(f'??? note "Unassigned Skills — {count} skill{"s" if count != 1 else ""}"')
        lines.append("")
        body = ["Not yet published under any team."]
        body.append("")
        for skill in unassigned:
            body.append(build_skill_accordion_item(skill, note=""))
            body.append("")
        lines.append(indent("\n".join(body)))
        lines.append("")

    return "\n".join(lines)


def build_activity_page(plugins):
    lines = ["# Reporting", ""]
    lines.append(
        "Placeholder — pulled from Anthropic's Usage & Cost API once each team is set up "
        "as its own workspace, plus a logging layer for skill-level detail."
    )
    lines.append("")

    lines.append("## Usage Metrics — Planned")
    lines.append("")
    lines.append(
        "Team and org-wide adoption metrics aren't wired up yet. Here's the full set of "
        "what's worth pulling once they are, roughly in order of how feasible each one is "
        "to actually get:"
    )
    lines.append("")
    lines.append("| Metric | Level | Source | Status |")
    lines.append("|---|---|---|---|")
    lines.append(
        "| Requests, tokens, spend | Org-wide | Anthropic Usage & Cost Admin API "
        "| Feasible once API access is set up |"
    )
    lines.append(
        "| Requests by team | Team (workspace) | Anthropic Usage & Cost Admin API, "
        "if each team has its own workspace | Feasible, needs workspace-per-team setup |"
    )
    lines.append(
        "| Token mix (input / output / cache read+write) | Org-wide | Anthropic Usage API "
        "| Feasible once API access is set up |"
    )
    lines.append(
        "| Cost by model (Opus / Sonnet / Haiku mix) | Org-wide | Anthropic Cost Admin API "
        "| Feasible once API access is set up |"
    )
    lines.append(
        "| Prompt cache hit rate & savings | Org-wide | Anthropic Usage API "
        "(cache_read_input_tokens vs. total) | Feasible once API access is set up |"
    )
    lines.append(
        "| Average tokens per request | Org-wide or team | Derived from requests + tokens "
        "totals, no new data needed | Feasible once API access is set up |"
    )
    lines.append(
        "| Request volume trend (daily / weekly) | Org-wide or team | Anthropic Usage API, "
        "time-bucketed | Feasible once API access is set up |"
    )
    lines.append(
        "| Model version / mix adoption | Org-wide or team | Anthropic Usage API, broken "
        "out by model | Feasible — flags teams still on older models |"
    )
    lines.append(
        "| Batch vs. real-time API split | Org-wide | Anthropic Usage API, if the Message "
        "Batches API is in use | Feasible, only useful once batch usage exists |"
    )
    lines.append(
        "| Individual usage stats | Person | Custom authenticated proxy in front of Claude "
        "| Under evaluation — see note below |"
    )
    lines.append("")
    lines.append(
        "Skill-level detail (which skill, how often) isn't in this table — Anthropic's API "
        "has no concept of \"skills,\" so that needs its own logging layer regardless of "
        "level. See the homepage's Top Skills preview for where that will surface once it "
        "exists."
    )
    lines.append("")
    lines.append("### A note on individual usage stats")
    lines.append("")
    lines.append(
        "Storing usage events for 40k people isn't a scale problem — any normal database "
        "handles that volume easily. The real constraints are:"
    )
    lines.append("")
    lines.append(
        "- **Anthropic's own reporting is by API key and workspace, not by named "
        "individual.** Attributing a request to a specific person needs our own layer in "
        "front of Claude (an authenticated gateway or proxy) that tags and logs each "
        "request — that's a real build, not a reporting toggle."
    )
    lines.append(
        "- **Privacy and HR review.** Individual-level usage dashboards read like "
        "productivity monitoring and typically need legal/HR sign-off before they're shown "
        "broadly, especially at a regulated company."
    )
    lines.append("")
    lines.append(
        "Recommendation: start with team-level aggregates (lower lift, no privacy review "
        "needed) and treat named-individual stats as a separate initiative pending its own "
        "approval."
    )
    lines.append("")

    lines.append("## Team Breakdown — Planned")
    lines.append("")
    lines.append(
        "The slice that matters most once usage is wired up: every team in the catalog, "
        "side by side. Skills Published is real (pulled from the catalog); the rest are "
        "placeholders for the same Usage & Cost API breakdown, per team workspace."
    )
    lines.append("")
    lines.append("| Team | Skills Published | Requests (30d) | Cost (30d) | Active Users (30d) |")
    lines.append("|---|---|---|---|---|")
    for plugin in plugins:
        lines.append(f"| {plugin['name']} | {len(plugin['skills'])} | — | — | — |")
    lines.append("")

    lines.append("[:octicons-arrow-left-24: Back to Home](index.md)")
    lines.append("")
    return "\n".join(lines)


def main():
    # No standalone Skills output dir — skills only ever appear nested
    # inside the Teams accordion.
    if os.path.isdir(SKILLS_OUT_DIR):
        shutil.rmtree(SKILLS_OUT_DIR)

    for path in (PLUGINS_OUT_DIR, GENERATED_DIR):
        if os.path.isdir(path):
            shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)

    plugins = load_plugins()
    skills = load_skills()
    skills_by_name = {s["name"]: s for s in skills}

    skill_to_plugins = defaultdict(list)
    for plugin in plugins:
        for skill_name in plugin["skills"]:
            skill_to_plugins[skill_name].append(plugin["name"])

    friendly_date = datetime.now(timezone.utc).strftime("%B %-d, %Y")

    with open(os.path.join(GENERATED_DIR, "stats.md"), "w", encoding="utf-8") as f:
        f.write(build_stats_snippet(plugins, skills))

    with open(os.path.join(PLUGINS_OUT_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write(build_plugins_index(plugins, skills_by_name, skill_to_plugins, friendly_date))

    with open(os.path.join(DOCS_DIR, "activity.md"), "w", encoding="utf-8") as f:
        f.write(build_activity_page(plugins))

    print(
        f"Wrote stats snippet and plugins/index.md ({len(plugins)} teams, "
        f"{len(skills)} skills in the accordion), and activity.md"
    )


if __name__ == "__main__":
    main()
