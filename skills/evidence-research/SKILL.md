---
name: evidence-research
description: "Research every angle of a problem from recent, traceable evidence: geography, open datasets, statistics, news, regulation, and expert reports from the last five years. Use when framing a problem, checking whether a pain is real and growing, building an evidence ledger, or before choosing a solution."
---

# Evidence Research

## Mission
Build a complete, sourced picture of a problem before anyone decides what it is or how to solve it. Cover every angle that could change the decision, in the specific geography where the problem lives. Base it on recent open data, official statistics, and news, not on intuition or memory. The result is an evidence ledger that every later decision can cite.

## Evidence rules
- **Five-year window.** Write the run date at the top of the brief and compute the cutoff: run date minus five years. Only evidence published within the window, or describing a period within it, may support a decision. Older material may appear only as labelled historical background or as the start of a trend line, never as the current state.
- **Stale data.** If the newest data for a key metric is older than the cutoff, say so, mark it **stale**, and lower the confidence of anything that depends on it.
- **Every claim has a source.** That means title, publisher, URL, publication date, and access date. A claim without one is an **assumption** and must be labelled as such. Never present remembered facts as current data.
- **Triangulate.** Confirm every number that a decision depends on with at least two independent sources where possible. When sources disagree, record both values and explain the gap: different definitions, periods, or methods.
- **Rank evidence types.** From strongest to weakest: official statistics and administrative data, open datasets with a documented method, peer-reviewed studies, reports from multilateral bodies or regulators, reputable industry reports, quality journalism, then company claims and opinion. Record the type of each source. Never treat a press release or a single anecdote as a fact about a market.
- **No research tools, no data.** If you can search the web or fetch documents, do it. If you can't, say so plainly. Then write the research plan instead (queries, sources to check, what each would settle) and mark every affected claim as unverified. Never fill the gap with invented figures.
- **Desk research isn't validation.** It shows whether a problem exists and how large it is. It doesn't prove that users want a particular solution.

## Workflow

### 1. Fix the scope
Write down the problem area, the geography (country, region, city, or a rural/urban split, as precise as the problem needs), the affected population, the run date, and the five-year cutoff. List the local languages. Search in them as well as in English, because local data and news are often only published locally.

### 2. Map the angles
For each angle, write the questions whose answers could change the decision, then research them. Skip an angle only with a written reason.
- **People**: who is affected, how many, which demographics, how often, and how badly.
- **Economic**: cost of the problem, who bears it, prices, incomes, budgets, and willingness or ability to pay.
- **Geography and infrastructure**: regional differences, connectivity, logistics, energy, climate, and urban versus rural.
- **Regulation and policy**: laws, standards, licences, subsidies, government programmes, and upcoming changes.
- **Technology**: what is possible now, adoption levels, data availability, and enabling or blocking tech.
- **Social and cultural**: behaviour, trust, norms, language, and informal workarounds.
- **Environmental**: impact and exposure where relevant.
- **Trend**: whether the problem is growing, shrinking, or shifting over the five-year window, and why.
- **Existing efforts**: government, NGO, academic, and corporate initiatives, and what came of them. Hand any company-level detail to the `competitor-landscape` skill.

### 3. Collect open data
Search, in this order:
- the national statistics office, ministries, regulators, and municipal open-data portals for the geography;
- regional and global sources that cover it (for example the World Bank, OECD, UN agencies, IMF, WHO, ILO, Eurostat, and Our World in Data);
- academic repositories and open datasets with a documented method.

For each dataset, record what it measures, its coverage (geography and period), update frequency, definitions, and known limits. Extract the figures that size or explain the problem, with units and periods.

### 4. Scan the news
Search recent news in the local languages and in English: incidents, policy announcements, protests, launches, failures, funding, and expert commentary. Build a dated timeline of the events inside the window that shaped the problem. Separate reported fact from opinion. Confirm any important claim against a second outlet or a primary source.

### 5. Synthesise
For each angle, write what the evidence says, how confident you are, and what it implies for framing the problem. Name the root causes that the evidence supports, and the ones it doesn't. List the open questions that only fieldwork or interviews can answer, and pass them to the `problem-discovery` skill.

## Required outputs
1. Scope block: problem area, geography, population, run date, five-year cutoff, and languages searched.
2. Evidence ledger, one row per claim: claim | value and unit | geography | period | source (title, publisher, URL) | published | accessed | evidence type | confidence | notes.
3. Angle map: findings, confidence, and implications for each angle.
4. Geography profile: the facts about the place that matter for this problem.
5. News timeline of dated events inside the window.
6. Data gaps: what is missing or stale, why it matters, and how to fill it.
7. Research plan for anything you couldn't check, with the exact queries and sources.

## Quality check
Before handing off, make sure that:
- every number in the summary appears in the ledger with a dated source;
- no decision rests on evidence older than the cutoff;
- disagreements between sources are visible rather than averaged away;
- assumptions are labelled;
- the geography in every source matches the problem's geography, or the mismatch is stated.
