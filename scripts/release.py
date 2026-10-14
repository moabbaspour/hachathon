#!/usr/bin/env python3
"""Versioning and changelog, in the changesets style, without Node.

The version lives in .claude-plugin/plugin.json. Pending changes are
Markdown files in .changeset/ with the bump type in their frontmatter.

  python3 scripts/release.py add minor "Add the pitch-deck skill"
  python3 scripts/release.py status     # list pending changesets and the next version
  python3 scripts/release.py version    # bump plugin.json, write CHANGELOG.md, delete changesets
  python3 scripts/release.py current    # print the current version
  python3 scripts/release.py notes      # print the CHANGELOG section for the current version
"""

from __future__ import annotations

import argparse
import os
import re
import secrets
import sys
from dataclasses import dataclass
from pathlib import Path

from _lib import CHANGELOG, CHANGESET_DIR, PLUGIN_JSON, parse_frontmatter, read_json

BUMPS = ("patch", "minor", "major")
HEADINGS = {"major": "Major Changes", "minor": "Minor Changes", "patch": "Patch Changes"}


@dataclass
class Changeset:
    path: Path
    bump: str
    message: str


def current_version() -> str:
    return read_json(PLUGIN_JSON)["version"]


def bumped(version: str, bump: str) -> str:
    major, minor, patch = (int(x) for x in version.split("."))
    if bump == "major":
        return f"{major + 1}.0.0"
    if bump == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def pending() -> list[Changeset]:
    changesets = []
    for path in sorted(CHANGESET_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        bump = next((v for v in parse_frontmatter(text).values() if v in BUMPS), None)
        if not bump:
            raise SystemExit(f"error: {path.name} has no patch/minor/major bump in its frontmatter")
        message = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S).strip()
        changesets.append(Changeset(path, bump, message))
    return changesets


def next_version(changesets: list[Changeset]) -> str | None:
    if not changesets:
        return None
    bump = max((c.bump for c in changesets), key=BUMPS.index)
    return bumped(current_version(), bump)


def add(bump: str, message: str) -> Path:
    name = read_json(PLUGIN_JSON)["name"]
    slug = "-".join(re.findall(r"[a-z0-9]+", message.lower())[:5]) or "change"
    path = CHANGESET_DIR / f"{slug}-{secrets.token_hex(2)}.md"
    CHANGESET_DIR.mkdir(exist_ok=True)
    path.write_text(f'---\n"{name}": {bump}\n---\n\n{message.strip()}\n', encoding="utf-8")
    return path


def set_version(version: str) -> None:
    source = PLUGIN_JSON.read_text(encoding="utf-8")
    # Rewrite only the version line, to keep key order and formatting.
    updated, count = re.subn(r'("version"\s*:\s*")[^"]*(")', rf"\g<1>{version}\g<2>", source, count=1)
    if not count:
        raise SystemExit(f"error: no version field in {PLUGIN_JSON}")
    PLUGIN_JSON.write_text(updated, encoding="utf-8")


def changelog_section(version: str, changesets: list[Changeset]) -> str:
    lines = [f"## {version}"]
    for bump in reversed(BUMPS):
        items = [c for c in changesets if c.bump == bump]
        if not items:
            continue
        lines += ["", f"### {HEADINGS[bump]}", ""]
        for c in items:
            first, *rest = c.message.splitlines() or [""]
            lines.append(f"- {first}")
            lines += [f"  {line}" if line else "" for line in rest]
    return "\n".join(lines) + "\n"


def write_changelog(section: str) -> None:
    title = f"# {read_json(PLUGIN_JSON)['name']}\n"
    text = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else title
    if text.startswith("# "):
        head, _, body = text.partition("\n")
        text = f"{head}\n\n{section}\n{body.lstrip()}"
    else:
        text = f"{title}\n{section}\n{text}"
    CHANGELOG.write_text(text.rstrip() + "\n", encoding="utf-8")


def notes(version: str) -> str:
    text = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else ""
    match = re.search(rf"^## {re.escape(version)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return match.group(1).strip() if match else ""


def github_output(**values: str) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            for k, v in values.items():
                f.write(f"{k}={v}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_add = sub.add_parser("add", help="record a pending change")
    p_add.add_argument("bump", choices=BUMPS)
    p_add.add_argument("message", help="changelog entry, Markdown")
    sub.add_parser("status", help="list pending changesets")
    sub.add_parser("version", help="apply pending changesets")
    sub.add_parser("current", help="print the current version")
    sub.add_parser("notes", help="print the CHANGELOG section for the current version")
    args = parser.parse_args()

    if args.cmd == "add":
        print(f"created {add(args.bump, args.message).relative_to(CHANGESET_DIR.parent)}")
    elif args.cmd == "current":
        print(current_version())
    elif args.cmd == "notes":
        print(notes(current_version()))
    elif args.cmd == "status":
        changesets = pending()
        for c in changesets:
            print(f"{c.bump:<6} {c.path.name}: {c.message.splitlines()[0] if c.message else ''}")
        nxt = next_version(changesets)
        print(f"{current_version()} -> {nxt}" if nxt else "no pending changesets")
        github_output(pending=str(bool(changesets)).lower())
    elif args.cmd == "version":
        changesets = pending()
        version = next_version(changesets)
        if not version:
            print("no pending changesets")
            return 0
        set_version(version)
        write_changelog(changelog_section(version, changesets))
        for c in changesets:
            c.path.unlink()
        print(f"version {version}")
        github_output(version=version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
