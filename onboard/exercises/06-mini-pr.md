# Exercise 6 — Mini PR end-to-end

**Time:** 2 hours
**Builds:** Full workflow muscle memory — your first real Claude-driven PR

---

## Goal
Take a small, well-defined ticket from start to merged PR using `/sprint` → `/review` → `/ship`. This is the real workflow. The exercises above were practice. This is the game.

## What to do

### Step 1 — Pick the ticket (10 min)

Open Jira. Find a Settings ticket appropriate for you:
- For Tariq: **PROD-789** (Staff edit polish — photo, country picker, Resend Invite) — small, well-scoped, low-risk
- For backend engineers: pick a corresponding small SND-* refactor ticket
- For full-stack: a feature ticket sized M (1-2 days)

Read the ticket. Read the acceptance criteria. Read any linked Confluence page.

### Step 2 — Branch and session (5 min)

```bash
cd ~/scrips-repos/scrips-react
git checkout main && git pull
git checkout -b feat/PROD-789-staff-edit-polish
claude
```

In Claude:
```
/using-superpowers
```

### Step 3 — Plan with /port-spec or /writing-plans (20 min)

If you're porting (Flutter → React), use:
```
/port-spec
```
Provide the Jira ticket URL. Let Claude run the 5-parallel discovery.

If you're greenfield, use:
```
/writing-plans
```
Give Claude the AC. Let it produce a step-by-step plan.

**STOP and review the plan.** Don't proceed until you can answer:
- Does this match the AC?
- Is the file list right?
- Are dependencies surfaced?
- What's the test plan?

If the plan looks wrong, ask Claude to revise. Iterate until correct.

### Step 4 — Execute with /sprint (60 min)

```
/sprint
```

Hand off the plan. Watch Claude execute:
- Writes the code
- Runs tests
- Self-checkpoints
- Handles failures via /systematic-debugging when needed

You're the director:
- Approve architectural decisions
- Redirect when going off-spec
- Don't type code yourself unless Claude is truly stuck

### Step 5 — Review with /review (15 min)

```
/review
```

Claude self-reviews the diff. Read its findings:
- Signal DS violations?
- TypeScript errors?
- Missing tests?
- Jira link in commit message?

Fix everything Claude flags. Re-review.

### Step 6 — Ship with /ship (10 min)

```
/ship
```

Claude creates the PR:
- Branch named `feat/PROD-789-...`
- Commit message `[PROD-789] ...`
- PR body links the ticket
- Reviewer: Samer

Verify the PR in GitHub. Add any context the AC needs.

### Step 7 — Capture the session

```
/session-capture
```

Or tell Claude: "Capture this session — what we did, what we learned, what's next."

## Success looks like

After 2 hours:

- [ ] PR is open in GitHub
- [ ] PR links the Jira ticket
- [ ] CI is green (or pending)
- [ ] Branch name and commit message follow conventions
- [ ] You can describe what each step did and why
- [ ] You felt the workflow click

## What "felt the workflow click" means

There's a moment in exercise 6 where you stop thinking about which skill to invoke and just... type the natural thing. Claude routes to the right skill automatically because you set up the session with `/using-superpowers`.

When that happens, you're a Claude super-user. The workflow is yours.

## Self-check question

> "Walk me through the workflow from picking up a Jira ticket to opening a PR, listing every skill you'd invoke and what each produces."

Expected answer:
1. `/using-superpowers` — load meta-protocol
2. `/port-spec` or `/writing-plans` — produce spec
3. `/sprint` — execute
4. `/systematic-debugging` — when stuck
5. `/review` — self-audit
6. `/ship` — create PR
7. `/session-capture` — save learnings

If your answer is missing any of these, re-do the exercise. The workflow has to be muscle memory before week 2.

## When you finish

Tell Samer:
> "First PR open: [link]. Exercise 6 complete. Ready for week 2."

Samer will review the PR + verify the gate (see /onboard step 5).

## What's next

Week 2 starts. You're now a contributing engineer at Scrips. The exercises are over.
