---
name: open-loops-ledger
description: "Stops loose ends from dying in conversation. Every commitment, decision, undeployed PR, or unfiled ticket that surfaces mid-session becomes a tracked row with an OWNER and a real TRACKER (Jira/GH PR/GH Issue) — or is explicitly killed with a reason. Fires whenever work is deferred, a decision is made, code is written-but-not-deployed, or a ticket is needed-but-not-filed."
type: procedure
---

# open-loops-ledger — nothing leaves a session as prose-only

**The problem:** as agent velocity rises, the bottleneck isn't generating work — it's that work *gets
lost*. Code that isn't deployed, decisions made in chat and never codified, "I'll do X next" with no
owner and no tracker. It compounds: each session resumes from the last chat line, not the outstanding
debt. This skill makes the debt durable, owned, and surfaced.

**The rule (non-negotiable):** any of these, the moment it appears, becomes a ledger row with an
**owner** + a **real tracker** — or is **killed** with a one-line reason:
- a deferral ("later / next session / once X lands")
- a **decision** that should outlive the chat (architectural → an ADR/DS-NNN, not just a chat line)
- **code written but not deployed** (open PR, branch, staged edit)
- a **ticket needed but not filed**
- a commitment to a person ("I'll send / they'll review")

A row with no owner **and** no tracker is technical debt, not a handoff. Banned closing states:
"will follow up", "TBD", "in a future session" — those are `open` loops; file them.

## The ledger
A markdown table at `<your working repo>/.claude/open-loops.md` (create if missing). The **trackers
are the team's existing systems** — Jira (PROD) for work, GH PRs/Issues for code. The ledger points at
them; it does not replace them. A loop is "tracked" only once it has a Jira/GH ref; until then it's
`blocked` on filing and that filing is the next action.

```
| ID | What | Type | Owner | Tracker | Status | Opened | Next check |
```
Type: `code · decision · ticket · follow-up`. Status: `open · blocked · in-review · done · killed`.

## Procedure
1. **On start** — read the ledger; advance/close anything whose tracker shows resolved.
2. **On every trigger** — append a row. No owner yet? Assigning one IS the next action. No tracker? Filing it IS the next action (status `blocked` until filed).
3. **On a decision** — write the decision into the row; if architectural, the tracker is an ADR/DS-NNN.
4. **On close** — set `done`/`killed` + a one-line resolution. Never delete a row (audit trail).
5. **On end** — flush; report opened/closed/blocked delta.

## What this is NOT
- Not a replacement for Jira/GH — it's the buffer + index that guarantees every loop *reaches* them.
- Not a narrative log of what happened — it's the forward list of what's unresolved.
- Not for trivia — a one-line fix done in the same turn isn't a loop. A loop outlives the turn.

## Anti-patterns
- A wall-of-text "next steps" paragraph instead of ledger rows → the debt is invisible next session.
- Closing a session with an open commitment that has no Jira/GH ref → silent deferral.
- Deleting a resolved row instead of marking it `done` → loses the audit trail.

**Origin:** 2026-06-12 — Samer named the systemic failure of high-velocity agent work: loose ends die
in conversation, no owner, no tracker, no follow-up. This is the standing system that prevents it.
