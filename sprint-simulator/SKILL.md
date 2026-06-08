---
name: sprint-simulator
description: Guided dry-run of a Week-1 sprint using the four 24/7 primitives. Picks a safe real ticket from the practitioner-app backlog, walks the engineer through worktree-isolated subagent dispatch, and scores them on five calibration moments. Use when an engineer just completed v5 onboarding and needs to drill the primitives before touching the real critical path. Invoke as `/sprint-simulator`.
---

# /sprint-simulator — Guided dry-run of a parallel sprint

You are guiding the engineer through their first parallel-subagent sprint. **Your job is to build their muscle memory on the four primitives — `/goal`, worktrees, CronCreate, subagent-driven-development — before they touch the critical-path practitioner rewrite.**

The simulator uses a *real* ticket from their backlog, in a *real* worktree, with *real* code — but on a low-blast-radius task (a UI polish PR or a typo fix expanded into a refactor). If the simulator's PR ships, great. If it doesn't, no scope was lost.

---

## Operating principle

**Drill, then score.** Six steps. Each step takes 15–20 minutes. The whole simulator is ~2 hours.

The engineer is *not* allowed to skip steps. Each step builds muscle memory for the one after.

At the end, you produce a scorecard with five calibration signals. Honest red marks are more useful than false greens. The engineer DMs the scorecard to Samer.

---

## Step 0 — Identify who's drilling + their backlog

Ask:
- Name (likely Tariq, but the skill works for anyone)
- Repo (likely `~/scrips-repos/scrips-react`)
- Picked ticket — they should have one in mind. If not, scan their Jira filter and propose 3 candidates with low blast radius (StatusChip migration sites, Storybook story additions, copy fixes that touch a Signal DS component).

If they haven't onboarded yet (no `readiness-check.sh` run in their session history), **stop**. Send them to `/onboard` first.

---

## Step 1 — Spawn a worktree (15 min)

Drill the worktree primitive on its own.

```bash
cd ~/scrips-repos/scrips-react
git worktree add -b feat/PROD-XXXX-simulator-drill \
  ~/scrips-repos/.worktrees/simulator-drill main
cd ~/scrips-repos/.worktrees/simulator-drill
```

**Verify:**
- `git status` shows the new branch
- `pwd` shows the worktree path
- The main repo is untouched (engineer can still work in it for unrelated tasks)

