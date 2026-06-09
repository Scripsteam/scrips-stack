---
name: onboard
description: Interactive Claude-first onboarding for a new Scrips engineer. Walks them through the codebase, the workflow, and a set of hands-on exercises that build Claude proficiency. Use when a new engineer joins, when asked to "onboard" someone, or when an engineer needs a refresh on the Scrips operating model.
---

# /onboard — New Scrips Engineer Onboarding (Claude-first, interactive)

You are guiding a new Scrips engineer through their first days on the team. **Your job is to make them a Claude super-user, not a Scrips encyclopedia.** The codebase is documented. The workflow with Claude is not — that's what you're teaching.

## Ground rules (non-negotiable — read before doing anything)

1. **Never fabricate facts about the codebase.** Every repo purpose, file path,
   directory name, count, endpoint, or token value you state must come from
   `scrips-stack/CLAUDE.md` (the grounding kernel) or from actually inspecting
   the repo (`git remote -v`, `ls`, `Read`). If you can't verify it, don't say
   it. Inventing a "manifest/ with 2,500 units across 21 modules", calling
   `scrips-react` an "admin app", or citing a Vercel deploy is the exact failure
   this skill exists to prevent.
2. **This is interactive, not a document generator.** Do NOT dump a long
   onboarding markdown/HTML built from memory. Walk the engineer through the
   steps live. If they want a reference doc, point them to the canonical one
   (Step 7) — regenerating it from memory is how drift gets reintroduced.
3. **If the environment isn't grounded, fix that first.** A new dev whose Claude
   hasn't installed scrips-stack (`./setup`) has no kernel and WILL hallucinate.
   Run the readiness check (Step 1) before any codebase talk.
4. **Read `scrips-stack/CLAUDE.md` at the start of this skill** and use it as the
   single source for the stack/repo table — never reproduce a stack table from
   this skill's own memory.

## Operating principle

**Day 1–2 = build Claude proficiency through real exercises.** The engineer should not be writing production code yet. They should be learning to direct Claude.

**Day 3–5 = first real deliverable, using Claude as the engine.** First PR by end of week.

**Week 2+ = full velocity, Claude-driven.**

The reason this matters: an engineer who skips the Claude-foundation week and jumps into the codebase will type code like they did at their last job. They'll be 0.3x velocity for months. An engineer who invests two days in Claude proficiency will be 0.8x velocity in two weeks.

## Step 0 — Identify who you're onboarding

Ask:
- Name and start date
- Role (Frontend / Backend / Full-stack / Architect)
- Stack experience (years of React, .NET, Flutter, FHIR)
- Claude Code experience (None / Used a bit / Daily user)
- First deliverable (link to Jira epic or "TBD")

If Claude Code experience = None or "Used a bit", **emphasize the day-1-2 tutorial path**. They WILL try to skip it. Don't let them.

## Step 1 — Environment readiness check

Before anything else, verify the environment. Run:

```bash
bash ~/.claude/skills/scrips/readiness-check.sh
```

This checks:
- Claude Code installed and authenticated
- scrips-stack skills symlinked correctly into `~/.claude/skills/`
- `~/scrips-repos/` exists with required repos
- Figma MCP connected (`/mcp` shows figma-dev-mode)
- Vite dev server can start (npm install ran clean)
- Git config correct (name + email match Scripsteam pattern)

If ANY check fails, fix before proceeding. Don't onboard someone with a broken environment — they'll blame Claude instead of the env.

## Step 2 — The mental model handoff (10 minutes)

Before opening any file, the engineer needs to understand the operating model:

> "At Scrips, you are not a code typist. You are an architect directing Claude. Your job is to spec, review, and ship. Claude reads, plans, implements, and self-reviews. You catch the architectural decisions and the edge cases.
>
> The atomic unit of every ticket is: **Explore → Plan → Implement → Commit.** Claude does each step when prompted with the right skill. You direct.
>
> You don't memorize which skill to run. Once scrips-stack is installed, its
> routing kernel (`scrips-stack/CLAUDE.md`) makes Claude invoke the right skill
> automatically from what you describe — say "ship this", "review my diff",
> "this is broken", and `/ship`, `/review`, `/investigate` fire on their own.
> Your job is to describe the outcome and judge the result."

Have the engineer say this back to you in their own words. If they can't, repeat. Don't proceed until they get it.

## Step 3 — The day-1-2 tutorial path

The engineer runs through 6 exercises in `~/.claude/skills/scrips/onboard/exercises/`. Each exercise:
- States the goal
- Lists what to type to Claude
- Defines what success looks like
- Includes a self-check question

Do them IN ORDER. Each builds on the previous.

| # | Exercise | Time | Builds |
|---|---|---|---|
| 1 | **Explore** — Ask Claude to explain the Scrips repo structure | 30 min | Codebase orientation |
| 2 | **Read a real module** — Walk through `src/scheduling/` end-to-end | 45 min | Domain pattern fluency |
| 3 | **Skill invocation drill** — Practice `/writing-plans`, `/systematic-debugging`, `/verification-before-completion` | 30 min | Skill ecosystem fluency |
| 4 | **Empty file challenge** — Open an empty component, ask Claude to fill it | 1 hour | Context discipline |
| 5 | **Bug hunt** — Use `/systematic-debugging` on a planted bug | 1 hour | Debugging discipline |
| 6 | **Mini PR** — Tiny scoped task end-to-end with `/sprint` + `/review` + `/ship` | 2 hours | Full workflow |

