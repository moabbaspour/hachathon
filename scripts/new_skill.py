#!/usr/bin/env python3
"""Scaffold a new skill and wire it into every file that lists skills.

  python3 scripts/new_skill.py pitch-deck
  python3 scripts/new_skill.py pitch-deck --description "Build a 3-minute pitch. Use when..."
  python3 scripts/new_skill.py judge-prep --bucket hackathon --user-invoked

Creates skills/<bucket>/<name>/SKILL.md and agents/openai.yaml (plus the
bucket's README.md if the bucket is new), then updates plugin.json, the bucket
README, and the top-level README, and records a minor changeset. What's left
is replacing the TODO placeholders with the skill's content;
`python3 scripts/sync_skills.py --check` fails until they're gone.
"""

from __future__ import annotations

import argparse
import sys

from _lib import END_MARKER, NAME_RE, REPO, SKILLS_DIR, START_MARKER, TODO, load_skills, yaml_str
from release import add as add_changeset
from sync_skills import sync

DEFAULT_BUCKET = "hackathon"

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

BUCKET_README = """\
# {title}

{todo}: one line on what this bucket is for.

{start}
{end}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name", help="kebab-case skill name, e.g. pitch-deck")
    parser.add_argument("--bucket", default=DEFAULT_BUCKET, help=f"bucket folder under skills/ (default: {DEFAULT_BUCKET})")
    parser.add_argument("--description", help="SKILL.md description; model-invoked skills should include 'Use when...'")
    parser.add_argument("--display-name", help="name shown in the Codex skill picker (default: from the name)")
    parser.add_argument("--short-description", help="one short line for the Codex skill picker")
    parser.add_argument(
        "--user-invoked",
        action="store_true",
        help="only reachable when the user types it (sets disable-model-invocation)",
    )
    parser.add_argument("--no-changeset", action="store_true", help="don't record a changeset")
    args = parser.parse_args()

    name, bucket = args.name, args.bucket
    for value, what in ((name, "skill name"), (bucket, "bucket")):
        if not NAME_RE.match(value):
            parser.error(f"{what} must be kebab-case (lowercase letters, digits, hyphens): {value!r}")
    if existing := next((s for s in load_skills() if s.name == name), None):
        parser.error(f"a skill named {name!r} already exists at {existing.path.relative_to(REPO)}")

    title = name.replace("-", " ").title()
    bucket_dir = SKILLS_DIR / bucket
    skill_dir = bucket_dir / name
    created = []

    bucket_readme = bucket_dir / "README.md"
    if not bucket_readme.exists():
        bucket_dir.mkdir(parents=True, exist_ok=True)
        bucket_readme.write_text(
            BUCKET_README.format(title=bucket.replace("-", " ").title(), todo=TODO, start=START_MARKER, end=END_MARKER),
            encoding="utf-8",
        )
        created.append(bucket_readme)

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

    if not args.no_changeset:
        created.append(add_changeset("minor", f"Add the `{name}` skill."))

    changed, _ = sync()

    for p in created:
        print(f"created {p.relative_to(REPO)}")
    for p in changed:
        print(f"updated {p.relative_to(REPO)}")

    todos = [p.relative_to(REPO) for p in created if TODO in p.read_text(encoding="utf-8")]
    if todos:
        print(f"\nNext: replace the {TODO} placeholders in:")
        for p in todos:
            print(f"  {p}")
        print("then run `python3 scripts/sync_skills.py` to refresh the README lines from the description.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
