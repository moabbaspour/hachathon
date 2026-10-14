"""Shared helpers for the repo's maintenance scripts. Standard library only."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / "skills"
PLUGIN_JSON = REPO / ".claude-plugin" / "plugin.json"
README = REPO / "README.md"
CHANGELOG = REPO / "CHANGELOG.md"
CHANGESET_DIR = REPO / ".changeset"

# Buckets whose skills ship in the plugin and are listed in README.md.
# Any bucket not listed here as unpromoted is promoted.
UNPROMOTED_BUCKETS = {"deprecated", "in-progress", "misc"}

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
START_MARKER = "<!-- skills:start -->"
END_MARKER = "<!-- skills:end -->"
TODO = "TODO"


@dataclass
class Skill:
    bucket: str
    name: str
    path: Path
    frontmatter: dict[str, str]

    @property
    def description(self) -> str:
        return self.frontmatter.get("description", "")

    @property
    def user_invoked(self) -> bool:
        return self.frontmatter.get("disable-model-invocation", "").lower() == "true"

    @property
    def summary(self) -> str:
        """First sentence of the description, for README one-liners."""
        match = re.match(r"(.+?[.!?])(\s|$)", self.description)
        return match.group(1) if match else self.description

    @property
    def rel_dir(self) -> str:
        return self.path.parent.relative_to(REPO).as_posix()


def parse_frontmatter(text: str) -> dict[str, str]:
    """Parse the flat `key: value` frontmatter used by SKILL.md files."""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    data = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "#")):
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1].replace('\\"', '"')
        data[key.strip()] = value
    return data


def yaml_str(value: str) -> str:
    """Quote a scalar for YAML when a plain scalar would be ambiguous."""
    if not value or re.search(r":\s|\s#|^[\s\"'&*!|>%@`\[\]{},?-]|\s$", value):
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def is_promoted(bucket: str) -> bool:
    return bucket not in UNPROMOTED_BUCKETS


def buckets() -> list[str]:
    return sorted(p.name for p in SKILLS_DIR.iterdir() if p.is_dir())


def load_skills() -> list[Skill]:
    skills = []
    for skill_md in sorted(SKILLS_DIR.glob("*/*/SKILL.md")):
        bucket = skill_md.parent.parent.name
        fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        skills.append(Skill(bucket, skill_md.parent.name, skill_md, fm))
    return skills


def bucket_title(bucket: str) -> str:
    readme = SKILLS_DIR / bucket / "README.md"
    if readme.exists():
        for line in readme.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    return bucket.replace("-", " ").title()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
