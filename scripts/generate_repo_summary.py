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
  docs/plugins/<name>.md     one full page per team, with its bundled skills
  docs/activity.md           recent commits + contributors

There is deliberately no standalone Skills catalog or per-skill page —
skills are only ever shown nested inside a team's accordion (or the
"Unassigned Skills" entry), and never show their raw SKILL.md contents,
which is considered too detailed for new users.

docs/index.md and docs/guides/*.md are hand-written and never touched here.
"""
import json
import os
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
GENERATED_DIR = os.path.join(DOCS_DIR, "_generated")
PLUGINS_OUT_DIR = os.path.join(DOCS_DIR, "plugins")
SKILLS_OUT_DIR = os.path.join(DOCS_DIR, "skills")
PLUGINS_DIR = os.path.join(REPO_ROOT, "plugins")
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)

def run_git(args):
    result = subprocess.run(
        ["git", "-C", REPO_ROOT, *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


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


def get_recent_commits(limit=10):
    log = run_git(["log", f"-{limit}", "--pretty=format:%h|%an|%ad|%s", "--date=short"])
    commits = []
    for line in log.splitlines():
        parts = line.split("|", 3)
        if len(parts) == 4:
            commits.append(parts)
    return commits


def get_contributors():
    log = run_git(["log", "--pretty=format:%an"])
    return Counter(name for name in log.splitlines() if name).most_common()


def get_total_commit_count():
    return run_git(["rev-list", "--count", "HEAD"])


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


def build_stats_snippet(plugins, skills, friendly_date):
    # Raw HTML <a> tags bypass MkDocs' markdown link resolution, so these
    # must already be the served paths (with use_directory_urls: true),
    # not the source .md filenames.
    return (
        f'<div class="stat-strip reveal">\n'
        f'  <a class="stat" href="plugins/"><span class="stat-number" data-target="{len(plugins)}">0</span>'
        f'<span class="stat-label">Teams</span></a>\n'
        f'  <a class="stat" href="plugins/"><span class="stat-number" data-target="{len(skills)}">0</span>'
        f'<span class="stat-label">Skills</span></a>\n'
        f"</div>\n"
        f'<p class="stat-updated">Last updated <strong>{friendly_date}</strong></p>\n'
    )


def build_plugins_index(plugins, skills_by_name, skill_to_plugins):
    team_count = len(plugins)
    lines = [
        "# Teams",
        "",
        f"{team_count} team{'s' if team_count != 1 else ''} {'have' if team_count != 1 else 'has'} "
        "published skills here. Click a team to see what they've shared.",
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

        if plugin["commands"]:
            body.append("**Commands**")
            body.append("")
            body.append("| Command | Description |")
            body.append("|---|---|")
            for cmd in plugin["commands"]:
                body.append(f"| `{cmd['name']}` | {cmd['description']} |")
            body.append("")

        body.append(f"[Full team page →]({plugin['name']}.md)")

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


def build_plugin_page(plugin, skills_by_name, skill_to_plugins):
    lines = []
    lines.append(f"# {plugin['name']}")
    lines.append("")
    author_bit = f" · {plugin['author']}" if plugin["author"] else ""
    lines.append(f"*Team · v{plugin['version']}{author_bit}*")
    lines.append("")
    lines.append(plugin["description"])
    lines.append("")

    if plugin["commands"]:
        lines.append("## Commands")
        lines.append("")
        lines.append("| Command | Description |")
        lines.append("|---|---|")
        for cmd in plugin["commands"]:
            lines.append(f"| `{cmd['name']}` | {cmd['description']} |")
        lines.append("")

    lines.append("## Skills")
    lines.append("")
    if plugin["skills"]:
        for skill_name in plugin["skills"]:
            skill = skills_by_name.get(skill_name)
            if not skill:
                continue
            other_plugins = [p for p in skill_to_plugins.get(skill_name, []) if p != plugin["name"]]
            note = f"Also on: {', '.join(other_plugins)}" if other_plugins else ""
            lines.append(build_skill_accordion_item(skill, note))
            lines.append("")
    else:
        lines.append("This team hasn't published any skills yet.")
        lines.append("")

    lines.append("[:octicons-arrow-left-24: Back to Teams catalog](index.md)")
    lines.append("")
    return "\n".join(lines)


def build_activity_page(commits, contributors, total_commits):
    lines = ["# Repository Activity", ""]
    lines.append(f"**Total commits:** {total_commits} · **Contributors:** {len(contributors)}")
    lines.append("")

    lines.append("## Recent Commits")
    lines.append("")
    lines.append("| Commit | Author | Date | Message |")
    lines.append("|---|---|---|---|")
    for sha, author, date, message in commits:
        message = message.replace("|", "\\|")
        lines.append(f"| `{sha}` | {author} | {date} | {message} |")
    lines.append("")

    if contributors:
        lines.append("## Contributors")
        lines.append("")
        lines.append("| Name | Commits |")
        lines.append("|---|---|")
        for name, count in contributors:
            lines.append(f"| {name} | {count} |")
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

    commits = get_recent_commits()
    contributors = get_contributors()
    total_commits = get_total_commit_count()
    friendly_date = datetime.now(timezone.utc).strftime("%B %-d, %Y")

    with open(os.path.join(GENERATED_DIR, "stats.md"), "w", encoding="utf-8") as f:
        f.write(build_stats_snippet(plugins, skills, friendly_date))

    with open(os.path.join(PLUGINS_OUT_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write(build_plugins_index(plugins, skills_by_name, skill_to_plugins))

    for plugin in plugins:
        path = os.path.join(PLUGINS_OUT_DIR, f"{plugin['name']}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(build_plugin_page(plugin, skills_by_name, skill_to_plugins))

    with open(os.path.join(DOCS_DIR, "activity.md"), "w", encoding="utf-8") as f:
        f.write(build_activity_page(commits, contributors, total_commits))

    print(
        f"Wrote stats snippet and plugins/index.md ({len(plugins)} teams, "
        f"{len(skills)} skills in the accordion), and activity.md"
    )


if __name__ == "__main__":
    main()
