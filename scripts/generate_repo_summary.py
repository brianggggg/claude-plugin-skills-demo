#!/usr/bin/env python3
"""Regenerates the docs/ site from the current state of the repository.

Run by the "Docs" GitHub Actions workflow on every push, so the MkDocs
site always reflects the current plugins, skills, and commits:

  docs/index.md          overview + plugin/skill card grids
  docs/plugins/<name>.md one page per plugin, with its bundled skills
  docs/skills/<name>.md  one page per skill, with the plugins that use it
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
PLUGINS_OUT_DIR = os.path.join(DOCS_DIR, "plugins")
SKILLS_OUT_DIR = os.path.join(DOCS_DIR, "skills")
PLUGINS_DIR = os.path.join(REPO_ROOT, "plugins")
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)

PLUGIN_ICONS = [
    "material-puzzle-outline",
    "material-connection",
    "material-calendar-check-outline",
    "material-account-plus-outline",
    "material-receipt-text-check-outline",
]
SKILL_ICON = "material-flash-outline"


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


def get_current_branch():
    return run_git(["rev-parse", "--abbrev-ref", "HEAD"])


def plugin_card(plugin, icon, link_prefix=""):
    skill_count = len(plugin["skills"])
    skill_note = f"{skill_count} skill{'s' if skill_count != 1 else ''}" if skill_count else "no bundled skills"
    return (
        f"-   :{icon}:{{ .lg .middle }} __{plugin['name']}__ `v{plugin['version']}`\n\n"
        f"    ---\n\n"
        f"    {plugin['description']}\n\n"
        f"    {len(plugin['commands'])} commands · {skill_note}\n\n"
        f"    [:octicons-arrow-right-24: View plugin]({link_prefix}plugins/{plugin['name']}.md)\n"
    )


def skill_card(skill, used_by, link_prefix="", note_override=None):
    if note_override is not None:
        used_note = note_override
    else:
        used_note = f"Used by: {', '.join(used_by)}" if used_by else "Standalone — not bundled by a plugin"
    return (
        f"-   :{SKILL_ICON}:{{ .lg .middle }} __{skill['name']}__\n\n"
        f"    ---\n\n"
        f"    {skill['description']}\n\n"
        f"    {used_note}\n\n"
        f"    [:octicons-arrow-right-24: View skill]({link_prefix}skills/{skill['name']}.md)\n"
    )


def build_index(plugins, skills, skill_to_plugins, commits, contributors, total_commits, branch, now):
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
    lines.append('<div class="grid cards" markdown>')
    lines.append("")
    for plugin, icon in zip(plugins, PLUGIN_ICONS):
        lines.append(plugin_card(plugin, icon))
        lines.append("")
    lines.append("</div>")
    lines.append("")

    lines.append("## Skills")
    lines.append("")
    lines.append('<div class="grid cards" markdown>')
    lines.append("")
    for skill in skills:
        lines.append(skill_card(skill, skill_to_plugins.get(skill["name"], [])))
        lines.append("")
    lines.append("</div>")
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


def build_plugin_page(plugin, skills_by_name, skill_to_plugins):
    lines = []
    lines.append(f"# {plugin['name']}")
    lines.append("")
    author_bit = f" · {plugin['author']}" if plugin["author"] else ""
    lines.append(f"*Plugin · v{plugin['version']}{author_bit}*")
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

    lines.append("## Bundled skills")
    lines.append("")
    if plugin["skills"]:
        lines.append('<div class="grid cards" markdown>')
        lines.append("")
        for skill_name in plugin["skills"]:
            skill = skills_by_name.get(skill_name)
            if not skill:
                continue
            other_plugins = [p for p in skill_to_plugins.get(skill_name, []) if p != plugin["name"]]
            note = f"Also used by: {', '.join(other_plugins)}" if other_plugins else "Bundled by this plugin"
            lines.append(skill_card(skill, [], link_prefix="../", note_override=note))
            lines.append("")
        lines.append("</div>")
        lines.append("")
    else:
        lines.append("This plugin doesn't bundle any skills — its commands are self-contained.")
        lines.append("")

    lines.append("[:octicons-arrow-left-24: Back to catalog](../index.md)")
    lines.append("")
    return "\n".join(lines)


def build_skill_page(skill, used_by):
    lines = []
    lines.append(f"# {skill['name']}")
    lines.append("")
    lines.append("*Skill*")
    lines.append("")
    lines.append(skill["description"])
    lines.append("")

    lines.append("## Used by")
    lines.append("")
    if used_by:
        for plugin_name in used_by:
            lines.append(f"- [{plugin_name}](../plugins/{plugin_name}.md)")
    else:
        lines.append("Not currently bundled by any plugin — available standalone.")
    lines.append("")

    lines.append("## Full skill definition")
    lines.append("")
    lines.append("??? note \"SKILL.md contents\"")
    lines.append("")
    lines.append("    ```markdown")
    for line in skill["body"].splitlines():
        lines.append(f"    {line}" if line else "")
    lines.append("    ```")
    lines.append("")

    lines.append("[:octicons-arrow-left-24: Back to catalog](../index.md)")
    lines.append("")
    return "\n".join(lines)


def main():
    if os.path.isdir(PLUGINS_OUT_DIR):
        shutil.rmtree(PLUGINS_OUT_DIR)
    if os.path.isdir(SKILLS_OUT_DIR):
        shutil.rmtree(SKILLS_OUT_DIR)
    os.makedirs(PLUGINS_OUT_DIR, exist_ok=True)
    os.makedirs(SKILLS_OUT_DIR, exist_ok=True)

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
    branch = get_current_branch()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    with open(os.path.join(DOCS_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write(
            build_index(
                plugins, skills, skill_to_plugins, commits, contributors, total_commits, branch, now
            )
        )

    for plugin in plugins:
        path = os.path.join(PLUGINS_OUT_DIR, f"{plugin['name']}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(build_plugin_page(plugin, skills_by_name, skill_to_plugins))

    for skill in skills:
        path = os.path.join(SKILLS_OUT_DIR, f"{skill['name']}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(build_skill_page(skill, skill_to_plugins.get(skill["name"], [])))

    print(f"Wrote docs/index.md, {len(plugins)} plugin pages, {len(skills)} skill pages")


if __name__ == "__main__":
    main()
