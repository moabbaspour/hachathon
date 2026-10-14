#!/usr/bin/env python3
"""Scaffold a new agent and add it to the README.

  python3 scripts/new_agent.py problem-to-pitch --skills problem-discovery,market-segmentation,mvp-experiment
  python3 scripts/new_agent.py churn-detective --skills problem-discovery --description "Find why... Use when..."

Creates agents/<name>/AGENT.md, the one source that install.py turns into each
vendor's agent format, then updates README.md. What's left is replacing the
TODO placeholders; `python3 scripts/sync.py --check` and install.py refuse the
agent until they're gone.
"""

from __future__ import annotations

import argparse
import sys

from _lib import AGENTS_DIR, ISOLATION_HEADING, NAME_RE, REPO, TODO, load_agents, load_skills, yaml_str
from sync import sync

AGENT_BODY = """\
# {title}

## Mission
{todo}: what this agent takes in and what it hands back, in two or three sentences.

{isolation}
- Every run is independent. Don't read, reuse, or depend on another agent's or another run's files, notes, or conclusions.
- Write only inside `work/{name}/<run-slug>/` in the current project, where `<run-slug>` is a short kebab-case name for this run's topic. Create it at the start; if it already exists, add a numeric suffix.
- Don't call or hand off to another agent. Make every decision yourself and record it in your run folder.
- If something you need is missing, write down the assumption and continue rather than borrowing from another run.

## Workflow

### 1. {todo}
Use the `{first_skill}` skill to {todo}.

### 2. {todo}
{todo}: next step, naming the skill it uses.

## Output
{todo}: the files this agent leaves in its run folder, and the summary it returns.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name", help="kebab-case agent name, e.g. problem-to-pitch")
    parser.add_argument("--skills", required=True, help="comma-separated skills the agent works with, in workflow order")
    parser.add_argument("--description", help="when to use this agent; include 'Use when...' so the model can delegate to it")
    args = parser.parse_args()

    name = args.name
    if not NAME_RE.match(name):
        parser.error(f"agent name must be kebab-case (lowercase letters, digits, hyphens): {name!r}")
    if any(a.name == name for a in load_agents()):
        parser.error(f"an agent named {name!r} already exists at agents/{name}/")

    skills = {s.name: s for s in load_skills()}
    if name in skills:
        parser.error(f"{name!r} is already a skill name; pick a different agent name")
    wanted = [s.strip() for s in args.skills.split(",") if s.strip()]
    for skill in wanted:
        if skill not in skills:
            parser.error(f"unknown skill {skill!r}; available: {', '.join(sorted(skills))}")
        if skills[skill].user_invoked:
            parser.error(f"skill {skill!r} is user-invoked, so an agent can't load it")

    description = args.description or f"{TODO}: what it does, in one sentence. Use when {TODO}."
    frontmatter = [f"name: {name}", f"description: {yaml_str(description)}", "skills:"]
    frontmatter += [f"  - {s}" for s in wanted]
    body = AGENT_BODY.format(
        title=name.replace("-", " ").title(),
        name=name,
        todo=TODO,
        isolation=ISOLATION_HEADING,
        first_skill=wanted[0],
    )
    agent_md = AGENTS_DIR / name / "AGENT.md"
    agent_md.parent.mkdir(parents=True)
    agent_md.write_text("---\n" + "\n".join(frontmatter) + "\n---\n\n" + body, encoding="utf-8")

    stale, _ = sync()

    print(f"created {agent_md.relative_to(REPO)}")
    if stale:
        print("updated README.md")
    print(f"\nNext: replace the {TODO} placeholders in agents/{name}/AGENT.md, then run `python3 scripts/sync.py`.")
    print(f"Install it with: python3 scripts/install.py --vendor <claude|codex|copilot|gemini> --agents {name} --target <project>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
