Skills live in `skills/<skill-name>/` and agents in `agents/<agent-name>/`. Nothing here is a plugin. `scripts/install.py` copies skills and renders agents into another project, in the format of one AI tool.

Scripts are Python 3, standard library only:

- `python3 scripts/new_skill.py <name> [--description "..."] [--user-invoked]` scaffolds a skill (`SKILL.md`, `agents/openai.yaml`) and updates the README. Always create skills with it; then replace the `TODO` placeholders.
- `python3 scripts/new_agent.py <name> --skills <skill>,<skill> [--description "..."]` scaffolds an agent (`agents/<name>/AGENT.md`) and updates the README. Always create agents with it; then replace the `TODO` placeholders.
- `python3 scripts/sync.py` validates every skill and agent, and regenerates the lists in `README.md` between `<!-- skills:start -->`/`<!-- skills:end -->` and `<!-- agents:start -->`/`<!-- agents:end -->`. Never edit inside the markers by hand. Run it after adding, renaming, or deleting a skill or agent, or after changing a description. `--check` changes nothing and fails on drift, invalid skills or agents, or leftover `TODO`s; CI runs it.
- `python3 scripts/install.py --vendor <claude|codex|copilot|gemini> [--target <dir>] [--skills ...] [--agents ...] [--uninstall]` installs into a project. The per-vendor paths and agent formats live in its `VENDORS` table. To support another tool, add an entry there and document the paths in its docstring and in `README.md`.

## Skills

Each skill is a folder containing a `SKILL.md` (frontmatter `name` must match the folder name) and an `agents/openai.yaml` with Codex UI metadata (`interface.display_name`, `interface.short_description`). Supporting reference files sit next to `SKILL.md`. The first sentence of the `description` becomes the skill's one-liner in the README.

Every `SKILL.md` is either:

- **User-invoked**: `disable-model-invocation: true` in frontmatter plus `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. The `description` is a one-line human-facing summary.
- **Model-invoked** (the default): neither flag. The `description` keeps rich trigger phrasing ("Use when...") so the model can reach for it.

When one skill depends on another, name it in plain words ("use the `problem-discovery` skill"), not as a tool call or a cross-folder file link, so it works in every tool.

## Agents

An agent chains model-invoked skills into one job. `agents/<name>/AGENT.md` is its only source, with frontmatter `name` (matching the folder name), `description` ("Use when..." phrasing), and `skills` (a YAML list, in workflow order). `install.py` renders it per vendor:

- Claude Code gets the `skills` list in frontmatter and preloads those skills.
- Codex (TOML, snake_case `name`), Copilot, and Gemini CLI can't preload skills, so the rendered instructions open by naming them.

Agents must stay independent so many can run side by side:

- Every agent body keeps the `## Isolation` section from the scaffold: write only inside `work/<agent>/<run-slug>/`, never read another agent's or run's files, never call or hand off to another agent, and record decisions in the run folder.
- Write each workflow step as "Use the `<skill>` skill to ...".
- Keep agent bodies tool-neutral: no tool names, model names, or paths outside the run folder, and no `'''` (it would break the Codex TOML).
