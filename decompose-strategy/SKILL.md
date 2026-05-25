---
name: decompose-strategy
description: When a user has a large strategic goal (multi-sprint, multi-bounded-context, multiple unknowns), decompose it into executable phases respecting context window limits, engineer capacity, and dependencies. Use BEFORE writing plans, specs, or tickets when the scope is "rewrite this", "migrate to X", "build the new system", or any goal that would consume more than one sprint.
---

# /decompose-strategy — Strategic goal → executable backlog

You are the planning architect. Your job is to prevent scope explosion by converting ambitious goals into executable units that respect three hard constraints:

1. **Context window** — each unit must fit in one Claude Code session (one bounded context, ≤ 2000 LOC touched, ≤ 5 files in scope)
2. **Engineer capacity** — N engineers × M days, with realistic velocity per engineer
3. **Dependencies** — what blocks what (build order matters, parallel where possible)

## When to invoke

Invoke this skill when you hear:
- "Rewrite the X to Y" / "Migrate from X to Y"
- "Build the new X service"
- "Refactor the X architecture"
- "Modernize the X stack"
- Any goal that names an outcome > one sprint away
- Any goal that touches > one bounded context
- When user says "I keep boiling the ocean" or expresses scope anxiety

If the user just says "build feature X" and X fits in one sprint → use `/writing-plans` instead. This skill is for STRATEGIC goals, not features.

## The protocol — six steps, in order

### 1. Clarify the goal in one sentence

Before doing anything, force the user to state the goal in one sentence. If they can't, the goal isn't ready. Push back:

> "Before I decompose this, give me one sentence: who does what, by when, to what effect? Example: 'Tariq ships the new vertical-SOAP practitioner React app on existing REST API in 4 weeks.' If you can't, the goal isn't decomposable yet — let's brainstorm first via /brainstorming."

### 2. Surface the locked constraints

Ask explicitly (don't infer):
- **Timeline:** weeks, with absolute end-date
- **Team:** names, roles, % availability, what other commitments they have
- **What's fixed (cannot move):** features, dates, quality bars
- **What's flexible (can be cut if slipping):** features, scope, polish
- **Existing assets:** what's already built, what's a fresh build

If any of these are vague, stop and ask. Don't decompose ambiguous inputs.

### 3. Identify bounded contexts

Decompose the goal into bounded contexts. A bounded context is:
- One coherent piece of functionality
- Owned by one engineer (no shared mutation across)
- Fits in one Claude Code session (this is the hard constraint)
- Has a clear "done" criterion that's verifiable in code or by test

Examples for a "rewrite encounter to FHIR" goal:
- BC1: FHIR Encounter resource model + persistence
- BC2: FHIR Questionnaire resource for templates
- BC3: SOAP composer (vertical UI)
- BC4: Sign/lock state machine
- BC5: RAG integration
- BC6: Dapr event publisher rewiring

If a bounded context is too large (won't fit in one session), split it further. "Too large" = > 5 files touched, > 2 days work, or > 1 architectural decision.

### 4. Build the dependency graph

For each bounded context, ask:
- What does this depend on? (must complete before)
- What depends on this? (we're blocking)
- Can this run parallel to anything? (no shared files)

Output as a DAG, even as text:

```
BC1 (Encounter resource) ─┬──→ BC4 (sign/lock)
                          ├──→ BC3 (SOAP UI)
                          └──→ BC6 (events)
BC2 (Questionnaire) ──────→ BC3 (SOAP UI)
BC5 (RAG) — parallel to all of above
```

### 5. Size each unit and sequence into phases

Sizing legend:
- **S** = ½ day (one session, one file, mechanical refactor)
- **M** = 1–2 days (one bounded context, ≤ 5 files)
- **L** = 3–5 days (one bounded context, complex logic)
- **XL** = > 5 days → MUST SPLIT. Never accept XL.

Sequence into phases respecting deps. Each phase = parallel slice of work. Each engineer in each phase has clear ownership.

```
Phase 1 (Week 1):
  Engineer A: BC1 [M], BC2 [M]
  Engineer B: BC5 [L]  (parallel — no dep)

Phase 2 (Week 2):
  Engineer A: BC3 [L]  (waited for BC1+BC2)
  Engineer B: BC4 [M], BC6 [M]
```

### 6. Risk callouts + cut-line

Explicitly state:
- **Top 3 risks** that could blow the plan (technical, capacity, dependency)
- **Cut-line:** if you fall behind by week 2, what do you drop FIRST? Order them.
- **Calibration checkpoint:** when do you re-evaluate? (Usually end of week 1.)

## Output format

Default output: HTML artifact in `~/claude-os/artifacts/<YYYY-MM-DD>-<slug>-decomposition.html` with:
- Goal statement
- Constraints
- Bounded context table
- Dependency graph (CSS/SVG, not prose)
- Phase plan (Gantt-style or table)
- Risk callouts + cut-line
- Calibration checkpoint date

If user explicitly asks for Jira tickets, generate ticket drafts (title + AC + estimate) after the HTML.

## Hard rules

- **Never produce a plan with an XL item.** Split it.
- **Never produce a plan without a cut-line.** Slippage is inevitable; the cut-line forces priority discipline.
- **Never accept "TBD" for capacity.** If unknown, ask. If still unknown, assume worst case (0.3x for new engineers, 0.5x for new-to-codebase, 1.0x for veterans).
- **Never decompose without surfacing locked constraints first.** Decomposition without constraints = fiction.
- **Always flag if the goal as stated cannot fit the timeline.** Don't pretend it fits. Surface the gap and ask which constraint moves.

## Anti-patterns to catch

If you find yourself doing any of these, stop:

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| One big bucket called "build the new system" | No bounded context = no executable | Force the user to enumerate BC1...BCn |
| Linear plan with no parallelism | Wastes capacity | Find independent BCs and parallelize |
| Optimistic sizes ("it's just a port") | Velocity reality vs aspiration | Multiply by engineer-velocity factor |
| Plans that ignore the unknown unknowns | Discovery work isn't tracked | Add a "spike" phase before commit |
| "Stretch goals" that are actually critical | Real critical path hidden | Forbid stretch — everything is in or cut |

## Example invocations

- "I want to rewrite the encounter service to FHIR-native by end of Q3."
- "We need to port the practitioner app to React in 1 month with one engineer."
- "Migrate the design system from Tailwind utility classes to Signal DS components across 50 screens."
- "Decompose the Scrips.Encounter buildout per the strangler-fig plan."

For each: clarify → constraints → bounded contexts → deps → phases → risks. Output HTML.

## What success looks like

A successful decomposition produces a plan where:
- Every line item is sized S/M/L (no XL)
- Each engineer has a clear day-by-day path
- Dependencies are explicit
- The cut-line is named
- The team can start tomorrow without further planning

If the user reads the output and says "I know exactly what to do Monday" — you succeeded. If they say "this is great but how do I start?" — you failed. Try again.
