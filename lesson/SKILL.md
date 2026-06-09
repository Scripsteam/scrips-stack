---
name: lesson
description: Capture a durable engineering lesson into the team's shared memory (LESSONS.md) and open a PR. Use after a PR merges, a bug is root-caused, an incident is resolved, or a code review surfaces a pattern worth not relearning. The point is a self-improving team memory that doesn't depend on manually debriefing anyone.
---

# /lesson — capture a lesson into shared memory

The team's hard-won knowledge must live in `scrips-stack/LESSONS.md`, not in one
person's head. This skill turns a moment of "we just learned something" into a
durable, sourced entry that every engineer's Claude reads on day one — so the
system gets better on its own instead of depending on debriefing a senior dev.

## When to fire (proactively)

- A PR just merged that encodes a non-obvious decision or pattern.
- A bug/incident was root-caused (capture the root cause + the guard).
- A code review surfaced a recurring mistake.
- You hit a wall that the next person will also hit (auth quirk, build gotcha, deploy step).
- The user says "lesson", "capture this", "we shouldn't relearn this", "add to lessons".

If a lesson is really a one-off with no future bearing, don't capture it. The bar
is: *will this save the next engineer (or agent) from breaking something?*

## What to do

1. **State the lesson in one line** — the rule. Imperative, falsifiable.
2. **Why** — one sentence. The cost it prevents.
3. **How to apply** — the concrete action next time.
4. **Source** — the PR number, ticket, incident, or decision that proves it. A
   lesson without provenance is an opinion; cite the `Scripsteam/<repo> #NNN` or
   `PROD-XXXX` or the dated incident.
5. **Verify it's not already there** — grep `LESSONS.md` for the topic; if a
   related entry exists, sharpen it instead of duplicating.
6. **Place it under the right section** (Repos/Deploy/Backend/Frontend/Process) —
   append to that section, keep the format identical to the surrounding entries.
7. **Open a PR** (don't push to main directly): branch `chore/lesson-<slug>`,
   commit `[lessons] <one-line rule>`, PR titled the same, body = the why +
   source. Tag the relevant reviewer.

## Format (match exactly)

```
- **<The rule, bold>.** <Why, one sentence.> <How to apply.> (Source:
  `Scripsteam/<repo> #NNN` / PROD-XXXX / dated incident.)
```

## Output

Confirm the entry added, the section it landed in, and the PR link. If the lesson
generalizes a kernel fact (a repo purpose, a token value, a convention), also flag
that `CLAUDE.md` may need the same correction — drift in one usually means drift
in the other.

## Why this exists

Lessons that live only in chat or in a senior engineer's memory don't compound —
every new hire re-learns them by breaking something, and the team can't scale
faster than the senior can debrief. A sourced, append-only `LESSONS.md` that every
agent loads turns each mistake into permanent team capability. That's the
feedback loop: work → lesson → shared memory → the next engineer starts ahead.
