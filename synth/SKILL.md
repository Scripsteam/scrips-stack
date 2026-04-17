---
name: synth
description: Synthesizes Jira + Axure + Figma + Confluence + brain into a feature BRD with 6 mandatory sections (personas, journeys, entity state machines, BDD use cases, integration scenarios, acceptance criteria). Runs Stage 02 of the Scrips SDLC pipeline (docs/superpowers/sdlc/PIPELINE.md). Use when starting any new feature or when a Jira epic/stories are thin (field lists only) and need product depth before sprint execution.
---

# synth — Product-source Synthesis Skill

**Announce at start:** "Running synth on feature: `<feature-slug>`."

---

## Outcome Tracking (MANDATORY)

**At start — RECALL:** Before Step 0, invoke `agent-outcome-tracker` RECALL:
- Query `agent_traces` where `agent_skill = 'synth'` AND `feature_slug LIKE '<domain>%'`, last 10 rows
- Recall brain for `"<feature-slug> synthesis BRD sources"`
- Declare in one line: which sources caused failures before, which patterns worked

**At end — CAPTURE:** After Step 3 quality gate passes, invoke `agent-outcome-tracker` CAPTURE:
- `task_type`: `brd-synthesis`
- `agent_skill`: `synth`
- `feature_slug`: the slug
- Score: 5 if all 6 sections complete + all sources found, 3 if any `[SOURCE UNAVAILABLE]`, 1 if quality gate blocked
- `what_worked`: which sources were richest (Figma/Confluence/brain)
- `what_failed`: any source that was unavailable or thin

---

## Why this skill exists

The diagnostic at `docs/superpowers/retros/sprint-rerun-diagnostic.md` (v2) identified the root cause of three sprint reruns: **there is no synthesis layer between product sources and code.** Jira stories carry fields + endpoints + tests. Everything a feature needs — personas, journeys, state machines, cross-page scenarios, error flows — lives in Axure, Figma, Confluence, and the brain. The agent has never synthesized them. This skill does.

A pass of this skill is mandatory before Stage 04 (Story Expansion) and before admin-sprint-runner touches code for the feature.

---

## Inputs

The skill requires a **feature argument** — a slug like `department-management` or `practitioner-association`. From the slug, it expects to locate:

| Source | How to find it |
|---|---|
| **Jira epic + children** | Epic provided by user or searched via `searchJiraIssuesUsingJql`. Children fetched via epic-link JQL. |
| **Axure prototype** | Check `~/scrips-repos/scrips-react/docs/design/axure/` first. If empty, ask user for an Axure URL or local path. Never fabricate. |
| **Figma file** | File key `8YhKao7Q62LXnMnrsVsW3C`. Section identified by feature slug (e.g., "Department Management" section). |
| **Confluence BRDs** | Space: `SCRIPS DEVELOPMENT`. Search via `searchConfluenceUsingCql` with feature keywords. |
| **Brain (open-brain)** | Query via `mcp__open-brain__search_brain` with feature keywords + related entity names. |

If any source is genuinely unavailable (e.g., Axure export not yet produced), do not invent. Mark it `[SOURCE UNAVAILABLE — <reason>]` in the output and continue with what exists. Samer reviews the BRD in Stage 03 and decides whether to block or proceed.

---

## Outputs

1. **Primary:** `~/claude-os/docs/superpowers/sdlc/<feature-slug>/02-brds/<feature-slug>.md` — the BRD with 6 mandatory sections (format below).
2. **Supporting:** `~/claude-os/docs/superpowers/sdlc/<feature-slug>/01-raw-sources/sources.md` — source index (URLs, extract paths, relevance notes). Written first.
3. **Both stages' manifests:** `01-raw-sources/_manifest.md` and `02-brds/_manifest.md` per the PIPELINE.md contract.

---

## Process

### Step 0 — Bootstrap the folder

```
mkdir -p ~/claude-os/docs/superpowers/sdlc/<feature-slug>/{01-raw-sources,02-brds}
```

Write the two `_manifest.md` files with the stage metadata, owner=`synth`, started timestamp, gate `passed: false`.

