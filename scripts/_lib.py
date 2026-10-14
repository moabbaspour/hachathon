"""Shared helpers for the repo's scripts. Standard library only."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / "skills"
AGENTS_DIR = REPO / "agents"
README = REPO / "README.md"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SKILLS_START_MARKER = "<!-- skills:start -->"
SKILLS_END_MARKER = "<!-- skills:end -->"
AGENTS_START_MARKER = "<!-- agents:start -->"
AGENTS_END_MARKER = "<!-- agents:end -->"
# Every agent body needs this heading: the rules that keep runs independent.
ISOLATION_HEADING = "## Isolation"
TODO = "TODO"

Frontmatter = dict[str, "str | list[str]"]


def parse_frontmatter(text: str) -> tuple[Frontmatter, str]:
    """Parse flat `key: value` frontmatter, plus `key:` followed by `  - item` lists. Returns (frontmatter, body)."""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}, text
    data: Frontmatter = {}
    key = None
    for line in match.group(1).splitlines():
        item = re.match(r"^\s+-\s+(.*)$", line)
        if item and key is not None:
            value = data[key]
            data[key] = (value if isinstance(value, list) else []) + [item.group(1).strip().strip("\"'")]
            continue
        if ":" not in line or line.startswith((" ", "#")):
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1].replace('\\"', '"')
        data[key] = value
    return data, text[match.end() :]


def yaml_str(value: str) -> str:
    """Quote a scalar for YAML when a plain scalar would be ambiguous."""
    if not value or re.search(r":\s|\s#|^[\s\"'&*!|>%@`\[\]{},?-]|\s$", value):
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def first_sentence(text: str) -> str:
    match = re.match(r"(.+?[.!?])(\s|$)", text)
    return match.group(1) if match else text


@dataclass
class Skill:
    name: str
    path: Path  # skills/<name>/SKILL.md
    frontmatter: Frontmatter

    @property
    def dir(self) -> Path:
        return self.path.parent

    @property
    def description(self) -> str:
        value = self.frontmatter.get("description", "")
        return value if isinstance(value, str) else ""

    @property
    def user_invoked(self) -> bool:
        return str(self.frontmatter.get("disable-model-invocation", "")).lower() == "true"


@dataclass
class Agent:
    name: str
    path: Path  # agents/<name>/AGENT.md
    frontmatter: Frontmatter
    body: str

    @property
    def description(self) -> str:
        value = self.frontmatter.get("description", "")
        return value if isinstance(value, str) else ""

    @property
    def skills(self) -> list[str]:
        value = self.frontmatter.get("skills", [])
        return value if isinstance(value, list) else [v.strip() for v in value.split(",") if v.strip()]


def load_skills() -> list[Skill]:
    skills = []
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        fm, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        skills.append(Skill(skill_md.parent.name, skill_md, fm))
    return skills


def load_agents() -> list[Agent]:
    agents = []
    for agent_md in sorted(AGENTS_DIR.glob("*/AGENT.md")):
        fm, body = parse_frontmatter(agent_md.read_text(encoding="utf-8"))
        agents.append(Agent(agent_md.parent.name, agent_md, fm, body))
    return agents


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()