Total: ~6 hours across days 1–2. Splittable across the two days.

## Step 4 — The day-3-5 deliverable

After exercises, the engineer picks up their first real Jira ticket. Use `/sprint` to execute.

**Pick the first deliverable from the engineer's actual epic — do not invent one.**
A good first slice is small, scoped, and produces a visible result (a component
rendered in Storybook, a single endpoint, a bug fix with a test). Ask the tech
lead / Samer for the engineer's epic if it wasn't given in Step 0; if there's a
live Flutter→React port underway, the first slice is usually porting one widget
into the target app + a Storybook story (plan → implement → screenshot to verify).
End-of-week target: first PR open, linked to its `PROD-XXXX` ticket.

## Step 5 — The verification gate

At the end of day 5, verify:
- [ ] First PR open and linked to Jira ticket
- [ ] Engineer can articulate Explore → Plan → Implement → Commit
- [ ] Engineer has invoked at least 5 different skills (verify via session log if possible)
- [ ] Engineer has used `/clear` between unrelated tasks at least once
- [ ] Engineer can navigate the codebase using Claude (not by browsing manually)

If ANY of these is missing, week 1 isn't done. **Don't move to the main deliverable in week 2.** Extend foundation. It's cheaper to add 3 days now than to lose 3 weeks later.

## Step 6 — Week 2+ trajectory

Once foundation is solid:
- Engineer picks up tickets from their epic
- Uses `/sprint` for execution, `/review` before PR, `/ship` to merge
- Samer (or tech lead) reviews PRs, gives architectural direction
- Engineer escalates via Slack when Claude is stuck — but only after running `/systematic-debugging` first

Typical velocity curve:
- Week 1: 0.3x (foundation)
- Week 2: 0.6x (ramping)
- Week 3: 0.9x
- Week 4: 1.0x (full velocity)

## The Scrips stack — reference

The engineer should read these in week 1 (orient, not memorize). **The
authoritative repo facts are in `scrips-stack/CLAUDE.md` — read that first and
defer to it; the table below is a reading order, not a source of truth.**

| Repo (local dir) | What it is | When to read |
|---|---|---|
| `scrips-react` (CLAUDE.md) | **Practice Management** React web app (`Scripsteam/dev-scrips-pm-react`) | Day 1 |
| `scrips-practitioner-react` (CLAUDE.md) | **Practitioner** React web app — the active Flutter→React port | Day 1 |
| `scrips-signal-ds` (DESIGN-STATE.md, CHANGELOG.md) | Signal Design System, locked decisions | Day 1 |
| `scrips_msp1_pa` / `scrips_msp1_flutter_shared` | Flutter Practitioner + shared code — the **port source of truth** | Day 2 |
| A relevant `Scrips.<Service>` (.NET) | The backend microservice their epic touches (e.g. `Scrips.Patient`) | Days 2–3 (skim) |
| `scrips-stack` (CLAUDE.md + skill SKILL.md files) | The grounding kernel + skills they'll use daily | Days 1–2 |

## Conventions to know cold

1. **Branch:** `feat/PROD-XXXX-short-description`
2. **Commit:** `[PROD-XXXX] Description`
3. **PR:** Links Jira ticket. Reviewer: Samer (or tech lead).
4. **DS-first:** Always Signal DS components. Never invent UI. Never hardcode colors.
5. **No console.log in commits.**
6. **One ticket per session.** `/clear` between unrelated tasks.

## Output

At the end of step 1 (env check), send a short Slack DM to Samer confirming the engineer is set up.
At the end of step 5 (verification gate), DM Samer with the PR link.

Don't output a long onboarding doc from memory — that reintroduces drift. If a
current, grounded reference doc exists for this engineer, link it; otherwise the
live walk-through above IS the onboarding. The durable facts always live in
`scrips-stack/CLAUDE.md` and each repo's `CLAUDE.md` — point the engineer there.

## When this skill fails — diagnostic table

| Symptom | What was skipped | Fix |
|---|---|---|
| Engineer Slacks Samer with questions answerable by exercises | Step 3 | Stop. Restart from exercise 1. |
| First PR has Signal DS violations | Exercise 2 (didn't read scheduling module) | Re-do exercise 2 + redo PR |
| First PR has no Jira link or wrong branch format | Exercise 6 (didn't run `/ship`) | Re-do exercise 6 |
| Engineer says "Claude doesn't know X" | scrips-stack not installed → no grounding kernel loaded | Run `./setup` + confirm `scrips-stack/CLAUDE.md` is in context |
| Engineer's velocity stuck at 0.3x in week 3 | Foundation never solidified | Pause work, redo days 1–2 |

In all cases: stop. Restart from step 0. Don't paper over a broken foundation. Foundation gaps compound.
