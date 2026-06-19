# scrips-stack releases

Newest first. Every team-kit change lands here with a plain-language note — what changed, why, and what
you do differently. (The `scrips-stack-release` skill keeps this honest.)

---

## 2026-06-19 — Port protocol: diagnose first (Step 0)

**What changed:** `practitioner-flutter-to-react` now opens with **Step 0 — diagnose first**: before building (or when inheriting an existing port), the agent runs a three-input check — *is the source legible? do the DS bricks exist? is there a frame contract to read?* — and names the gaps before writing any code. If a port already exists, it diffs against the source and labels each drift by cause (source-not-read / missing-brick / no-frame). Also: the skill now defers deep discovery to `port-spec` instead of duplicating it, and marks the Step 0–7 sequence as the canonical one that sibling wrappers (`pm-`/`ua-flutter-to-react`) reference.

**Why:** proven the same day — an agent *told to diagnose first* self-identified a ported screen's wrong-side summary, bare side-rail, and missing Orb before any rework. Baking it in means that doesn't depend on someone remembering to ask.

**What you do differently:** nothing new to install if you already pulled today — `git pull && ./setup` brings the updated skill. For any port, the agent diagnoses before it builds.

**Owner / questions:** Samer.

---

## 2026-06-19 — The parity loop now installs: two gates + the Practitioner port wrapper

**What changed:** three skills join the kit.
- **`design-parity-judge`** — the measured render-vs-source visual gate. It reads the live DOM and scores it against hard gates (no clipping, control-size coherence, real DS color, and **G6 parity-vs-source** for ports). It blocks any "done / at-parity" claim that has no measured gate table — a screenshot proves it rendered, not that it passes.
- **`scrips-verify`** — the unified pre-handback check (always-on integration + security; conditional frontend/backend). Runs before a PR.
- **`practitioner-flutter-to-react`** — a thin Practitioner-App surface wrapper. It carries the PA specifics (source repos `scrips_msp1_pa` / `scrips_msp1_flutter_shared`, target `scrips-practitioner-react`, Signal DS `^1.11.0`) and invokes the generic engines. It does NOT duplicate them — surface facts live in the wrapper, the engines stay generic.

**Why:** a ported Practitioner encounter screen drifted from its Flutter source — patient summary on the wrong side, a bare side-rail, no Orb — and nothing caught it before it reached a review. The reason: `design-parity-judge` and `scrips-verify` existed only on one machine, never in the kit, so the team literally could not run the gate that should have caught it. And there was no PA surface layer, so the generic port engine had no surface facts to anchor on. This closes both holes.

**What you do differently:** re-pull + `./setup` (git-bash on Windows) + restart Claude. Then for any practitioner port, invoke `practitioner-flutter-to-react` — it walks source → contract → frame → parity → verify, and won't let an agent call a port "done" without the measured parity table.
```
git -C ~/scrips-repos/scrips-stack pull && ./setup
```

**Owner / questions:** Samer.

---

## 2026-06-15 — Team telemetry: see how we build (per person · project · task) — re-install required

**What changed:** the harness now ships three lightweight telemetry instruments (installed by `./setup`, no extra steps):
- **The talk** — which sub-agents you dispatch, tagged by the project (repo) you're in.
- **Estimate vs actual** — when a task is created with an estimate and completed with an actual, that becomes a *calibration pair*. The `sprint` and `feature-brief` ceremonies now record this for you automatically — you don't hand-fill anything.
- **Build effort** — token volume per project (measured from your local Claude transcripts).

It rolls up into a **predictability dashboard** in `scrips-telemetry` — sliced by person, project, and task — so we can see where estimates run hot, where effort goes, and get sharper at forecasting. Each runs at session end, ships only to our private `scrips-telemetry` repo, keyed by your git email. Nothing leaves the org.

Two fixes worth naming: estimate↔actual now pair correctly (they keyed on mismatched fields before, so the loop captured nothing), and your identity resolves consistently even if you use a per-repo git email.

**On money:** the dashboard does **not** compute spend — billing $ lives in the **Anthropic Console → Usage** (org-level, accurate). Our telemetry owns predictability + effort, not dollars.

**Why:** we estimate in weeks what lands in hours. The only way that improves is measuring estimate-vs-actual by person, project, and task type and feeding it back — that's predictability, and it was structurally empty until now.

**What you do differently:** **re-pull + `./setup` + restart Claude** — this one needs the restart, because the instruments load when Claude starts. After that it's automatic; just keep using `sprint` / `feature-brief` as normal.
```
git -C ~/scrips-repos/scrips-stack pull && ./setup
```
Then quit and reopen Claude Code. That's it.

