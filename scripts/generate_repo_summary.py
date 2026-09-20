#!/usr/bin/env python3
"""Regenerates docs/index.md from the current state of the repository.

Run by the "Docs" GitHub Actions workflow on every push so the MkDocs
site always reflects the current plugins, skills, and commits.
"""
import json
import os
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
OUTPUT_PATH = os.path.join(DOCS_DIR, "index.md")
PLUGINS_DIR = os.path.join(REPO_ROOT, "plugins")
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


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
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


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
                    fm = parse_frontmatter(f.read())
                commands.append(
                    {
                        "name": "/" + cmd_file[: -len(".md")],
                        "description": fm.get("description", ""),
                    }
                )
        plugins.append(
            {
                "name": manifest.get("name", name),
                "description": manifest.get("description", ""),
                "version": manifest.get("version", ""),
                "author": manifest.get("author", {}).get("name", ""),
                "commands": commands,
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
            fm = parse_frontmatter(f.read())
        skills.append(
            {
                "name": fm.get("name", name),
                "description": fm.get("description", ""),
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


def get_current_branch():
    return run_git(["rev-parse", "--abbrev-ref", "HEAD"])


def build_markdown():
    plugins = load_plugins()
    skills = load_skills()
    commits = get_recent_commits()
    contributors = get_contributors()
    total_commits = get_total_commit_count()
    branch = get_current_branch()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    lines.append("# Business Ops Plugin & Skills Catalog")
    lines.append("")
    lines.append(
        f"*This page is generated automatically from the repository's current state. "
        f"Last updated: **{now}** (branch `{branch}`).*"
    )
    lines.append("")

    lines.append("## Overview")
    lines.append("")
    lines.append(f"- **Plugins:** {len(plugins)}")
    lines.append(f"- **Skills:** {len(skills)}")
    lines.append(f"- **Total commits:** {total_commits}")
    lines.append(f"- **Contributors:** {len(contributors)}")
    lines.append("")

    lines.append("## Plugins")
    lines.append("")
    for plugin in plugins:
        lines.append(f"### `{plugin['name']}` (v{plugin['version']})")
        lines.append("")
        lines.append(plugin["description"])
        lines.append("")
        if plugin["commands"]:
            lines.append("| Command | Description |")
            lines.append("|---|---|")
            for cmd in plugin["commands"]:
                lines.append(f"| `{cmd['name']}` | {cmd['description']} |")
            lines.append("")

    lines.append("## Skills")
    lines.append("")
    lines.append("| Skill | Description |")
    lines.append("|---|---|")
    for skill in skills:
        lines.append(f"| `{skill['name']}` | {skill['description']} |")
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

    return "\n".join(lines) + "\n"


def main():
    os.makedirs(DOCS_DIR, exist_ok=True)
    markdown = build_markdown()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
