# Skills For Hackathons

My agent skills and agents for hackathons and early-stage products: find a real problem, pick the right first market, build the smallest MVP that proves something, and pitch it.

- A **skill** is one focused method, such as problem discovery or market sizing.
- An **agent** chains several skills into one job, such as going from a raw problem to a pitch.

Both work with Claude Code, Codex, GitHub Copilot, and Gemini CLI. Hack around with them and make them your own.

## Installation

Clone this repo once, then install into the project you work in, in the format your AI tool reads:

```bash
git clone https://github.com/moabbaspour/hackathon.git ~/hackathon-skills
cd ~/code/my-project
python3 ~/hackathon-skills/scripts/install.py --vendor codex   # or claude, copilot, gemini
```

Start a new session of your AI tool in that project, and the skills and agents are there.

| `--vendor` | Skills go to | Agents go to |
|---|---|---|
| `claude` | `.claude/skills/<skill>/` | `.claude/agents/<agent>.md` |
| `codex` | `.agents/skills/<skill>/` | `.codex/agents/<agent>.toml` |
| `copilot` | `.github/skills/<skill>/` | `.github/agents/<agent>.agent.md` |
| `gemini` | `.gemini/skills/<skill>/` | `.gemini/agents/<agent>.md` |

Other options:

- `--target <dir>`: install into another project instead of the current directory.
- `--agents problem-to-pitch`: install only that agent, plus the skills it uses.
- `--skills problem-discovery,mvp-experiment`: install only those skills.
- `--uninstall`: remove what the script installed.
- `--list`: list every skill, agent, and vendor.

To update, `git pull` in the clone and run the same install command again. The script only replaces files it installed itself. It refuses to overwrite anything else unless you pass `--force`.

Instead of running it yourself, you can tell your AI tool:

> Clone https://github.com/moabbaspour/hackathon into a temporary folder and run `python3 <that folder>/scripts/install.py --vendor codex --target .` from this project's root. Then tell me which skills and agents were installed and how to start each agent.

## Skills

<!-- skills:start -->

### Model-invoked

- **[competitor-landscape](./skills/competitor-landscape/SKILL.md)**: Map the competitors and alternatives for a problem: who tried it, why some failed and others succeeded, how big each is, what they delivered, and how much funding they raised.
- **[evidence-research](./skills/evidence-research/SKILL.md)**: Research every angle of a problem from recent, traceable evidence: geography, open datasets, statistics, news, regulation, and expert reports from the last five years.
- **[market-segmentation](./skills/market-segmentation/SKILL.md)**: Segment and size a market, choose a beachhead with strong fit and manageable friction, and estimate near-term obtainable demand for an MVP or hackathon concept.
- **[mvp-experiment](./skills/mvp-experiment/SKILL.md)**: Design a narrow, honest hackathon MVP as the fastest test of one measurable hypothesis.
- **[problem-discovery](./skills/problem-discovery/SKILL.md)**: Frame and validate a sharply defined, costly customer problem before proposing solutions for a hackathon or MVP.
- **[solution-selection](./skills/solution-selection/SKILL.md)**: Generate solution options for a validated problem and choose one that is innovative, defensible, and backed by data rather than intuition.

<!-- skills:end -->

## Agents

Each agent runs in its own context, writes only to its own `work/<agent>/<run>/` folder, and never calls another agent. You can run many agents at once, or the same agent on ten problems, without them affecting each other.

<!-- agents:start -->

- **[problem-to-pitch](./agents/problem-to-pitch/AGENT.md)**: Take a hackathon challenge from a raw problem area to an evidence-backed pitch: recent open-data and news research, a validated problem, the competitor landscape with failures, successes, and funding, a beachhead market, a defensible solution, an MVP experiment, and a three-minute pitch script. Skills: `evidence-research`, `problem-discovery`, `competitor-landscape`, `market-segmentation`, `solution-selection`, `mvp-experiment`.

<!-- agents:end -->

To start an agent after installing:

- **Claude Code**: "Use the problem-to-pitch agent on ...".
- **Codex**: "Spawn the problem_to_pitch agent on ...". Codex agent names use underscores, and Codex loads a project's agents only when the project is trusted.
- **Copilot**: pick `problem-to-pitch` in the agent picker, or ask for it by name.
- **Gemini CLI**: `@problem-to-pitch ...`.

## Adding a skill

```bash
python3 scripts/new_skill.py pitch-deck --description "Build a three-minute pitch. Use when..."
```

This creates `skills/pitch-deck/` with `SKILL.md` and `agents/openai.yaml` (Codex picker metadata), and adds it to this README. Fill in the `TODO` placeholders. Run `python3 scripts/new_skill.py --help` for the options.

## Adding an agent

```bash
python3 scripts/new_agent.py churn-detective --skills problem-discovery,mvp-experiment --description "Find why customers leave. Use when..."
```

This creates `agents/churn-detective/AGENT.md` and adds it to this README. `AGENT.md` is the only file you write: `install.py` turns it into each tool's agent format. Fill in the `TODO` placeholders, and keep the `## Isolation` section.

After editing, renaming, or deleting a skill or agent, run `python3 scripts/sync.py` to refresh the lists above. `python3 scripts/sync.py --check` changes nothing and fails on invalid skills or agents, leftover `TODO`s, or a stale README. CI runs it on every pull request.
