# 24/7 Engineering Playbook

> How to use Claude Code as a multiplier, not a typewriter. The four primitives
> that turn one engineer into a team. Built for the June 2026 sprint —
> practitioner rewrite + Template Studio + Workflow Studio + Care Pathway +
> Rule Engine + CRM + Stock.

---

## The shape of the day (after this playbook is muscle memory)

```
08:00  Morning dispatch          → spawn 3-6 subagents into worktrees, each on a tight task
09:00  Synchronous review        → review last night's overnight diffs + PRs
10:00  Decision work             → architecture calls, spec lock-in, contract decisions
12:00  Subagent harvest          → review what the 3-6 subagents produced, merge in order
14:00  Synchronous build         → the work that needs you in the loop
17:00  Overnight cron schedule   → set tonight's regression / scaffolding / refactor pass
18:00  EOD wrap                  → /retro, push, /goal status update
```

Engineer-hours per day: 8. Claude-hours per day: 20+. **Multiplier comes from the gap.**

---

## Primitive 1 — `/goal` · the long-running mission

`/goal` holds a multi-day or multi-week objective across sessions. It owns its own
wake-up cadence, summarizes itself across context compactions, and surfaces blockers
to you each morning instead of waiting silently.

### When to use

- Any goal that spans more than one /sprint session (your June practitioner rewrite, all of Andrew's CRM sprint 1+2)
- Anything where you want a recurring "where are we" without typing the prompt yourself
- Long-running migrations (Flutter→React port modules)

### Initialization

```
/goal Ship vertical-SOAP practitioner app to UAT sign-off by Friday Week 4 of June.
Scope: EncounterInbox, FrameEncounter, S+O+A+P blocks, dynamic templates,
sign-lock workflow. Out of scope: ambient, wearables, FHIR rewrite.
Andrew owns Template Studio; you consume via Questionnaire contract.
Wake every weekday 06:00 local with status + ask + risk.
```

### What it does

- Self-pacing — sets its own wake-up via `ScheduleWakeup` (dynamic mode)
- Cross-session — survives `/clear`, survives context compaction
- Auto-surfaces blockers each wake-up rather than waiting for you to ask

### Anti-patterns

- ✗ One `/goal` per ticket — wrong granularity. /goal is for the *sprint mission*.
- ✗ Vague goals like "improve performance" — needs a measurable done-when
- ✗ Goals without a wake cadence — they go dormant and you forget

---

## Primitive 2 — Git worktrees · parallel without collision

Each subagent gets its own branch + filesystem checkout under
`~/scrips-repos/.worktrees/`. Five agents editing five branches simultaneously,
zero merge conflicts.

### Setup (run once, team-setup.sh does this)

```bash
mkdir -p ~/scrips-repos/.worktrees
echo "*" > ~/scrips-repos/.worktrees/.gitignore
```

### Spawn a worktree for a parallel task

```bash
cd ~/scrips-repos/scrips-react
git worktree add -b feat/PROD-XXXX-soap-objective-block \
  ~/scrips-repos/.worktrees/scrips-react-objective-block main
```

### From inside Claude Code

The `using-git-worktrees` skill knows the discipline. Tell Claude:

> "Spawn a worktree off main for feat/PROD-XXXX. Implement the objective block per `~/claude-os/docs/scheduling-ai-spec/...`. Push when tests green."

### Clean up after merge

```bash
git worktree remove ~/scrips-repos/.worktrees/scrips-react-objective-block
git branch -d feat/PROD-XXXX-soap-objective-block
```

### Anti-patterns

- ✗ Spawning a worktree inside another worktree — git breaks
- ✗ Worktrees on OneDrive — sync conflicts will corrupt git state
- ✗ Forgetting to clean up — leaves dozens of orphan branches in `git branch`

---

## Primitive 3 — `CronCreate` · overnight work

Schedule an agent to run while you sleep. Regression sweeps, lint passes,
scaffold-of-next-day, draft PRs that are ready to review with coffee.

### When to use

- Code-review pass on all in-flight worktrees (run at 02:00, Slack summary by 06:00)
- Regression sweep — run `vitest`, Storybook smoke test, type-check across N branches
- Day-N+1 scaffolding — given today's merged PR, scaffold the next ticket's components

### Template (paste into Claude)

```
Schedule a daily 02:00 (Asia/Dubai) agent that:
1. Pulls latest main
2. For each open worktree under ~/scrips-repos/.worktrees/:
   a. cd into it
   b. Run /review
   c. Run npm run lint && vitest run --coverage
   d. Capture pass/fail + diff stats
3. Post a single Slack DM to me at 06:00 with summary:
   - branches reviewed: N
   - tests passing: X/Y
   - new findings: list
   - draft PRs opened: list of URLs
```

### Anti-patterns

- ✗ Letting overnight agents merge to main — review-required, never auto-merge
- ✗ Overnight tasks that need decisions — they'll wait silently
- ✗ Forgetting to cancel — old crons fire forever; review monthly

---

## Primitive 4 — `subagent-driven-development` · N parallel implementers

You're the orchestrator. Spawn N sub-Claudes via the `Agent` tool, each briefed cold,
each returning a tight summary. You synthesize. This is the morning ritual.

### When it's right

- Tasks have **no shared state** — agents don't need each other's output
- Each task fits in one agent's context window
- You can review N diffs in less time than building one yourself

### When it's wrong

- Sequential dependencies — Agent B needs Agent A's PR merged first
- Same file edits — two agents on the same file = merge conflict
- Exploration — single thread is better when you don't know the shape yet

### Morning dispatch template

```
I'm dispatching 4 subagents this morning. Each gets its own worktree.

Agent 1 (Explore subagent_type):
  Find every Flutter widget under encounter_module/objective that maps to a React
  block. Return: list of widgets, their state shape, their API calls. Under 300 words.

Agent 2 (general-purpose):
  In a fresh worktree off main, implement the Objective block per
  ~/claude-os/docs/scheduling-ai-spec/blocks/objective.md. TDD. Push when green.

Agent 3 (general-purpose):
  Same as Agent 2 but for the Subjective block, in its own worktree.

Agent 4 (Plan):
  Read the Template engine contract end-to-end. Draft the implementation plan
  for the dynamic Questionnaire render. Return: spec + risks. Under 500 words.

Send all 4 in parallel. Return when all 4 complete.
```

---

## Worked examples drawn from the June backlog

### Example 1 — Tariq · Practitioner rewrite Week 1

**Mission:** Mount Andrew's scheduling + patients components under practitioner routes. First PR EOD Friday.

```
Morning dispatch (08:30):

Agent 1 (Explore): Map every route in src/scheduling/ + src/patients/ in scrips-react.
  Return: which need wrapping in PractitionerLayout, which are direct mounts.

Agent 2 (general-purpose, worktree): Mount /practitioner/schedule and
  /practitioner/patients routes. Use existing components, no copies.

Agent 3 (Plan): Read CLAUDE.md + flutter-to-react SKILL. Draft port-spec for
  EncounterInbox component from Flutter. Return: spec + missing-data list.

11:00 you review Agent 1's map, approve Agent 2's diff, refine Agent 3's spec.
14:00 spawn Agent 4 with refined spec → implement EncounterInbox.
17:00 schedule overnight: regression sweep + scaffold FrameEncounter for tomorrow.
```

### Example 2 — Andrew · CRM sprint 1

**Mission:** Patient engagement entity + list + communications service in one sprint.

```
Morning dispatch:

Agent 1 (worktree feat/PROD-XXXX-crm-entity): EF Core entity + migration
  + repository. No service layer yet.

Agent 2 (worktree feat/PROD-YYYY-crm-list): Frontend list page using StatusChip,
  pagination, search. Calls a mocked GET /api/CRM/engagements endpoint.

Agent 3 (worktree feat/PROD-ZZZZ-crm-communications): Communications service
  scaffold — send-via-Slack adapter, send-via-email adapter. Strategy pattern.

Lunch: review 3 diffs, merge Agent 1 first, Agent 2 against Agent 1's endpoint,
Agent 3 last with Agent 1's entity as the recipient.
```

### Example 3 — Andrew · Template Studio scaffold

```
Agent 1 (Explore): Read all 8 endpoints on TemplateController. Map to React routes
  the Studio admin UI needs. Return: route table + missing endpoint candidates.

Agent 2 (worktree): Scaffold /studio/templates list + edit pages with Signal DS,
  read-only initially. RHF + Zod schema mirrors the entity.

17:00 overnight cron: run Storybook a11y audit on all Studio components,
  open issues for any axe violations.
```

### Example 4 — Care Pathway · EHR tab integration

Pattern: `/sprint` with explicit "use ADR-PROTO-008 R2 as the canonical contract"
brief; Claude reads the MADR; spawns one Agent for the React tab + one for the
Aidbox query path. Single PR.

### Example 5 — Rule Engine · coding edits page

Andrew's existing `samer/rules-controller-harden` branch (commit 9934f08).
Spawn one Agent in that worktree to: (a) add JSON expression editor, (b) wire
test runner against synthetic encounter payloads, (c) write Storybook story.
PR open by EOD.

### Example 6 — Stock management · entity + movements

Two-agent parallel: entity + list page. Same shape as CRM Example 2.
The reorder rules + supplier link in Week 3 will need a third agent for the
strategy pattern (different fulfillment paths).

### Example 7 — Workflow Studio · Elsa integration list

Existing Elsa designer stays. Wrap with React `WorkflowsList.tsx` +
`WorkflowRunPanel.tsx`. One agent, one PR. The shape is already mapped in
the Protocol Studio Migration Brief — read it first.

### Example 8 — Cross-stream contract lock

End of Week 2: Tariq + Andrew must lock the `EncounterTemplate` shape.
Spawn one Agent: read both repos, propose the contract as a TypeScript type +
matching .NET DTO, return for human review. No code yet, just the contract.

### Example 9 — Overnight regression after a merge

```
Trigger: any PR merged to main on scrips-react.
Cron: 30 min after merge, spawn Agent in fresh clone of main.
Run: vitest, Storybook smoke, type-check.
On failure: open issue + Slack DM.
On success: silent (no notification noise).
```

### Example 10 — Friday EOD goal-status

```
/goal status

Returns: this week's commits/merges, remaining backlog vs sprint plan,
new risks, ask of you for Monday.
```

---

## Hygiene checklist · weekly

- [ ] Clean up worktrees: `git worktree list` — should have ≤ 5 active
- [ ] Audit crons: `claude` → list scheduled tasks — kill any that should have completed
- [ ] Review `/goal` status — is it still the right shape, or has scope drifted?
- [ ] Skim `~/.claude/projects/.../memory/` — any feedback memories that should be promoted to CLAUDE.md?

---

## The recovery rubric · when this all goes sideways

| Symptom | What broke | Fix |
|---|---|---|
| 5 worktrees in conflict | Same-file edits across agents | Spawn one merge-orchestrator agent in a 6th worktree |
| Overnight cron fired but nothing in Slack | API key expired or Slack scope dropped | Check `~/.anthropic-api-key`, restart Claude |
| `/goal` lost its through-line | Context compaction without summarize | Re-invoke `/goal` with fresh state from `~/claude-os/daily-activity-log.md` |
| Subagent confidently reports done, tests fail | Verification skipped | Re-dispatch with `/verification-before-completion` in the brief |
| Worktree won't delete (busy) | Lock file in worktree dir | `git worktree prune --force` then `rm -rf` the dir |

---

## When you've internalized this

You'll know it's working when:

1. Your morning is reading + deciding, not typing
2. Your night ends with `/retro` + cron schedule, not a half-finished PR
3. Your week ends with N merged PRs where N ≥ 3× what you did pre-playbook
4. You're never the bottleneck on parallel work

If any of those isn't true by end of Week 1, ping Samer in the calibration gate.

---

**Linked:**

- `using-git-worktrees` skill — `~/.claude/skills/using-git-worktrees/SKILL.md`
- `subagent-driven-development` skill — `~/.claude/skills/subagent-driven-development/SKILL.md`
- `dispatching-parallel-agents` skill — `~/.claude/skills/dispatching-parallel-agents/SKILL.md`
- `decompose-strategy` skill — `~/.claude/skills/decompose-strategy/SKILL.md`
- v5 onboarding deck — `~/claude-os/artifacts/team-onboarding-v5/`
- Plan: `~/claude-os/artifacts/2026-05-25-andrew-tariq-claude-upgrade-plan.html`
