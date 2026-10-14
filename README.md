# Skills For Hackathons

My agent skills for hackathons and early-stage products: find a real problem, pick the right first market, and build the smallest MVP that proves something.

The skills are small, composable, and work with any model. Hack around with them and make them your own.

## Installation

A plugin updates itself. [skills.sh](https://skills.sh) copies editable files into your project, and you update them by hand. Pick one per agent, because installing both gives you every skill twice.

<details>
<summary><strong>Claude Code</strong></summary>

```bash
claude plugin marketplace add moabbaspour/hackathon
claude plugin install moabbaspour-skills@moabbaspour
```

</details>

<details>
<summary><strong>Codex</strong></summary>

```bash
codex plugin marketplace add moabbaspour/hackathon
codex plugin add moabbaspour-skills@moabbaspour
```

</details>

<details>
<summary><strong>GitHub Copilot</strong> (CLI and VS Code)</summary>

```bash
copilot plugin marketplace add moabbaspour/hackathon
copilot plugin install moabbaspour-skills@moabbaspour
```

In VS Code, run **Chat: Install Plugin From Source** and enter `https://github.com/moabbaspour/hackathon`.

</details>

<details>
<summary><strong>Gemini CLI</strong> (manual updates)</summary>

```bash
gemini skills install https://github.com/moabbaspour/hackathon.git --path skills/hackathon
```

Re-run the command to update.

</details>

<details>
<summary><strong>Any other agent, or editable files</strong> (manual updates)</summary>

```bash
npx skills@latest add moabbaspour/hackathon -a <agent>  # cursor, opencode, windsurf, ...; omit -a to choose
```

To update, run `npx skills@latest update`, and re-run `add` to pick up new skills.

</details>

## Reference

<!-- skills:start -->

### Hackathon

#### Model-invoked

- **[problem-discovery](./skills/hackathon/problem-discovery/SKILL.md)**: Frame and validate a sharply defined, costly customer problem before proposing solutions for a hackathon or MVP.
- **[market-segmentation](./skills/hackathon/market-segmentation/SKILL.md)**: Segment and size a market, choose a beachhead with strong fit and manageable friction, and estimate near-term obtainable demand for an MVP or hackathon concept.
- **[mvp-experiment](./skills/hackathon/mvp-experiment/SKILL.md)**: Design a narrow, honest hackathon MVP as the fastest test of one measurable hypothesis.

<!-- skills:end -->

## Adding a skill

```bash
python3 scripts/new_skill.py pitch-deck --description "Build a three-minute pitch. Use when..."
```

This creates `skills/hackathon/pitch-deck/` with `SKILL.md` and `agents/openai.yaml`, adds it to `.claude-plugin/plugin.json` and both READMEs, and records a changeset. Then fill in the `TODO` placeholders. Run `python3 scripts/new_skill.py --help` for options (`--bucket`, `--user-invoked`, ...).

After renaming, moving, or deleting a skill, or editing a description, run `python3 scripts/sync_skills.py` to refresh every list. `--check` verifies everything is in sync.

## Releasing

Everything is plain Python 3, no dependencies.

1. After changing a skill, record it: `python3 scripts/release.py add patch "Fix wording in mvp-experiment"` (`patch`, `minor`, or `major`).
2. Push to `main`. The Release workflow opens a "chore: version skills" PR that bumps the version in `.claude-plugin/plugin.json` and updates `CHANGELOG.md`.
3. Merge that PR. The workflow tags `vX.Y.Z` and creates a GitHub release. Plugin installs pick up the new version automatically.

`python3 scripts/release.py status` shows pending changes and the next version.
