# Tariq · Claude Code instructions

> ⚠️ **SCOPE PIVOT — 2026-05-26** ⚠️
>
> Samer restated Tariq's scope on 2026-05-26: **backend .NET services** —
> `Scrips.Patient`, `Scrips.Provider` (practitioner service), `Scrips.Billing`,
> `Scrips.PracticeManagement` / `Scrips.Practice.Aggregator`, `Scrips.QuestionBank`,
> plus other BE services as the sprint dictates.
>
> The body below (FE practitioner-stream in `dev-scrips-pm-react`) is **SUPERSEDED**
> and pending Samer's rewrite. Until then:
> - Use `/be-sprint-runner` not `admin-sprint-runner` for sprint execution
> - Repo root is `~/scrips-repos/Scrips.<Service>/`, not `~/scrips-repos/scrips-react/`
> - Tooling expectations: `dotnet` (.NET 8 SDK), `dotnet ef`, NuGet — not `npm`/`vite`
> - The 4 primitives (`/goal`, worktrees, `CronCreate`, subagent-driven dev) still apply
> - Brain-deny rules (below) still apply
>
> ---
>
> Role-aware addendum to canonical engineer CLAUDE conventions.
> Lives in scrips-stack so it travels with the skills.
>
> **Reading order each session (post-pivot):**
> 1. The .NET service repo's `CLAUDE.md` if present (stack, EF conventions)
> 2. This file — scope, the 4 primitives, brain-deny rules
> 3. `~/.claude/skills/scrips/playbooks/24-7-engineering.md` — the daily ritual

---

## Who you are in this repo

You are the **practitioner-stream owner** inside `dev-scrips-pm-react`.

- Andrew owns the **Practice Management** stream — Scheduling, Patients, Billing, Org admin
- You own the **Practitioner** stream — the vertical SOAP encounter, dynamic templates, sign-lock
- Both streams ship from the same repo. Different routes, different folder roots.
- Your routes: `/practitioner/*`. Your code root: `src/practitioner/` (create if absent)
- You may mount Andrew's components from `src/{scheduling,patients,billing}/` under practitioner routes — **never copy them**. Import + compose.

---

## Your June mission

Ship vertical-SOAP practitioner app to UAT sign-off with one existing client by **Friday Week 4 of June**.

| Week | Deliverable |
|---|---|
| W1 | EncounterInbox + FrameEncounter shell mounted under `/practitioner/encounters/` |
| W2 | Templates engine resolves dynamic Questionnaire for one specialty · S + O blocks |
| W3 | P1 multi-specialty templates verified for 2 specialties · O block PE complete |
| W4 | A + P blocks · sign-lock workflow · UAT with one client signed off |

**Cut-line:** Ambient (PROD-541 epic) defers to Phase 2 if not deployed by end of W3. Wearables UI defers first.

---

## What's out of your stream

- **Person / Patient FHIR rewrite** — Samer's separate track. `Scrips.Persons` exists; HRN/MRN spec is PRM/3271720978. Not your sprint.
- **`Scrips.Encounter` FHIR-native service** — Phase 2, post-UAT. Aidbox licensed dev + prod. Build seam at `EncounterTemplate.fhirBindings` so swap is mechanical.
- **Studio admin UI** — Andrew owns. You consume via the Questionnaire contract. Contract lock end of W2.
- **Existing UAE clients** — legacy stays. Clean slate for new clients only. No data migration.
- **Andrew's residual Settings sprint** — PROD-762 / 764 / 787 / 788 / 790 stay with Andrew. Don't dilute focus.

---

## The 4 primitives — when each fires

Full playbook: `~/.claude/skills/scrips/playbooks/24-7-engineering.md`. Short version:

| Primitive | When |
|---|---|
| `/goal` | Once. Initialize your June mission on Day 1 (template on v5 deck slide 03). Wakes itself each weekday 06:00 Asia/Gaza. |
| `git worktrees` | Every parallel task. Spawn under `~/scrips-repos/.worktrees/practitioner-<feature>/`. Clean up after merge. |
| `CronCreate` | Every overnight. Regression sweep at 02:00, Slack DM summary at 06:00. |
| `subagent-driven-development` | Every morning. 3–6 subagents on independent tasks. Harvest at lunch. |

---

## When to use which sub-agent type

- `Explore` — read-only investigation (find every callsite, map a module). Never use for implementers.
- `Plan` — architectural planning, multi-step strategy. Use before any non-trivial implementation.
- `general-purpose` — actual implementation. Always in a worktree.

