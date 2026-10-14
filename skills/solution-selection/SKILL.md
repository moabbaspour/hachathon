---
name: solution-selection
description: "Generate solution options for a validated problem and choose one that is innovative, defensible, and backed by data rather than intuition. Use when moving from a problem to a solution, comparing approaches, justifying a solution to judges or investors, or finding the gap competitors left open."
---

# Solution Selection

## Mission
Turn a well-evidenced problem into one chosen solution that a sceptical judge or investor would accept. It must address the supported root cause, be new where it matters, avoid the mistakes that sank earlier attempts, and rest on facts at every step. Gut feeling may generate ideas, but it never selects one.

## Inputs
- The problem statement and evidence ledger, from the `evidence-research` and `problem-discovery` skills.
- The competitor, failure, and success analysis, from the `competitor-landscape` skill.
- The beachhead segment, from the `market-segmentation` skill, if it exists yet.

If an input is missing, say so. Either get it first or continue with the gap labelled, and lower the confidence of the decision accordingly.

## Rules
- **Cite the evidence.** Every score and every argument cites ledger rows. An argument without evidence is labelled an **assumption** and lowers that option's confidence. It can't raise its score.
- **Five-year window.** Precedents and data that support a choice must fall within the five years before the run date. Older precedents are history and need a reason why they still apply.
- **Root cause first.** An option that doesn't act on a root cause the evidence supports is rejected, however novel it is.
- **Innovation means a specific difference.** It must differ from what competitors do on a dimension users care about, and the evidence must explain why it is possible or needed now. Adding "AI", "blockchain", or "a platform" is not innovation on its own.
- **Defensible means it survives questions.** The choice must still hold after the strongest objections have been answered with evidence.

## Workflow

### 1. Generate options widely
Produce at least six distinct options before judging any of them. Spread them across these types:
- product or technology;
- process or service design;
- business model (who pays, how, and when);
- partnership or distribution;
- policy or institutional;
- data or information.

Always include the status quo and the best existing competitor as baselines. Use these prompts:
- What worked for this problem in another geography or industry within the last five years?
- Which failed competitor's idea would work now that the cause of its failure has changed?
- Which step in the current workaround can be removed?
- Who else could pay?
- What new data, infrastructure, or regulation from the window makes something possible now?

### 2. Screen
Drop any option that:
- misses the root cause;
- repeats a documented failure cause that still applies;
- breaks a regulation;
- can't be tested within the team's constraints.

Write one evidence-backed line for each dropped option.

### 3. Score the rest
Score each remaining option 1 to 5 on each criterion. Anchor what 1, 3, and 5 mean, and cite evidence for every score:
- **Root-cause fit**: how directly it removes the cause.
- **Evidence of impact**: precedents and data showing that this kind of solution works.
- **Feasibility**: technology, data, team, and time.
- **Viability**: unit economics and a payer who can and will pay.
- **Adoption**: fit with user behaviour, trust, and infrastructure in this geography.
- **Differentiation**: a meaningful difference from every competitor.
- **Defensibility**: what stops others copying it, such as data, network, distribution, partnerships, regulatory position, or know-how.
- **Why now**: recent changes, inside the window, that make it timely.
- **Risk**: the regulatory, technical, and market risks, and how hard each is to reduce.

Also record a confidence level for each score. Don't let a high average hide a fatal score. Show how sensitive the choice is to the two least certain inputs.

### 4. Red-team the leader
Write the five strongest objections a judge, investor, or competitor would raise, and answer each with evidence. If an objection can't be answered, either change the option, pick the runner-up, or record it as the main risk to test.

### 5. Decide
Choose one solution and name the runner-up. State:
- what would make you switch to the runner-up (the kill criteria);
- the assumption that is riskiest and could still be tested, and hand it to the `mvp-experiment` skill.

## Required outputs
1. Option list with type, short description, and the evidence that inspired each option.
2. Screening log for the dropped options.
3. Scoring matrix: criteria × options, with anchored scores, cited evidence, and confidence.
4. One-page summary of the chosen solution:
   - what it is and for whom;
   - which root cause it acts on;
   - the innovation;
   - why now;
   - the difference from each main competitor;
   - defensibility;
   - unit economics in outline.
5. Objection log: objection, evidence-backed answer, and what remains open.
6. Decision: the choice, the runner-up, the kill criteria, and the riskiest assumption for the MVP.

## Quality check
Reject the decision if:
- any score lacks a source;
- the chosen option doesn't touch a supported root cause;
- the innovation is only a technology label;
- the "why now" relies on evidence older than five years;
- it repeats a documented failure cause without saying what changed;
- an objection from step 4 was left unanswered without being recorded as a risk.
