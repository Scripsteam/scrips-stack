# Scrips Engineering · team Claude Code addendum

> Symmetric role-aware addendum to the canonical `dev-scrips-pm-react/CLAUDE.md`.
> Lives in scrips-stack so both engineers read the same doc, same primitives, same expectations — but with parallel sections specifying each owner's stream.
>
> **The principle:** Scrips moves by combining best thinking. Engineers are evaluated as individuals; the company ships by team performance. This doc keeps Andrew + Tariq symmetric on tooling and discipline, asymmetric only on stream ownership.
>
> **Reading order each session:**
> 1. `~/scrips-repos/scrips-react/CLAUDE.md` — canonical PM-stream doc (stack, conventions, Signal DS rules, two-store rule)
> 2. This file — both stream scopes, the 4 primitives, brain-deny rules
> 3. `~/.claude/skills/scrips/playbooks/24-7-engineering.md` — the daily ritual

---

## Both of you · same baseline

Same repo. Same primitives. Same calibration. Same brain-deny rules. Same one-PR-per-session hygiene. Same Friday EOD retro pace.

Your **only asymmetry** is the stream you own. Everything else is shared discipline.

| | Andrew | Tariq |
|---|---|---|
| Stream | Practice Management | Practitioner |
| Routes | `/scheduling/*` · `/patients/*` · `/billing/*` · `/org/*` · `/settings/*` | `/practitioner/*` |
| Code root | `src/scheduling/` · `src/patients/` · `src/billing/` · `src/org/` | `src/practitioner/` (create if absent) |
| Backend lead-or-consume | Lead — owns Studio admin UI, ambient deploy, API behaviour | Consume — uses Andrew's components, calls existing endpoints |
| Calibration owner | Samer + Tariq cross-review at W2 contract lock | Samer · Friday weekly |

**Compose, never copy.** If your stream needs a component the other owns, import it. Recreating duplicates is the worst failure mode — caught in PR review, sent back every time.

---

## June mission · 7 streams · 4 weeks · 3 humans

| Stream | Owner | W1 | W2 | W3 | W4 |
|---|---|---|---|---|---|
| Practitioner rewrite | **Tariq** | EncounterInbox + FrameEncounter shell | Templates engine · S+O blocks | A+P blocks · sign-lock | UAT w/ one client |
| Template Studio (build) | **Andrew** | Scaffold admin UI · author CRUD | Publish API · specialty filters | Consumed by Tariq | UAT alongside |
| Workflow Studio | shared | Elsa designer kept · React list+run | Activity catalog · run panel | cut-line if needed | cut-line |
| Care Pathway | shared | Prototype → production-path | EHR tab integration (PROD-654) | Architecture tab build | cut-line |
| Rule Engine | **Andrew** | Coding edits page · JSON editor | Test runner · synthetic payloads | Hardening | cut-line |
| CRM (sprint 1+2) | **Andrew** | Entity · list | Communications · notifications | Segments · campaigns | QA + handoff |
| Stock management | **Andrew** | defer W2 | Inventory list · movements | Reorder rules · supplier | QA + handoff |

**Cut-line:** Ambient defers to Phase 2 if not deployed by end of W3. Wearables UI defers first. **Cross-stream contract lock:** end of W2 · `EncounterTemplate` shape — joint Andrew + Tariq decision, Samer sign-off.

---

## What's out of either stream

- **Person / Patient FHIR rewrite** — Samer's separate track. `Scrips.Persons` exists; HRN/MRN spec is PRM/3271720978.
- **`Scrips.Encounter` FHIR-native service** — Phase 2, post-UAT. Aidbox licensed dev + prod. Build seam at `EncounterTemplate.fhirBindings` so swap is mechanical.
- **Existing UAE clients** — legacy stays. Clean slate for new clients only. No data migration.
- **Andrew's residual Settings sprint** — PROD-762 / 764 / 787 / 788 / 790 stay with Andrew but treated as background fill-in, not displacement of CRM / Stock / Rule Engine.

---

## The 4 primitives — when each fires (shared)

Full playbook: `~/.claude/skills/scrips/playbooks/24-7-engineering.md`. Both of you run the same daily shape.

| Primitive | When |
|---|---|
| `/goal` | Once per sprint mission. Initialize on Day 1. Wakes itself every weekday 06:00 with status + ask + risk. |
| `git worktrees` | Every parallel task. Spawn under `~/scrips-repos/.worktrees/<stream>-<feature>/`. Clean up after merge. |
| `CronCreate` | Every overnight. Regression sweep at 02:00, Slack DM summary at 06:00. |
| `subagent-driven-development` | Every morning. 3–6 subagents on independent tasks. Harvest at lunch. |

---

## Sub-agent type selector (shared)

- `Explore` — read-only investigation (find every callsite, map a module). Never use for implementers.
- `Plan` — architectural planning, multi-step strategy. Use before any non-trivial implementation.
- `general-purpose` — actual implementation. Always in a worktree.

---

## Brain · finance · investor — not your context

Denied at the MCP layer in your `~/.claude/settings.local.json` (team-setup.sh writes the deny rules). Same denied list for both:

- `mcp__open-brain__*` — Samer's vault
- `mcp__*__quickbooks*` — finance
- `mcp__*__attio*` — Samer's ops CRM (the Scrips product CRM is a different thing)
- `mcp__*__fireflies*` — meeting transcripts often carry investor / personal context
- `mcp__*__outlook_email*` — Samer's mail
- `Bash(az:*)` / `Bash(kubectl:*)` / `Bash(terraform:*)` — infra ops
- Confluence spaces COS / FIN / BOARD / INVESTOR — Confluence-side ACL
- Obsidian vault — never registered