### Step 1 — Source discovery (Stage 01)

Dispatch **five parallel subagents**, one per source type. Each returns a concise extract — not a full dump. Each agent must explicitly list what it looked at (URLs, nodeIds, file paths) so the parent can trace every BRD claim back to a source.

**Subagent A — Jira**
- Tools: `searchJiraIssuesUsingJql`, `getJiraIssue`.
- Task: Find the epic for the feature. List all children (key, summary, description, status, acceptance criteria). Return a markdown table + full descriptions as an appendix.

**Subagent B — Axure**
- Tools: `Read`, `Glob`, `Grep` (local filesystem); `WebFetch` if a URL is provided.
- Task: Locate Axure exports for the feature. For each screen, extract: screen name, interaction hotspots, transitions to other screens, any annotations. If no Axure export is present, return `[SOURCE UNAVAILABLE — no Axure export in ~/scrips-repos/scrips-react/docs/design/axure/]`.

**Subagent C — Figma**
- Tools: `mcp__claude_ai_Figma__get_metadata`, `get_design_context`, `get_screenshot` on file `8YhKao7Q62LXnMnrsVsW3C`.
- Task: Locate the feature's section in the Figma file. For every frame in that section, return: nodeId, frame name, entity/state it represents, transitions (if annotated), screenshot path. Capture screenshots to `01-raw-sources/figma-screenshots/`.

**Subagent D — Confluence**
- Tools: `searchConfluenceUsingCql`, `getConfluencePage`.
- Task: Search `SCRIPS DEVELOPMENT` space for BRDs matching the feature keywords + entity names. For each hit, return: title, URL, full body text (or relevant excerpt if very long).

**Subagent E — Brain**
- Tools: `mcp__open-brain__search_brain`, `mcp__open-brain__recall_related`.
- Task: Search for memos referencing the feature or its entities (personas, journeys, prior decisions, compliance notes). Return titles + full bodies of top-10 relevant memos.

**Dispatch them in parallel** using one message with five `Agent` tool calls.

When all five return, write `01-raw-sources/sources.md` with one section per source type, plus an index at the top. Mark the stage manifest `passed: true` only if every source has either real content or an explicit `[SOURCE UNAVAILABLE — <reason>]` line. Never mark it passed with silent gaps.

### Step 2 — Synthesis (Stage 02)

Now — serially, not in parallel — synthesize `02-brds/<feature-slug>.md` with these six sections, in this exact order:

#### 1. User personas
Who uses this feature? For each persona: name (role, not individual), goals, pain points, permissions / role in the system, frequency of use, primary journey(s) they care about. Draw personas from brain memos + Confluence. If a role appears only in Jira (e.g., "OrgAdmin") and has no persona memo, generate a minimal persona and tag it `[DRAFT — validate with Samer]`.

#### 2. User journeys
Start-to-goal paths, with intermediate states. Format per journey:

```
### Journey: <name>
Persona: <role>
Trigger: <what starts this journey>
Goal: <what success looks like>

Steps:
1. <action> → <system response / state>
2. ...

Cross-feature touchpoints:
- <other feature> when <condition>
```

Every journey must come from Axure, Figma flow, or Confluence. Journeys invented from Jira alone are forbidden — Jira does not carry journeys.

#### 3. Entity state machines
For every entity this feature touches (e.g., Department, Practitioner, Specialty):

```
### Entity: <name>
States: [Draft, Active, Deactivated, Archived, ...]

Transitions:
- Draft → Active: triggered by <event>, effect <system change>, actor <persona>
- Active → Deactivated: ...

Invariants:
- <rule that must hold regardless of state>
```

State machines must be complete — no dangling states. If a state appears in a transition but has no inbound/outbound transitions listed, flag it `[GAP — transitions not specified in sources]`.

#### 4. Use cases (BDD)
Per use case:

