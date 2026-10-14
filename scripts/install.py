#!/usr/bin/env python3
"""Install skills and agents into a project, in the format one AI coding tool reads.

  python3 scripts/install.py --vendor codex                        # everything, into the current directory
  python3 scripts/install.py --vendor claude --target ~/code/my-app
  python3 scripts/install.py --vendor copilot --agents problem-to-pitch   # the agent plus the skills it uses
  python3 scripts/install.py --vendor gemini --skills problem-discovery
  python3 scripts/install.py --vendor codex --uninstall            # remove what this script installed
  python3 scripts/install.py --list

Vendors and where files go, relative to --target:

  claude   .claude/skills/<skill>/    .claude/agents/<agent>.md
  codex    .agents/skills/<skill>/    .codex/agents/<agent>.toml
  copilot  .github/skills/<skill>/    .github/agents/<agent>.agent.md
  gemini   .gemini/skills/<skill>/    .gemini/agents/<agent>.md

Re-running updates what this script installed earlier. It never overwrites a
skill or agent it didn't install, unless you pass --force.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from _lib import Agent, Skill, load_agents, load_skills, rel, yaml_str
from sync import validate_agents, validate_skills

# Marks what this script installed, so re-runs and --uninstall only touch those files.
MARKER = "installed-by: hackathon-skills"
SKILL_MARKER_FILE = ".installed-by-hackathon-skills"


def skills_preamble(a: Agent) -> str:
    """For tools that can't preload skills: name them up front."""
    skills = ", ".join(f"`{s}`" for s in a.skills)
    return (
        f"You are the `{a.name}` agent. {a.description}\n\n"
        f"You work only with these skills: {skills}. Before each workflow step that names a skill, "
        "open that skill and follow it. Don't use any other skill.\n\n"
    )


def md_marker(a: Agent) -> str:
    return f"<!-- {MARKER}; source: {rel(a.path)}; re-run scripts/install.py instead of editing -->\n\n"


def render_claude(a: Agent) -> str:
    # Claude Code preloads the listed skills into the subagent's context.
    skills = "".join(f"  - {s}\n" for s in a.skills)
    return (
        f"---\nname: {a.name}\ndescription: {yaml_str(a.description)}\nskills:\n{skills}---\n\n"
        + md_marker(a)
        + a.body.strip()
        + "\n"
    )


def render_markdown_agent(a: Agent) -> str:
    """Copilot and Gemini CLI: name + description frontmatter, instructions in the body."""
    return (
        f"---\nname: {a.name}\ndescription: {yaml_str(a.description)}\n---\n\n"
        + md_marker(a)
        + skills_preamble(a)
        + a.body.strip()
        + "\n"
    )


def render_codex(a: Agent) -> str:
    instructions = skills_preamble(a) + a.body.strip() + "\n"
    return (
        f"# {MARKER}; source: {rel(a.path)}; re-run scripts/install.py instead of editing\n"
        # Codex agent names are snake_case identifiers.
        f"name = {json.dumps(a.name.replace('-', '_'))}\n"
        f"description = {json.dumps(a.description, ensure_ascii=False)}\n"
        f"developer_instructions = '''\n{instructions}'''\n"
    )


@dataclass
class Vendor:
    skills_dir: str
    agents_dir: str
    agent_file: str  # format string with {name}
    render: Callable[[Agent], str]
    how_to_use: str  # format string with {agent} and {codex_agent}


VENDORS = {
    "claude": Vendor(
        ".claude/skills",
        ".claude/agents",
        "{name}.md",
        render_claude,
        "Start a new Claude Code session in the project, then ask: \"Use the {agent} agent on ...\".",
    ),
    "codex": Vendor(
        ".agents/skills",
        ".codex/agents",
        "{name}.toml",
        render_codex,
        "Start a new Codex session in the project (it must be a trusted project), then ask: "
        "\"Spawn the {codex_agent} agent on ...\".",
    ),
    "copilot": Vendor(
        ".github/skills",
        ".github/agents",
        "{name}.agent.md",
        render_markdown_agent,
        "Reload Copilot, then pick {agent} in the agent picker, or ask: \"Use the {agent} agent on ...\".",
    ),
    "gemini": Vendor(
        ".gemini/skills",
        ".gemini/agents",
        "{name}.md",
        render_markdown_agent,
        "Start a new Gemini CLI session in the project, then type: \"@{agent} ...\".",
    ),
}
ALIASES = {"github": "copilot", "github-copilot": "copilot", "claude-code": "claude", "openai": "codex"}


def ours(path: Path) -> bool:
    if path.is_dir():
        return (path / SKILL_MARKER_FILE).exists()
    return path.is_file() and MARKER in path.read_text(encoding="utf-8", errors="replace")