If you ever hit a permission error on something **engineering-shaped**, ping Samer — that's a bug, not policy.

---

## Hygiene · daily (shared)

1. **First command every session:** `/using-superpowers`
2. **Branch format:** `feat/PROD-XXXX-<stream>-<short-description>` (Andrew uses `pm-*`, Tariq uses `practitioner-*`)
3. **PR title:** `[PROD-XXXX] <description>` · link the corresponding Idea in Scrips Roadmap (SR) project
4. **Reviewer cross-pattern:** PM-stream PRs → Tariq reviews UI surface, Samer reviews architecture. Practitioner-stream PRs → Andrew reviews contract surface (Studio + Questionnaire), Samer reviews architecture.
5. **One ticket per session.** `/clear` between unrelated tasks.
6. **Compose, never copy.** Mount the other stream's components. Recreating is a review-block.
7. **Two-store rule:** Zustand UI state only. TanStack Query server state only. Never mix.
8. **FHIR seam:** Build with `fhirBindings: null` so Phase 2 swap is mechanical.
9. **EOD:** Run `/retro`, push, update `/goal` status, schedule overnight cron.

---

## Cross-team rituals (new in v5)

| When | What | Who |
|---|---|---|
| Monday 09:00 (after Andrew is back) | Joint planning sprint · 90 min | Andrew + Tariq + Samer |
| Daily 06:00 | `/goal` morning surface | Each engineer's own |
| Wednesday EOD | Mid-sprint check · async DM | Engineer → Samer |
| Friday EOD | Calibration call (per stream) · 20 min | Engineer + Samer |
| Friday EOD | Cross-stream sync · 30 min | Andrew + Tariq + Samer |
| Sprint end | Retro · 60 min · jointly | All three |

**The cross-stream sync at Friday EOD is non-optional.** It's where contract decisions, learnings, and Monday's dispatch shape get aligned. Don't ship it as "we'll catch up async" — sync time builds the shared model.

---

## Calibration · four gates · same shape for both

| When | Signal off-track if … |
|---|---|
| End Day 5 | First PR not open · no worktrees spawned · no `/goal` active |
| End Week 2 | Architecture deferred to Samer · &lt; 3 PRs/day average · no overnight cron live · contract not locked |
| End Week 3 | Stream deliverable not on track · pace stuck · subagents underused |
| End Week 4 | UAT failed (Tariq) / scope cut below demo (either) · sign-off not captured |

20 min each. Friday EOD. The Friday cross-stream sync runs **after** individual calibrations so both have just landed feedback.

---

## Recovery rubric (shared)

| Symptom | What broke | Fix |
|---|---|---|
| Claude says "task complete" but tests fail | Verification skipped | `/verification-before-completion` then demand evidence |
| Path doesn't exist | Hallucinated file | `ls` the parent. Re-ground in real source |
| Subagents return identical output | Sequential call, not parallel | Use one message with multiple Agent tool blocks |
| Stuck in loop on wrong approach | Lost the thread | `/clear` then re-state goal with full context |
| Wrong skill routes | Missing meta-protocol | Re-invoke `/using-superpowers` |
| `/goal` lost continuity | Compaction without summarize | Re-invoke with state from `~/claude-os/daily-activity-log.md` |
| Cross-stream conflict on a shared file | Two streams hit one file | Surface in the Friday cross-stream sync — never silently force-push |

---

## Who to ping (shared)

- **Samer · PM + architecture** — product calls, access, architecture decisions, contract sign-off
- **Andrew · Backend + PM stream owner** — Studio admin UI, ambient deployment, API behaviour, PM-stream questions
- **Tariq · Practitioner stream owner** — encounter shell, vertical SOAP, template render, Questionnaire consumption
- **Claude · the team** — everything else · `/using-superpowers` first

---

## What "team performance" means here

You will be evaluated individually on your stream delivery. **The company moves by combining your thinking.** That means:

- Both of you read the same docs (this one, the playbook, the v5 deck)
- Both of you join the Friday cross-stream sync
- Both of you take Monday planning together
- Both of you have the same access scope (engineering only — brain / finance / investor stay out of both)
- The 4 primitives are the same for both — no "Tariq dispatches subagents, Andrew doesn't"
- If one of you discovers a sharper pattern, it lands in this doc within a week — don't hoard

If something asymmetric emerges that isn't stream-ownership-driven, **flag it as a bug to Samer**, not a fact.

---

## Linked artifacts

- **v5 deck (team):** `~/claude-os/artifacts/2026-05-25-tariq-onboarding-v5.html` (currently Tariq-framed; symmetric v5.1 landing in this PR)
- **v4.3 deck (Tariq canonical · still applies):** `~/claude-os/artifacts/2026-05-19-tariq-onboarding-v4-3.html`
- **24/7 playbook:** `~/.claude/skills/scrips/playbooks/24-7-engineering.md`
- **Sprint simulator:** `~/.claude/skills/sprint-simulator/SKILL.md`
- **Team setup:** `~/.claude/skills/scrips/team-setup.sh`
- **Readiness check:** `~/.claude/skills/scrips/readiness-check.sh`
- **Upgrade plan (Samer's view):** `~/claude-os/artifacts/2026-05-25-andrew-tariq-claude-upgrade-plan.html`
- **Scrips Roadmap (Jira SR · Discovery):** https://scrips.atlassian.net/jira/polaris/projects/SR/ideas
- **Confluence PRD pattern:** `/wiki/spaces/ENG/` (PRD-004 most recent · 2026-05-09)

---

**Origin:** 2026-05-25 · [CLAUDE] · status-draft pending Samer sign-off. Supersedes the Tariq-only `tariq/CLAUDE-tariq.md` shipped earlier today in this same PR.