```
### UC-<feature-short>-<nn>: <name>
Actor: <persona>
Preconditions:
- <state / context required>

Main flow (Given / When / Then):
- Given <initial state>
- When <action>
- Then <outcome>
- And <side effect>

Alternate flows:
- AF1: ...
- AF2: ...

Error flows:
- EF1: ...
- EF2: ...

Links:
- Jira story: DEV-XXXX
- Figma frame: nodeId
- Journey: <journey name>
- State transition: <entity: from → to>
```

**Minimum coverage:** Every Jira story in scope must map to at least one use case. Every state transition must appear in at least one use case. Every journey step must appear in at least one use case.

#### 5. Integration scenarios
How this feature affects or depends on other features. Format:

```
### Scenario: <name>
When <change in this feature>
Then <effect in other feature>
Because <product reason>

Example:
- When a department is deactivated
- Then practitioners assigned to it are flagged for reassignment
- Because a practitioner without a department cannot receive appointments
```

Draw from Confluence + brain. If no integration scenarios are present in sources, say so explicitly rather than inventing.

#### 6. Acceptance criteria
Measurable, testable, per use case. Format:

```
### AC for UC-<id>
- [ ] <testable assertion, phrased in user-observable terms>
- [ ] ...

Quality bar: A QA engineer can walk this AC end-to-end in a browser and mark each line pass/fail without ambiguity.
```

Every AC must reference a specific UC. Orphan ACs (not tied to a UC) are forbidden.

### Step 3 — Quality gate

Before marking Stage 02 manifest `passed: true`, verify:

- [ ] All 6 sections present and non-empty
- [ ] Every persona traceable to brain memo, Confluence, or tagged `[DRAFT]`
- [ ] Every journey traceable to Axure / Figma / Confluence (not Jira alone)
- [ ] Every entity state machine has all transitions specified or marked `[GAP]`
- [ ] Every use case has main + ≥1 alternate + ≥1 error flow
- [ ] Every Jira story in scope mapped to ≥1 use case
- [ ] Every use case has ≥1 AC
- [ ] Nothing invented — every factual claim has a traceable source or an explicit `[GAP]` / `[DRAFT]` marker

If any check fails, fix before marking passed. If a check cannot be fixed (genuinely missing source), mark the gap and flag it prominently in the BRD header for Samer's Stage 03 review.

---

## Non-negotiables

1. **No fiction.** This matches the feedback memo `feedback_no_fiction_ports.md`. If a source is missing, say so. Do not invent personas, journeys, states, or scenarios.
2. **Sources > summaries.** Always read the actual source (Figma frame, Confluence page body, Jira description) — not a cached description. If a source was summarized in an earlier step and that summary is all that's available, re-fetch before making claims.
3. **Parallel inside, serial across.** Sources are read in parallel. Synthesis of the 6 BRD sections is serial — each section may reference prior sections.
4. **Gaps are artifacts.** `[GAP — needs X]` is valid BRD content. Blank fields or generic filler are not.
5. **Trace every claim.** Every sentence in the BRD must be supportable by a line in `01-raw-sources/sources.md`. If you cannot find the supporting line, either fix the trace or mark the claim `[GAP]`.
6. **Respect PIPELINE.md.** This skill is Stage 02 of the pipeline. Do not skip Stage 01's `sources.md` — downstream stages depend on it.

---

## When to use this skill

- Starting any new feature in the Scrips SDLC.
- Re-opening a feature whose original sprint produced CRUD shells instead of workflows (e.g., re-running DEV-2270 child features).
- Before any admin sprint touches code for a feature that does not yet have a `02-brds/<feature>.md` file.

## When NOT to use this skill

- Pure code changes / bug fixes that don't introduce new behavior.
- Features already covered by a current, Samer-approved BRD.
- Ops, finance, CFO/bookkeeping work — synth is an engineering-side skill.

---

## Skill dependencies

- Figma Console MCP (for frame reads + screenshots)
- Atlassian MCP (Jira + Confluence)
- open-brain MCP
- Read / Glob / Grep / Write tools (local filesystem)
- Agent tool (for the five parallel subagents in Step 1)

---

## Attribution tag

Work produced by this skill must be tagged `[SKILL: synth]` in any commit or summary that references it.
