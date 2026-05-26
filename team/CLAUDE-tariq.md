# Tariq · Claude Code instructions

> Role-aware addendum to each .NET service repo's own `CLAUDE.md`.
> Lives in scrips-stack so it travels with the skills.
>
> **Reading order each session:**
> 1. The active repo's own `CLAUDE.md` (e.g. `~/scrips-repos/Scrips.Patient/CLAUDE.md`) — stack, build commands, architecture, non-negotiables, code style
> 2. This file — your scope, the 4 primitives, brain-deny rules
> 3. `~/.claude/skills/scrips/playbooks/24-7-engineering.md` — the daily ritual

---

## Who you are

You are a **backend engineer** working across the Scrips .NET microservice fleet. You drive `/be-sprint-runner`, not `/admin-sprint-runner`.

**Your active repo set (June 2026):**

| Repo | What it owns | Port (REST/gRPC) |
|---|---|---|
| `Scrips.Patient` | Patient demographics, encounters, medications, documentation, PHI | 6001 / 5001 |
| `Scrips.Provider` | Practitioner enrollment, credentials, specialities, clinical favourites | 6007 / 5007 |
| `Scrips.Persons` | Person-record cross-cutting (HRN/MRN, shared identity) | varies |
| `Scrips.Billing` | Invoice, claims, payments, accounting integrations | varies |
| `Scrips.PracticeManagement` | Providers, practices, staff, clinical workflows | varies |
| `Scrips.Practice.Aggregator` | Cross-service aggregator (CQRS + MediatR gateway across Patient/Scheduling/Billing/Provider/PracticeMgmt) | varies |
| `Scrips.QuestionBank` | Question bank service | varies |
| `Scrips.Integration.Fhir` | FHIR R4 boundary layer | varies |

Cross-cutting shared libraries you'll touch: `Scrips.Core`, `Scrips.Common`.

Each repo is .NET 8 LTS, Clean Architecture (API / Application / Domain / Infrastructure), EF Core 8, Dapr pub/sub via RabbitMQ, gRPC server + clients, SQL Server.

---

## Your June 2026 mission

Ship backend capability that unblocks the FE streams (Andrew · PM React; Samer's separate FHIR/Person track) and lands one client to UAT by end of June. Concrete sprint shape comes from Jira — pull tickets at the start of each week with `/sprint`.

| Week | Focus (default shape — refine against your Jira board) |
|---|---|
| W1 | Land in `Scrips.Provider` + `Scrips.Patient`. Get the build green locally, run the existing tests, ship one small PR per repo to prove the loop. |
| W2 | Move into `Scrips.Billing` + `Scrips.PracticeManagement`. Touch the aggregator (`Scrips.Practice.Aggregator`) to wire any new cross-service endpoints the FE needs. |
| W3 | `Scrips.QuestionBank` work · FHIR integration touchpoints (`Scrips.Integration.Fhir`). Multi-tenant test coverage on anything PHI-adjacent. |
| W4 | Stabilise, UAT support, fill test gaps in services touched in W1–W3. End of W4 = ≥3 PRs/day average, all merged, no rollback. |

**Cut-line:** If a story can't ship in its sprint without scope creep, slice it. Don't carry across weeks. The shape above is a default — the real backlog is in Jira.

---

## What's out of your stream

- **FE / Flutter / React** — Andrew (PM React) + the Flutter app belong to other tracks. Don't run `npm`/`vite`; you won't need `scrips-react/node_modules`.
- **Aidbox FHIR-native rewrite** — Samer's separate track. `Scrips.Integration.Fhir` is your seam; don't migrate domain entities to FHIR resources unsolicited.
- **DevOps / Azure infra** — `Bash(az:*)`, `Bash(kubectl:*)`, `Bash(terraform:*)` are denied in your settings. Deployment, AKS, Key Vault rotation, etc. are not your domain.
- **Finance · investor · brain** — see deny rules below.

---

## The 4 primitives — when each fires

Full playbook: `~/.claude/skills/scrips/playbooks/24-7-engineering.md`. Short version:

| Primitive | When |
|---|---|
| `/goal` | Once. Initialize your June mission on Day 1 (template on v5 deck slide 03). Wakes itself each weekday 06:00 Asia/Gaza. |
| `git worktrees` | Every parallel task. Spawn under `~/scrips-repos/.worktrees/<repo>-<feature>/`. Clean up after merge. |
| `CronCreate` | Every overnight. Regression sweep at 02:00, Slack DM summary at 06:00. |
| `subagent-driven-development` | Every morning. 3–6 subagents on independent tasks. Harvest at lunch. |
| `/be-sprint-runner` | Sprint execution. Reads Jira stories, codes each against the live BE codebase, runs unit + integration tests, opens PR. |

---

## When to use which sub-agent type

- `Explore` — read-only investigation (find every callsite of a repository method, map a Dapr event flow, trace gRPC contracts). Never use for implementers.
- `Plan` — architectural planning, multi-step strategy. Use before any non-trivial change that crosses two services or touches the aggregator.
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

## Hygiene · daily (BE-specific)

1. **First command every session:** `/using-superpowers`
2. **Branch format:** `feat/PROD-XXXX-<service-shortname>-<short-description>` (e.g. `feat/PROD-1234-patient-encounter-export`)
3. **PR title:** `[PROD-XXXX] <description>`
4. **Reviewer:** Samer (while Andrew is off Tue–next-week); Andrew after that
5. **One ticket per session.** `/clear` between unrelated tasks.
6. **Read the repo's CLAUDE.md before editing it.** Each service has its own non-negotiables (e.g. `Scrips.Patient` PHI logging rules). They override anything generic in this addendum.
7. **Multi-tenant filter is non-negotiable.** Every query must filter by `TenantId`. A missing filter is a PHI-breach bug — block your own PR on it.
8. **PHI in logs = never.** Patient IDs only. No names, DOB, SSN, diagnoses, medications in logs, error messages, or telemetry.
9. **EF Core migrations:** run from the repo root, use the repo's documented project/startup-project pair (each repo's CLAUDE.md spells it out). Commit migration files alongside the code change.
10. **Tests:** every PR adds or updates `tests/<Repo>.UnitTests`. CQRS handlers and repository methods both need coverage.
11. **EOD:** Run `/retro`, push, update `/goal` status, schedule overnight cron.