def split(value: str | None) -> list[str]:
    return [v.strip() for v in (value or "").split(",") if v.strip()]


def select(args: argparse.Namespace, skills: dict[str, Skill], agents: dict[str, Agent]) -> tuple[list[Skill], list[Agent]]:
    want_skills, want_agents = split(args.skills), split(args.agents)
    if not want_skills and not want_agents:
        return list(skills.values()), list(agents.values())
    for name in want_agents:
        if name not in agents:
            raise SystemExit(f"error: unknown agent {name!r}; available: {', '.join(agents) or 'none'}")
    picked_agents = [agents[n] for n in want_agents]
    # An agent brings the skills it works with.
    names = list(dict.fromkeys(want_skills + [s for a in picked_agents for s in a.skills]))
    for name in names:
        if name not in skills:
            raise SystemExit(f"error: unknown skill {name!r}; available: {', '.join(skills)}")
    return [skills[n] for n in names], picked_agents


def print_list(skills: list[Skill], agents: list[Agent]) -> None:
    print("Skills:")
    for s in skills:
        print(f"  {s.name}")
    print("Agents:")
    for a in agents:
        print(f"  {a.name}  (skills: {', '.join(a.skills)})")
    print("Vendors:")
    for name, v in VENDORS.items():
        print(f"  {name:8} {v.skills_dir}/<skill>/  {v.agents_dir}/{v.agent_file.format(name='<agent>')}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vendor", help=f"one of: {', '.join(VENDORS)}")
    parser.add_argument("--target", default=".", help="project to install into (default: the current directory)")
    parser.add_argument("--skills", help="comma-separated skills (default: all, unless --agents is given)")
    parser.add_argument("--agents", help="comma-separated agents; their skills are installed too (default: all)")
    parser.add_argument("--uninstall", action="store_true", help="remove the selected skills and agents this script installed")
    parser.add_argument("--force", action="store_true", help="overwrite skills and agents this script didn't install")
    parser.add_argument("--list", action="store_true", help="list skills, agents, and vendors, then exit")
    args = parser.parse_args()

    all_skills = {s.name: s for s in load_skills()}
    all_agents = {a.name: a for a in load_agents()}
    if args.list:
        print_list(list(all_skills.values()), list(all_agents.values()))
        return 0

    vendor_name = ALIASES.get((args.vendor or "").lower(), (args.vendor or "").lower())
    if vendor_name not in VENDORS:
        parser.error(f"--vendor must be one of: {', '.join(VENDORS)}")
    vendor = VENDORS[vendor_name]
    target = Path(args.target).expanduser().resolve()
    if not target.is_dir():
        parser.error(f"--target is not a directory: {target}")

    skills, agents = select(args, all_skills, all_agents)
    plan = [(target / vendor.skills_dir / s.name, s) for s in skills]
    plan += [(target / vendor.agents_dir / vendor.agent_file.format(name=a.name), a) for a in agents]

    if args.uninstall:
        removed = 0
        for dest, _ in plan:
            if dest.exists() and ours(dest):
                shutil.rmtree(dest) if dest.is_dir() else dest.unlink()
                print(f"removed {dest.relative_to(target)}")
                removed += 1
        print(f"\nRemoved {removed} item(s) from {target}." if removed else "Nothing to remove.")
        return 0

    errors = validate_skills(skills) + validate_agents(agents, list(all_skills.values()))
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        print("Fix these first; `python3 scripts/sync.py --check` shows every problem.", file=sys.stderr)
        return 1
    clashes = [dest for dest, _ in plan if dest.exists() and not ours(dest)]
    if clashes and not args.force:
        for dest in clashes:
            print(f"error: {dest.relative_to(target)} exists and wasn't installed by this script", file=sys.stderr)
        print("Remove it, or pass --force to overwrite.", file=sys.stderr)
        return 1

    for dest, item in plan:
        if isinstance(item, Skill):
            if dest.exists():
                shutil.rmtree(dest) if dest.is_dir() else dest.unlink()
            shutil.copytree(item.dir, dest, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
            (dest / SKILL_MARKER_FILE).write_text(f"{MARKER}; source: {rel(item.dir)}\n", encoding="utf-8")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(vendor.render(item), encoding="utf-8")
        print(f"installed {dest.relative_to(target)}")

    print(f"\nInstalled {len(skills)} skill(s) and {len(agents)} agent(s) for {vendor_name} into {target}.")
    for a in agents:
        print("  " + vendor.how_to_use.format(agent=a.name, codex_agent=a.name.replace("-", "_")))
    if agents:
        print("Agents write their runs to work/<agent>/<run>/; add `work/` to .gitignore if you don't want to commit them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
