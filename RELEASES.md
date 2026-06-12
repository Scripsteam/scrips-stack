# scrips-stack releases

Newest first. Every team-kit change lands here with a plain-language note — what changed, why, and what
you do differently. (The `scrips-stack-release` skill keeps this honest.)

---

## 2026-06-12 — Retroactive note: Team Agent Observability (telemetry)  (shipped ~2026-06-10, commit 361eec5; documented now)

> Backfilled — this shipped before the release-discipline rule existed, so it never got a release note or a team post. Recording it now and educating the team.

**What it is:** team agent observability. Three instruments install with the harness (`./setup`) and write to `~/.claude/telemetry/events.jsonl`, keyed by your git email:
- `agent-track.py` (PreToolUse:Agent) — "the talk": agent dispatches (type, volume).
- `task-gate.py` (TaskCreate/Update) — estimate vs actual.
- session-end `push.sh` — union-merges your events into the shared `scrips-telemetry` repo at `telemetry/<you>/events.jsonl` (per-dev, clobber-proof).
- OTEL token/$ budget — opt-in, needs a collector endpoint (until then: "no data", honestly).

**What it captures (and what it does NOT):** per dispatch — agent type, a **160-char task description**, and the **prompt _length_** (`prompt_chars`, a number) + estimate-vs-actual. It does **not** capture your code, file contents, or full prompts. Velocity/calibration metadata, not surveillance.

**Why:** see across *every* engineer's agent use — estimate accuracy, drift, dispatch volume — aggregated to a team digest, so we calibrate how we work with agents.

**What you do differently:** re-pull `scrips-stack` and re-run `./setup` to activate it. Your data only flows once you install — inherent to observing your own machine. Until then the sink only has Samer's data.

**Owner / questions:** Samer. Status + design: `scrips-telemetry/OBSERVABILITY.md`.

---

## 2026-06-12 — Open-loops discipline + release discipline  (PR #12)

**What changed:**
- `open-loops-ledger` — new skill. Stops loose ends dying in conversation.
- `scrips-stack-release` — new skill. The rule that produced this very note: no team-kit change ships without a release note + team education + acknowledgement.

**Why:** as we lean harder on agents, the bottleneck isn't generating work — it's *losing* it. Code that isn't deployed, decisions made in chat and never written down, "I'll do X next" with no owner and no tracker. It compounds. These two skills make the debt durable, owned, and visible.

**What you do differently:**
- When you (or your agent) defer something, make a decision, leave a PR open, or need a ticket you haven't filed → it becomes a row in `.claude/open-loops.md` with an **owner** and a **real tracker** (Jira/GH), or it's killed with a reason. Never a vague "next steps" paragraph.
- When you change anything in `scrips-stack` → you write a release note here + a friendly team post + ask everyone to acknowledge.

**Owner / questions:** Samer (rule owner) · this update authored via Claude Code.