---

## Calibration · four gates

| When | Signal off-track if … |
|---|---|
| End Day 5 | First PR not open · no worktrees spawned · no `/goal` active |
| End Week 2 | No cross-service work (Patient + Provider + aggregator) shipped · &lt; 2 PRs/day average · no overnight cron live |
| End Week 3 | Tests not added with each PR · TenantId filter audit not run on touched files · pace stuck at 1–2 PRs/day |
| End Week 4 | UAT failed for any service in your set · rollbacks accumulated · scope cut without slice-and-ship discipline |

Calibration calls are 20 min each. Friday EOD.

---

## Recovery rubric

| Symptom | What broke | Fix |
|---|---|---|
| Claude says "task complete" but `dotnet test` fails | Verification skipped | `/verification-before-completion` then demand evidence |
| Path doesn't exist | Hallucinated file | `ls` the parent. Re-ground in real source |
| Subagents return identical output | Sequential call, not parallel | Use one message with multiple Agent tool blocks |
| Stuck in loop on wrong approach | Lost the thread | `/clear` then re-state goal with full context |
| Wrong skill routes | Missing meta-protocol | Re-invoke `/using-superpowers` |
| `/goal` lost continuity | Compaction without summarize | Re-invoke with state from `~/claude-os/daily-activity-log.md` |
| EF migration doesn't apply | Wrong `--project` / `--startup-project` pair | Read the repo's CLAUDE.md "Build and Run" section — each repo has its own pair |
| `dotnet build` fails on a fresh clone | Missing NuGet feed / Azure DevOps creds | Repo's ONBOARDING.md has the auth steps; ping Samer if still stuck after 10 min |

---

## Who to ping

- **Samer · PM + architecture** — product calls, access, architecture decisions, contract lock with FE streams, Aidbox/FHIR boundary questions
- **Andrew · FE owner + ex-BE lead** — questions about Dapr topics, gRPC contracts the FE consumes, deployment patterns · **off Tue this week through next**
- **Claude · the team** — everything else · `/using-superpowers` first

---

## Linked artifacts

- **v5 deck (this onboarding):** `~/claude-os/artifacts/2026-05-25-tariq-onboarding-v5.html`
- **24/7 playbook:** `~/.claude/skills/scrips/playbooks/24-7-engineering.md`
- **Sprint simulator:** `~/.claude/skills/sprint-simulator/SKILL.md`
- **BE sprint runner:** `~/.claude/skills/be-sprint-runner/SKILL.md` (your primary daily driver)
- **Port spec (if you ever do FE-port work):** `~/.claude/skills/port-spec/SKILL.md`
- **Team setup:** `~/.claude/skills/scrips/team-setup.sh`
- **Readiness check:** `~/.claude/skills/scrips/readiness-check.sh`
- **Per-repo CLAUDE.md** — read first in any session: `~/scrips-repos/<Repo>/CLAUDE.md`

---

**Origin:** 2026-05-25 · [CLAUDE] · BE-scope rewrite 2026-05-26 after Samer restated Tariq's scope as backend .NET services (Patient · Provider · Billing · PracticeManagement · QuestionBank · cross-cutting). Sprint-shape weekly table is a scaffold; refine against the Jira backlog at Sprint Planning.