---

## Brain · finance · investor — not your context

These tools are denied in your `~/.claude/settings.local.json` (team-setup.sh writes the deny rules). If you ever hit a permission error on something **engineering-shaped**, ping Samer — that's a bug, not policy. If you hit it on something below, it's working as intended:

- `mcp__open-brain__*` — Samer's vault
- `mcp__*__quickbooks*` — finance
- `mcp__*__attio*` — Samer's ops CRM (the Scrips product CRM is a different thing)
- `mcp__*__fireflies*` — meeting transcripts with investor / personal context
- `mcp__*__outlook_email*` — Samer's mail
- `Bash(az:*)` / `Bash(kubectl:*)` / `Bash(terraform:*)` — infra ops
- Confluence spaces COS / FIN / BOARD / INVESTOR — Confluence-side ACL
- Obsidian vault — never registered as an MCP for you

---

## Hygiene · daily

Per Andrew's CLAUDE.md, plus practitioner-specific:

1. **First command every session:** `/using-superpowers`
2. **Branch format:** `feat/PROD-XXXX-practitioner-<short-description>`
3. **PR title:** `[PROD-XXXX] <description>`
4. **Reviewer:** Samer (while Andrew is off Tue–next-week); Andrew after that
5. **One ticket per session.** `/clear` between unrelated tasks.
6. **Mount, don't copy.** If a Signal DS component exists for what you need, import it. Never recreate.
7. **Two-store rule** (from Andrew's CLAUDE.md): Zustand UI state only. TanStack Query server state only. Never mix.
8. **FHIR seam:** Build with `fhirBindings: null` so Phase 2 swap is mechanical.
9. **EOD:** Run `/retro`, push, update `/goal` status, schedule overnight cron.

---

## Calibration · four gates

| When | Signal off-track if … |
|---|---|
| End Day 5 | First PR not open · no worktrees spawned · no `/goal` active |
| End Week 2 | Architecture deferred to Samer · &lt; 3 PRs/day average · no overnight cron live |
| End Week 3 | Templates not rendering · 2 specialties not covered · pace stuck at 1–2 PRs/day |
| End Week 4 | UAT failed · scope cut below the demo · client sign-off not captured |

Calibration calls are 20 min each. Friday EOD.

---

## Recovery rubric

| Symptom | What broke | Fix |
|---|---|---|
| Claude says "task complete" but tests fail | Verification skipped | `/verification-before-completion` then demand evidence |
| Path doesn't exist | Hallucinated file | `ls` the parent. Re-ground in real source |
| Subagents return identical output | Sequential call, not parallel | Use one message with multiple Agent tool blocks |
| Stuck in loop on wrong approach | Lost the thread | `/clear` then re-state goal with full context |
| Wrong skill routes | Missing meta-protocol | Re-invoke `/using-superpowers` |
| `/goal` lost continuity | Compaction without summarize | Re-invoke with state from `~/claude-os/daily-activity-log.md` |

---

## Who to ping

- **Samer · PM + architecture** — product calls, access, architecture decisions, contract lock with Andrew
- **Andrew · Backend + PM stream owner** — Studio admin UI, ambient deployment, API behavior · **off Tue this week through next**
- **Claude · the team** — everything else · `/using-superpowers` first

---

## Linked artifacts

- **v5 deck (this onboarding):** `~/claude-os/artifacts/2026-05-25-tariq-onboarding-v5.html`
- **v4.3 deck (still canonical):** `~/claude-os/artifacts/2026-05-19-tariq-onboarding-v4-3.html`
- **24/7 playbook:** `~/.claude/skills/scrips/playbooks/24-7-engineering.md`
- **Sprint simulator:** `~/.claude/skills/sprint-simulator/SKILL.md`
- **Team setup:** `~/.claude/skills/scrips/team-setup.sh`
- **Readiness check:** `~/.claude/skills/scrips/readiness-check.sh`
- **Upgrade plan (Samer's view):** `~/claude-os/artifacts/2026-05-25-andrew-tariq-claude-upgrade-plan.html`
- **Andrew's canonical CLAUDE.md:** `~/scrips-repos/scrips-react/CLAUDE.md`
- **Scrips Agentic OS project hub** (you don't have access; for reference only): the upgrade you're using is step 12 of the build order

---

**Origin:** 2026-05-25 · [CLAUDE] · status-draft pending Samer sign-off.
