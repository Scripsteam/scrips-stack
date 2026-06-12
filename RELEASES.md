# scrips-stack releases

Newest first. Every team-kit change lands here with a plain-language note — what changed, why, and what
you do differently. (The `scrips-stack-release` skill keeps this honest.)

---

## 2026-06-12 — Agent Kit hub on Confluence + release notes mirror

**What changed:** created the org-knowledge hub "🤖 Scrips Agent Operating System — Team Kit" on Confluence (space DOC, under Platform & Infrastructure) — Release Log, Skills Catalog (all 50 skills), Plugins & Agentic Code, and Onboarding/Drills/Quizzes. Extended `scrips-stack-release` to mirror every future release note to the Confluence Release Log, and linked the hub from `/onboard`.

**Why:** release notes + the skills/plugins/agentic-code inventory need to live in durable org knowledge and feed onboarding, not just in the repo.

**What you do differently:** new engineers skim the hub + take the knowledge check during onboarding; kit changes now auto-mirror their note to Confluence (no extra step for you).

**Owner / questions:** Samer. Hub: DOC page 4354932738.

---

## 2026-06-12 — Telemetry attributes to the right person (effective git email)

**What changed:**
- The three telemetry instruments (`agent-track.py`, `task-gate.py`, `push.sh`) now key events on your **effective** git email (`git config user.email` — local > `includeIf` > global) instead of `git config --global user.email`.

**Why:** anyone whose scrips identity is set *per-directory* via `includeIf` (not globally) was being logged under their **personal global email** — so events landed in the sink under a stranger's key and fragmented the team digest. Caught on Tariq's machine: 28 events stamped a personal hotmail address instead of `tariq@scrips.com`. The instruments forced `--global`, which deliberately bypasses the very `includeIf` that gives you your scrips identity. If you use `includeIf` (likely Andrew too), this affected you.

**What you do differently:**
- Re-run `./setup` (or `bash harness/install-harness.sh`) to pick up the fixed instruments — on Windows the install is a dir copy, so the re-run is required.
- If you already generated events under a personal email, relabel the `dev` field in `~/.claude/telemetry/events.jsonl` to your scrips email before they push to the sink.

**Still open (not fixed here):** the central sink repo (`scrips-telemetry`) must exist and be cloned to `~/scrips-repos/scrips-telemetry` for `push.sh` to deliver — otherwise it exits "sink repo missing". Confirm repo name + access with Samer.

**Owner / questions:** Tariq (authored via Claude Code) · Samer (telemetry owner).

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

---

## 2026-06-11 — Flutter→React port + Claude Design brief  (PRs #9, #11)

> Backfilled. These shipped *after* the team's 2026-06-08 onboarding, so they weren't part of it.

**What changed:**
- `flutter-style-port` + `flutter-parity` — porting a Flutter screen to React with Signal-DS color + typography governance and parity checks.
- `claude-design-master-brief` — the standing brief that grounds Claude Design work.

**Why:** the PA Flutter→React port needs the colors/type to come from Signal DS, not be re-invented per screen.

**What you do differently:** mostly Tariq (port work) — when porting a Flutter surface, the routing kernel invokes these; nothing to memorize.

---

## Before 2026-06-12 — already covered, not re-documented here

The core engineering kit — `ship` · `review` · `sprint` · `qa` · `investigate` · `brief` · `retro` · `onboard` + the `methodology/` skills (TDD, systematic-debugging, writing-plans, verification-before-completion, git-worktrees, …) — was distributed 2026-06-08 (PRs #2–#6) and is **taught in the `/onboard` 48-hour arc** the team already completed. The routing kernel (`CLAUDE.md`) auto-invokes them from plain language, so they need no separate release note. This log starts tracking *new* changes from 2026-06-12; it deliberately does not re-teach what onboarding already covered.
