#!/usr/bin/env python3
"""Scaffold a new skill and add it to the README.

  python3 scripts/new_skill.py pitch-deck
  python3 scripts/new_skill.py pitch-deck --description "Build a 3-minute pitch. Use when..."
  python3 scripts/new_skill.py judge-prep --user-invoked

Creates skills/<name>/SKILL.md and skills/<name>/agents/openai.yaml, then
updates README.md. What's left is replacing the TODO placeholders with the
skill's content; `python3 scripts/sync.py --check` and install.py refuse the
skill until they're gone.
"""

from __future__ import annotations

import argparse
import sys

from _lib import NAME_RE, REPO, SKILLS_DIR, TODO, load_agents, load_skills, yaml_str
from sync import sync

SKILL_BODY = """\
# {title}

## Mission
{todo}: what this skill helps the user achieve, in two or three sentences.

## Guardrails
- {todo}: rules the agent must never break while running this skill.

## Workflow

### 1. {todo}
{todo}: first step.

### 2. {todo}
{todo}: next step.

## Output
{todo}: what the agent hands back at the end.
"""

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name", help="kebab-case skill name, e.g. pitch-deck")
    parser.add_argument("--description", help="SKILL.md description; model-invoked skills should include 'Use when...'")
    parser.add_argument("--display-name", help="name shown in the Codex skill picker (default: from the name)")
    parser.add_argument("--short-description", help="one short line for the Codex skill picker")
    parser.add_argument(
        "--user-invoked",
        action="store_true",
        help="only reachable when the user types it (sets disable-model-invocation)",
    )
    args = parser.parse_args()

    name = args.name
    if not NAME_RE.match(name):
        parser.error(f"skill name must be kebab-case (lowercase letters, digits, hyphens): {name!r}")
    if any(s.name == name for s in load_skills()):
        parser.error(f"a skill named {name!r} already exists at skills/{name}/")
    if any(a.name == name for a in load_agents()):
        parser.error(f"{name!r} is already an agent name; pick a different skill name")

    title = name.replace("-", " ").title()
    skill_dir = SKILLS_DIR / name
    created = []

    description = args.description or f"{TODO}: what it does, in one sentence. Use when {TODO}."
    frontmatter = [f"name: {name}", f"description: {yaml_str(description)}"]
    if args.user_invoked:
        frontmatter.append("disable-model-invocation: true")
    (skill_dir / "agents").mkdir(parents=True)
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(
        "---\n" + "\n".join(frontmatter) + "\n---\n\n" + SKILL_BODY.format(title=title, todo=TODO),
        encoding="utf-8",
    )
    created.append(skill_md)

    short = args.short_description or f"{TODO}: short picker line"
    openai = [
        "interface:",
        f"  display_name: {yaml_str(args.display_name or title)}",
        f"  short_description: {yaml_str(short)}",
    ]
    if args.user_invoked:
        openai += ["policy:", "  allow_implicit_invocation: false"]
    openai_yaml = skill_dir / "agents" / "openai.yaml"
    openai_yaml.write_text("\n".join(openai) + "\n", encoding="utf-8")
    created.append(openai_yaml)

    stale, _ = sync()

    for p in created:
        print(f"created {p.relative_to(REPO)}")
    if stale:
        print("updated README.md")

    todos = [p.relative_to(REPO) for p in created if TODO in p.read_text(encoding="utf-8")]
    if todos:
        print(f"\nNext: replace the {TODO} placeholders in:")
        for p in todos:
            print(f"  {p}")
        print("then run `python3 scripts/sync.py` to refresh the README line from the description.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