**Owner / questions:** Samer. (Heads-up: until everyone re-installs, the dashboard only reflects whoever has — so it'll look light until the team picks this up.)

---

## 2026-06-14 — setup now refreshes skills on Windows (no more silently-stale skills)

**What changed:** `setup` detects whether the platform actually makes symlinks. On Windows Git Bash (no Developer Mode), `ln -s DIR` silently makes a full **copy**, not a link — and the old code then **skipped** any already-installed (non-symlink) skill on re-run. Result: `git pull && ./setup` refreshed hooks/telemetry but **never refreshed skill content** — an updated `SKILL.md` stayed frozen at first-install version. Now, in copy-fallback mode, setup **refresh-copies** every kit skill each run, so content tracks the repo. Also stops the umbrella `~/.claude/skills/scrips` from churning a new `scrips.bak.<ts>` dir on every run.

**Why:** found on Windows when `/feature-brief` kept running #19 after #21 was pulled + `./setup` re-run. 4 skills were silently stale (`feature-brief`, `flutter-parity`, `onboard`, `scrips-stack-release`). Anyone on Windows (no symlink support) was affected — every skill content update since first install had silently not landed.

**What you do differently:** nothing new — `git pull && ./setup` now actually delivers skill updates on Windows. macOS/Linux behavior (symlinks) is unchanged. If you previously hit stale skills, this run fixes them.

**Owner / questions:** Tariq (authored via Claude Code) · Samer.

---

## 2026-06-14 — Feature Brief: trial-validated + polished from the first team run  (PR #21)

**What changed:** `/feature-brief` improved after Andrew's first live run (on the Consent Form Builder):
- The **claim audit now auto-runs** the git/grep and checks **both** what's shipped (`origin/main`) and what's only local — labelling each claim **MERGED / LOCAL-ONLY / ABSENT** — instead of leaving it to discipline.
- Each round **pre-answers** what it can from the ticket/code and only asks the genuinely ambiguous questions.
- The design round **proposes** the Signal DS components for you (and translates the jargon) rather than asking you to name them.
- Two mechanical fixes: the DS-gap step creates the `primitive-needed` label if it's missing; the TOPIC block posts as a Jira **comment**, not a description rewrite.

**Why:** the first run proved the ceremony's worth — its claim audit made the status honest (the consent document-builder / fill-engine / `PdfBoxOverlay` were POC/local-only, not merged; only the consent backend #882 + signing FE #546–557 are on `main`) and caught a platform duplication + a compliance question before any code. Andrew's verdict: "keep it, make it the default gate," plus this polish list. (Even the trial's own audit was nearly fooled by doing the check superficially — hence auto-running it now.)

**What you do differently:** same as before — run `/feature-brief` first on any feature — it's now lower-friction (fewer obvious questions; it proposes the design components) and more trustworthy (the evidence table is run, not recalled). Re-pull + `./setup`.

**Owner / questions:** Samer.

---

## 2026-06-13 — Stage 00 Feature Brief: think across all five dimensions before you build  (PR #19)

**What changed:** new skill **`/feature-brief`** — a "Stage 00" you run the moment you pick up a feature, before brainstorming or writing any code. It walks you through five dimensions in one pass — product, security, development, design, testing — catches conflicts *between* them (e.g. "this shows PHI in a viewer but no access model is defined", or "this re-builds something an ADR already owns"), and writes a structured brief that seeds the rest of the pipeline. It won't pass its own gate until every dimension is answered (or explicitly marked a gap) and no cross-dimensional conflict is left open.

**Why:** the expensive gaps are the ones you don't think to ask about up front — the missing security model that surfaces at review, the DS component that doesn't exist yet found at design time, the "it already exists" that turns out not to. Holding all five lenses in your head at once is genuinely hard; this turns it into a ~10-minute checklist instead of a sprint-three surprise. One rule it enforces hard: any "this already exists / it's merged / the wiring's verified" gets checked against the live repo (`file:line`) before it's written down — no claim becomes fact without evidence.

**What you do differently:** starting a feature? Run **`/feature-brief`** first — paste the Jira (`PROD-XXXX`) link, a Slack thread, or just describe it. Answer the five short rounds. You get a brief + a gate; only then open Stage 01. Re-pull `scrips-stack` and run `./setup` to get the command. (Auto-fire enforcement is Samer-side during this trial; you invoke it manually.)

**Owner / questions:** Samer. First live run: the Consent Form Builder.

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
