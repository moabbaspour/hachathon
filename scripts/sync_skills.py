#!/usr/bin/env python3
"""Regenerate every list of skills from the SKILL.md files themselves.

Updates:
  - .claude-plugin/plugin.json `skills` (promoted buckets only)
  - skills/<bucket>/README.md, between the skills markers
  - README.md, between the skills markers

Existing order in plugin.json is kept; new skills are appended, removed ones
dropped. README lists follow the same order.

  python3 scripts/sync_skills.py          # write changes
  python3 scripts/sync_skills.py --check  # change nothing, exit 1 if out of sync or invalid
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _lib import (
    END_MARKER,
    NAME_RE,
    PLUGIN_JSON,
    README,
    REPO,
    SKILLS_DIR,
    START_MARKER,
    TODO,
    Skill,
    bucket_title,
    buckets,
    is_promoted,
    load_skills,
    read_json,
)

USER_INVOKED_NOTE = (
    "Reachable only when you type them (Claude Code: `disable-model-invocation: true`; "
    "Codex: `policy.allow_implicit_invocation: false` in `agents/openai.yaml`)."
)
MODEL_INVOKED_NOTE = "Model- or user-reachable (rich trigger phrasing so the model can reach for them)."


def validate(skills: list[Skill]) -> list[str]:
    errors = []
    seen: dict[str, str] = {}
    for s in skills:
        where = s.path.relative_to(REPO).as_posix()
        if s.name in seen:
            errors.append(f"{where}: skill name also used in {seen[s.name]}")
        seen[s.name] = where
        if not NAME_RE.match(s.name):
            errors.append(f"{where}: folder name must be kebab-case")
        if s.frontmatter.get("name") != s.name:
            errors.append(f"{where}: frontmatter name must be {s.name!r}")
        if not s.description:
            errors.append(f"{where}: missing description")
        if TODO in s.path.read_text(encoding="utf-8"):
            errors.append(f"{where}: still contains {TODO} placeholders")
        openai = s.path.parent / "agents" / "openai.yaml"
        if not openai.exists():
            errors.append(f"{where}: missing agents/openai.yaml")
        else:
            text = openai.read_text(encoding="utf-8")
            if TODO in text:
                errors.append(f"{openai.relative_to(REPO)}: still contains {TODO}")
            implicit_off = "allow_implicit_invocation: false" in text
            if implicit_off != s.user_invoked:
                errors.append(
                    f"{where}: disable-model-invocation and "
                    "policy.allow_implicit_invocation in agents/openai.yaml disagree"
                )
    return errors


def ordered(skills: list[Skill], plugin: dict) -> list[Skill]:
    by_dir = {f"./{s.rel_dir}": s for s in skills}
    order = [p for p in plugin.get("skills", []) if p in by_dir]
    order += sorted(p for p in by_dir if p not in order)
    return [by_dir[p] for p in order]


def entry(s: Skill, link: str) -> str:
    return f"- **[{s.name}]({link})**: {s.summary}"


def bucket_block(bucket: str, skills: list[Skill]) -> str:
    def lst(items: list[Skill]) -> str:
        return "\n".join(entry(s, f"./{s.name}/SKILL.md") for s in items) or "_None yet._"

    if not is_promoted(bucket):
        return lst(skills)
    user = [s for s in skills if s.user_invoked]
    model = [s for s in skills if not s.user_invoked]
    return (
        f"## User-invoked\n\n{USER_INVOKED_NOTE}\n\n{lst(user)}\n\n"
        f"## Model-invoked\n\n{MODEL_INVOKED_NOTE}\n\n{lst(model)}"
    )


def readme_block(skills: list[Skill]) -> str:
    parts = []
    for bucket in dict.fromkeys(s.bucket for s in skills):
        parts.append(f"### {bucket_title(bucket)}")
        for title, invoked in (("User-invoked", True), ("Model-invoked", False)):
            items = [s for s in skills if s.bucket == bucket and s.user_invoked == invoked]
            if items:
                lines = "\n".join(entry(s, f"./{s.rel_dir}/SKILL.md") for s in items)
                parts.append(f"#### {title}\n\n{lines}")
    return "\n\n".join(parts) or "_No skills yet._"


def replace_block(path: Path, block: str) -> str:
    text = path.read_text(encoding="utf-8")
    start, end = text.find(START_MARKER), text.find(END_MARKER)
    if start == -1 or end < start:
        raise SystemExit(f"error: {path.relative_to(REPO)} needs {START_MARKER} and {END_MARKER}")
    return text[: start + len(START_MARKER)] + "\n\n" + block + "\n\n" + text[end:]


def plugin_text(plugin: dict, skills: list[Skill]) -> str:
    plugin = dict(plugin, skills=[f"./{s.rel_dir}" for s in skills if is_promoted(s.bucket)])
    return json.dumps(plugin, indent=2, ensure_ascii=False) + "\n"


def sync(check: bool = False) -> tuple[list[Path], list[str]]:
    """Bring every list in line with the SKILL.md files. Returns (changed or stale files, errors)."""
    plugin = read_json(PLUGIN_JSON)
    skills = ordered(load_skills(), plugin)
    errors = validate(skills)

    targets: dict[Path, str] = {PLUGIN_JSON: plugin_text(plugin, skills)}
    for bucket in buckets():
        readme = SKILLS_DIR / bucket / "README.md"
        if readme.exists():
            if TODO in readme.read_text(encoding="utf-8").split(START_MARKER)[0]:
                errors.append(f"{readme.relative_to(REPO)}: still contains {TODO}")
            targets[readme] = replace_block(readme, bucket_block(bucket, [s for s in skills if s.bucket == bucket]))
        else:
            errors.append(f"{readme.relative_to(REPO)}: missing")
    targets[README] = replace_block(README, readme_block([s for s in skills if is_promoted(s.bucket)]))

    stale = [p for p, text in targets.items() if p.read_text(encoding="utf-8") != text]
    if check:
        errors += [f"{p.relative_to(REPO)}: out of sync, run `python3 scripts/sync_skills.py`" for p in stale]
    else:
        for p in stale:
            p.write_text(targets[p], encoding="utf-8")
    return stale, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="change nothing; exit 1 if anything is out of sync")
    args = parser.parse_args()

    stale, errors = sync(check=args.check)
    if not args.check:
        for p in stale:
            print(f"updated {p.relative_to(REPO)}")
        if not stale:
            print("already in sync")
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
