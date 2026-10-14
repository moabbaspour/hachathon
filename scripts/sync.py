#!/usr/bin/env python3
"""Validate every skill and agent, and regenerate the lists in README.md.

The lists live between the skills and agents markers in README.md.

  python3 scripts/sync.py          # write changes
  python3 scripts/sync.py --check  # change nothing, exit 1 if out of sync or invalid
"""

from __future__ import annotations

import argparse
import sys

from _lib import (
    AGENTS_END_MARKER,
    AGENTS_START_MARKER,
    ISOLATION_HEADING,
    NAME_RE,
    README,
    SKILLS_END_MARKER,
    SKILLS_START_MARKER,
    TODO,
    Agent,
    Skill,
    first_sentence,
    load_agents,
    load_skills,
    rel,
)


def validate_skills(skills: list[Skill]) -> list[str]:
    errors = []
    for s in skills:
        where = rel(s.path)
        if not NAME_RE.match(s.name):
            errors.append(f"{where}: folder name must be kebab-case")
        if s.frontmatter.get("name") != s.name:
            errors.append(f"{where}: frontmatter name must be {s.name!r}")
        if not s.description:
            errors.append(f"{where}: missing description")
        if TODO in s.path.read_text(encoding="utf-8"):
            errors.append(f"{where}: still contains {TODO} placeholders")
        openai = s.dir / "agents" / "openai.yaml"
        if not openai.exists():
            errors.append(f"{where}: missing agents/openai.yaml")
            continue
        text = openai.read_text(encoding="utf-8")
        if TODO in text:
            errors.append(f"{rel(openai)}: still contains {TODO}")
        if ("allow_implicit_invocation: false" in text) != s.user_invoked:
            errors.append(
                f"{where}: disable-model-invocation and policy.allow_implicit_invocation in agents/openai.yaml disagree"
            )
    return errors


def validate_agents(agents: list[Agent], skills: list[Skill]) -> list[str]:
    errors = []
    by_name = {s.name: s for s in skills}
    for a in agents:
        where = rel(a.path)
        if not NAME_RE.match(a.name):
            errors.append(f"{where}: folder name must be kebab-case")
        if a.frontmatter.get("name") != a.name:
            errors.append(f"{where}: frontmatter name must be {a.name!r}")
        if a.name in by_name:
            errors.append(f"{where}: agent name clashes with the skill {a.name!r}")
        if not a.description:
            errors.append(f"{where}: missing description")
        if not a.skills:
            errors.append(f"{where}: `skills` must list at least one skill")
        for name in a.skills:
            if name not in by_name:
                errors.append(f"{where}: unknown skill {name!r}")
            elif by_name[name].user_invoked:
                errors.append(f"{where}: skill {name!r} is user-invoked, so an agent can't load it")
        if ISOLATION_HEADING not in a.body:
            errors.append(f"{where}: body needs a {ISOLATION_HEADING!r} section")
        if "'''" in a.body:
            errors.append(f"{where}: body can't contain ''' (it breaks the Codex TOML)")
        if TODO in a.path.read_text(encoding="utf-8"):
            errors.append(f"{where}: still contains {TODO} placeholders")
    return errors


def skills_block(skills: list[Skill]) -> str:
    parts = []
    for title, invoked in (("User-invoked", True), ("Model-invoked", False)):
        items = [s for s in skills if s.user_invoked == invoked]
        if items:
            lines = "\n".join(f"- **[{s.name}](./{rel(s.path)})**: {first_sentence(s.description)}" for s in items)
            parts.append(f"### {title}\n\n{lines}")
    return "\n\n".join(parts) or "_No skills yet._"


def agents_block(agents: list[Agent]) -> str:
    lines = []
    for a in agents:
        skills = ", ".join(f"`{s}`" for s in a.skills)
        lines.append(f"- **[{a.name}](./{rel(a.path)})**: {first_sentence(a.description)} Skills: {skills}.")
    return "\n".join(lines) or "_No agents yet._"


def replace_block(text: str, block: str, start_marker: str, end_marker: str) -> str:
    start, end = text.find(start_marker), text.find(end_marker)
    if start == -1 or end < start:
        raise SystemExit(f"error: README.md needs {start_marker} and {end_marker}")
    return text[: start + len(start_marker)] + "\n\n" + block + "\n\n" + text[end:]


def sync(check: bool = False) -> tuple[bool, list[str]]:
    """Validate, and bring README.md in line. Returns (README was stale, errors)."""
    skills, agents = load_skills(), load_agents()
    errors = validate_skills(skills) + validate_agents(agents, skills)

    current = README.read_text(encoding="utf-8")
    text = replace_block(current, skills_block(skills), SKILLS_START_MARKER, SKILLS_END_MARKER)
    text = replace_block(text, agents_block(agents), AGENTS_START_MARKER, AGENTS_END_MARKER)
    stale = text != current
    if stale and check:
        errors.append("README.md: out of sync, run `python3 scripts/sync.py`")
    elif stale:
        README.write_text(text, encoding="utf-8")
    return stale, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="change nothing; exit 1 if anything is out of sync")
    args = parser.parse_args()

    stale, errors = sync(check=args.check)
    if not args.check:
        print("updated README.md" if stale else "already in sync")
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
