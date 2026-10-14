Skills live in bucket folders under `skills/<bucket>/<skill-name>/`. Each bucket has a `README.md` whose first line says what the bucket is for. `deprecated/`, `in-progress/`, and `misc/` are unpromoted: their skills don't ship in the plugin or appear in the top-level `README.md`. Every other bucket is promoted.

Maintenance scripts are Python 3, standard library only:

- `python3 scripts/new_skill.py <name> [--bucket <bucket>] [--description "..."] [--user-invoked]` scaffolds a skill (SKILL.md, agents/openai.yaml, the bucket README if the bucket is new), updates every skill list, and records a minor changeset. Always create skills with it; then replace the `TODO` placeholders.
- `python3 scripts/sync_skills.py` regenerates `.claude-plugin/plugin.json`'s `skills` array, each bucket `README.md`, and the top-level `README.md` from the SKILL.md files. The lists live between `<!-- skills:start -->` and `<!-- skills:end -->`: never edit inside the markers by hand. Run it after renaming, moving, or deleting a skill, or after changing a description. `--check` changes nothing and fails on drift, invalid skills, or leftover `TODO`s; CI runs it.
- `python3 scripts/release.py add <patch|minor|major> "message"` records a changeset. Every user-visible change to a skill needs one. Never edit `version` in `plugin.json` by hand: the Release workflow runs `release.py version`.
- `scripts/link-skills.sh` symlinks every skill into `~/.claude/skills` and `~/.agents/skills` for local testing.

Run `claude plugin validate .` after touching either manifest in `.claude-plugin/`.

Each skill is a folder containing a `SKILL.md` (frontmatter `name` must match the folder name) and an `agents/openai.yaml` with Codex UI metadata (`interface.display_name`, `interface.short_description`). Supporting reference files sit next to `SKILL.md`. The first sentence of the `description` becomes the skill's one-liner in the READMEs.

Every `SKILL.md` is either:

- **User-invoked**: `disable-model-invocation: true` in frontmatter plus `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. The `description` is a one-line human-facing summary.
- **Model-invoked** (the default): neither flag. The `description` keeps rich trigger phrasing ("Use when...") so the model can reach for it.

When one skill depends on another, say so as an explicit instruction to call the Skill tool with the named skill (`Call the Skill tool with "problem-discovery"`), not a cross-folder file link.