**Self-check question:** "If you broke this branch right now, what would happen to the main repo?" (Answer: nothing — that's the point.)

---

## Step 2 — Initialize a tactical `/goal` (15 min)

Have them paste a short tactical goal for the simulator itself:

```
/goal Simulator drill: ship one small PR using the 4 primitives before lunch.
Scope: the picked ticket. Out of scope: any unrelated cleanup.
Wake at hourly intervals for the next 4 hours with status.
```

**Verify:**
- `/goal` confirms the goal is active
- They understand this is a *tactical* goal (4 hours), distinct from their *strategic* June `/goal` (4 weeks)

**Self-check question:** "Why is having both a strategic and a tactical goal at the same time fine?" (Answer: they operate at different time horizons. The strategic goal surveys; the tactical drives.)

---

## Step 3 — Morning dispatch · 3 subagents (30 min)

This is the heart of the simulator.

The engineer drafts the dispatch prompt themselves. You critique it before they send.

Required shape:
- **Exactly 3 subagents** (not 1, not 10 — 3 forces tradeoff thinking)
- Each subagent has **no shared state** with the others
- Each subagent is **briefed cold** — assume zero context from this session
- Each subagent has a **measurable done-when**
- Total work fits in a *worktree-of-one* (the simulator-drill worktree)

Example shape they should arrive at:

```
Agent 1 (Explore subagent_type):
  Find every callsite of <three-shade-pill-pattern> in
  src/{billing,scheduling,patients}/. Return: file:line list
  with the exact bg-X-100 text-X-700 patterns found. Under 200 words.

Agent 2 (general-purpose):
  In the worktree at ~/scrips-repos/.worktrees/simulator-drill,
  replace every callsite from Agent 1's output with
  <StatusChip tone="soft" status={...}>. Run vitest after.
  Open a draft PR titled "[PROD-XXXX] StatusChip migration · simulator drill".

Agent 3 (Plan):
  Read the Andrew domain pattern in CLAUDE.md and the StatusChip
  contract in @scripsteam/signal-ds. Return: a 5-line review
  checklist for Agent 2's PR.

Dispatch all 3 in parallel. Return when all 3 complete.
```

**Critique pass — make them fix at least one of these before sending:**
- Is Agent 1's output structured enough for Agent 2 to consume mechanically?
- Does Agent 3's checklist depend on Agent 2's PR existing, or can it run in parallel?
- Are the subagent types correct (Explore is read-only; never use it for the implementer)?

---

## Step 4 — Harvest + merge in order (30 min)

Once the 3 subagents return:

1. **Read all 3 outputs first** — don't act on Agent 1's output before reading Agent 3's checklist
2. **Decide merge order** — usually: read Agent 1's findings, apply Agent 3's checklist to Agent 2's PR
3. **Self-review** with `/review` before requesting Samer's review

**Verify:**
- Engineer can articulate *why* they merged in that order
- Engineer ran `/review` and acted on its findings, not just read them
- Engineer caught at least one issue across the 3 outputs (there's always one)

**Self-check question:** "What would have gone wrong if you'd merged Agent 2's PR before reading Agent 1's full list?" (Answer: probably missed callsites. Agent 2 was told to use Agent 1's output as input — if Agent 1 missed a regex variant, Agent 2 carries it forward.)

---

## Step 5 — Schedule an overnight cron (15 min)

Set up tonight's overnight pass on this branch. Pattern:

```
Schedule a one-time cron at 02:00 (Asia/Gaza) tomorrow that:
1. cd into ~/scrips-repos/.worktrees/simulator-drill
2. git pull (in case main moved)
3. Run npm run lint && vitest run --coverage
4. Capture pass/fail
5. Post a Slack DM to me at 06:00 with the result

Use CronCreate. Name 'simulator-drill-overnight'.
```

**Verify:**
- The cron is actually scheduled (check with `list scheduled tasks`)
- The engineer can articulate how they'd kill it if it ran amok

**Self-check question:** "What's the failure mode if your API key in `~/.anthropic-api-key` is wrong?" (Answer: cron fires, agent fails to start, no DM arrives. Detection = 06:00 silence. Recovery = fix key, manually trigger one run.)

---

## Step 6 — Scorecard (15 min)

You produce the scorecard. Honest red marks > false greens.

```markdown
# Sprint Simulator · Scorecard · Tariq Alardah · 2026-05-25

## Worktree spawned
- [ ] Worktree exists at ~/scrips-repos/.worktrees/simulator-drill
- [ ] On its own branch
- [ ] Main repo untouched
Score: ___ / 3

## Subagent dispatch
- [ ] Exactly 3 subagents dispatched
- [ ] No shared state between them
- [ ] Each briefed cold
- [ ] Each has measurable done-when
- [ ] First-draft dispatch needed at least one critique-driven revision
Score: ___ / 5

## Harvest discipline
- [ ] Read all 3 outputs before acting
- [ ] Merged in defended order
- [ ] /review run before requesting Samer's review
- [ ] Caught at least one cross-agent issue
Score: ___ / 4

## Cron set up
- [ ] CronCreate scheduled for overnight
- [ ] Cron name registered
- [ ] Engineer can articulate kill-switch
Score: ___ / 3

## /goal hygiene
- [ ] Tactical /goal active during the drill
- [ ] Strategic /goal still active (didn't get killed)
- [ ] Engineer can articulate the difference
Score: ___ / 3

## Total: ___ / 18

## Verdict
- 16-18: Ready for the critical path. Start the real practitioner work tomorrow.
- 12-15: Ready with one specific gap to fix. Note the gap, work the real path, calibrate Friday.
- 8-11: Re-drill the failing step before critical path. Don't paper over it.
- 0-7: Foundation gap. Pause and re-read v5 deck + 24/7 playbook. Re-drill tomorrow.

## Notes
[Engineer's own observations]

## Asks of Samer
[What they need from Samer to keep moving]
```

DM the scorecard to Samer. That's the end of the simulator.

---

## When this skill fails — diagnostic

| Symptom | What broke | Fix |
|---|---|---|
| Worktree won't create | Lock file or invalid path | `git worktree prune` then retry |
| `/goal` returns "no active goals" | Skill not invoked or state file missing | Check `~/.claude/state/goals/` exists |
| Subagents return identical output | Not actually parallel — sequential call | Use single message with multiple Agent tool blocks |
| Cron schedules but never fires | API key file empty or wrong | `cat ~/.anthropic-api-key` should be a real key |
| Engineer can't articulate the why | Drilling the *what*, not the *why* | Stop. Re-read the playbook section for the failing primitive. |

---

## What's deliberately not in scope

- Real practitioner-app tickets. The simulator uses a safe ticket so failure doesn't cost.
- New skill creation. The simulator drills existing skills, doesn't add new ones.
- Backend work. Pure frontend / DS-touching tasks for the drill.

If the simulator ends in a real PR that ships, celebrate that as bonus.
If the simulator ends with a thrown-away worktree but a green scorecard, that's the goal.

---

## Linked

- 24/7 playbook: `~/.claude/skills/scrips/playbooks/24-7-engineering.md`
- v5 deck: `~/claude-os/artifacts/2026-05-25-tariq-onboarding-v5.html`
- v4.3 deck (still canonical): `~/claude-os/artifacts/2026-05-19-tariq-onboarding-v4-3.html`
- using-git-worktrees skill: `~/.claude/skills/using-git-worktrees/SKILL.md`
- subagent-driven-development skill: `~/.claude/skills/subagent-driven-development/SKILL.md`
