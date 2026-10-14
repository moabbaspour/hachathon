---
name: mvp-experiment
description: Design a narrow, honest hackathon MVP as the fastest test of one measurable hypothesis. Use for prototype scope, demo planning, build-vs-simulate decisions, experiment loops, or short-stage presentations.
---

# MVP Experiment

## Mission
Turn one evidence-backed problem into a testable hypothesis and the smallest prototype that can produce credible evidence. An MVP is an experiment, not a miniature full product and not a collection of screens.

## Guardrails
- Carry forward the problem statement and target user; if those are weak, return to discovery rather than building around them.
- State what is real, simulated, manually operated, hard-coded, or planned. Never imply a simulated integration or model is live.
- Build the proof and calculation that supports the claimed outcome for real. Fake only the wrapper or external dependency when clearly disclosed.
- Do not invent baseline data, savings, accuracy, customer quotes, adoption, or results. Show assumptions and uncertainty.
- A demo is not a validation study. Separate “the prototype runs” from “the hypothesis is supported.”

## Workflow

### 1. Write one core hypothesis
Use:

> If we [specific intervention/action], then [measurable outcome] will change by [target amount/unit] for [specific user] in [defined context/timeframe].

Examples in the workshop concern energy or water savings. Do not copy the example percentages into another project. Define baseline, measurement method, comparison period, and minimum evidence needed. If the percentage is unknown, test direction or feasibility first and say so.

### 2. Choose the riskiest assumption
List assumptions about desirability, feasibility, and viability. Select the one that could invalidate the project and can be tested in the available time. Explain why the experiment informs this decision.

### 3. Cut scope aggressively
Keep only the feature that proves or disproves the hypothesis. For every proposed feature, ask: “If this does not work, does anything else matter?” Defer or remove the rest. The workshop’s “keep one, cross off seven” is a scope heuristic, not a required feature count.

Create a scope table:
- build for real;
- simulate/mock, with disclosure;
- manual concierge action;
- out of scope/roadmap.

### 4. Select prototype fidelity
Prefer the least costly form that can answer the question:
- clickable mock/screen for comprehension or workflow;
- scripted playback for sensor/data flow;
- transparent if/then logic for a model hypothesis;
- manual service for willingness-to-engage or workflow tests;
- real calculation/model for outcome claims.

A live demo should let a judge alter a meaningful input and see a valid output when that is central to the proof. For every mock, specify what a real deployment would still require.

### 5. Define the experiment
Specify:
- participant and recruitment source (not teammates as a substitute for target users);
- task or exposure;
- baseline and data provenance;
- success, failure, and inconclusive thresholds;
- duration and sample size;
- what will be observed, not just asked;
- safety/privacy constraints;
- how the result changes the product decision.

Test with a real person where possible: show the artifact, stay quiet, observe confusion and workarounds, then ask what it costs today, what they would change next, and what would prevent use. Test calculations against real bills/tariffs/equipment specifications where relevant. Make no claims beyond those checks.

### 6. Run short loops
Repeat Build → Test → Learn → Improve. After each loop, write one sentence: “We learned that…” Change one meaningful thing at a time, then keep/change/cut the hypothesis or feature. Watch for:
- **confusion**: user cannot understand the flow;
- **disbelief**: user doubts the result or the numbers;
- **polite praise**: “nice” without costly behavior change.

Treat these as signals to investigate, not automatic proof of success/failure.

### 7. Build backward from the stage demo
Plan a reliable 60-second core demo, then add only supporting detail. Prioritize a clean start state, one user task, one visible result, and a fallback recording/screenshot if live connectivity fails. In the pitch, disclose prototype boundaries and show the evidence separately from the product vision.

## Required outputs
1. Hypothesis card (user, action, outcome, metric, baseline, timeframe).
2. Riskiest assumption and why it matters.
3. Scope cut table (real / simulated / manual / excluded).
4. Test protocol and thresholds.
5. Iteration log: observation → learning → change → next test.
6. Demo script with explicit disclosures and fallback.
7. Claim audit: each on-stage claim linked to measured evidence or clearly labeled assumption/roadmap.

## Review checklist
Reject or revise the plan if it has multiple untested hypotheses, unmeasurable outcomes, no named user, a feature list without a test, fake numbers presented as actual, an undisclosed mock, no failure threshold, or a pitch claim that exceeds the evidence.
