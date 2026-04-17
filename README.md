# scrips-stack

AI workflow skills for the Scrips engineering team. Built for Claude Code.

Each skill is a slash command that gives Claude Code the full context of your stack — your Jira project, your Signal DS tokens, your Flutter/React/(.NET) conventions, your sprint rhythm — so you don't have to re-explain it every session.

---

## What is this?

scrips-stack is a collection of SKILL.md files. Each file is a set of instructions that Claude Code loads when you type a slash command. No binaries, no dependencies, no build step. Just Markdown that carries Scrips's context.

Inspired by [gstack](https://github.com/garrytan/gstack) (Garry Tan, MIT). scrips-stack is independently built for Scrips's stack, team, and product cycles.

---

## Install (30 seconds)

```bash
git clone --depth 1 https://github.com/Scripsteam/scrips-stack.git ~/.claude/skills/scrips
cd ~/.claude/skills/scrips && ./setup
```

That's it. The skills are now available in any Claude Code session.

**Add routing to a specific repo** (so Claude auto-invokes the right skill without you typing it):

```bash
cd ~/your-scrips-repo
cat ~/.claude/skills/scrips/CLAUDE.md >> CLAUDE.md
git add CLAUDE.md && git commit -m "chore: add scrips-stack skill routing"
```

**Update to latest:**

```bash
cd ~/.claude/skills/scrips && git pull
```

---

## Skills

### `/ship` — Create a PR

Creates a pull request with full Scrips conventions: correct branch name format, Jira ticket linked, commit message format, reviewer assigned.

**Use when:** you're ready to ship a feature or fix and want a clean, traceable PR.

**Example:**
```
/ship
```
Claude will check your branch name, validate commit messages, push, and create the PR with the full template — Jira link, test plan, checklist, and `Scripsteam/eng` as reviewer.

**What it enforces:**
- Branch format: `feat/DEV-XXXX-short-description`
- Commit format: `[DEV-XXXX] Description`
- PR title: `[DEV-XXXX] Feature description`
- No direct pushes to `main` or `develop`
- No PR without a Jira ticket

---

### `/review` — Code Review

Reviews your diff against Scrips standards. Gives you file:line findings with severity levels and specific fixes.

**Use when:** you want a code review before requesting one from a teammate, or as a self-review before shipping.

**Example:**
```
/review
```

**What it checks by layer:**

| Layer | Key checks |
|-------|-----------|
| React / TypeScript | Signal DS component usage, DS token compliance, no `any` types, loading/error/empty states |
| Flutter / Dart | `const` constructors, no business logic in `setState`, accessibility, proper image loading |
| .NET C# | REST conventions, `[Authorize]` on all endpoints, no raw SQL, `ProblemDetails` error format |
| Database | No raw SQL, EF Core for queries, reversible migrations, no data leakage across tenants |
| Signal DS | CSS variables, Storybook story for new components, accessibility |

**Severity levels:** BLOCKER · HIGH · MEDIUM · POLISH

**Output format:**
```
[HIGH] AppointmentController.cs:47 — Missing [Authorize] attribute.
  Current: [HttpGet("appointments")]
  Fix:     [Authorize] [HttpGet("appointments")]
  Why: Any unauthenticated user can list all appointments.
```

---

### `/investigate` — Debug

Root-causes issues in any part of the Scrips stack. Systematic: classify the layer, gather evidence, form ranked hypotheses, verify before fixing.

**Use when:** something is broken, throwing errors, or behaving unexpectedly.

**Example:**
```
/investigate the 500 error on the appointments endpoint after yesterday's deploy
```

**Stack coverage:**
- .NET API — null refs, 401/403, slow EF queries, migration failures
- Flutter — lifecycle bugs, null operators, navigation crashes, async gaps
- Database — EF migration issues, column changes, access control gaps, N+1 queries
- React Admin — stale closures, bad useEffect deps, API auth headers, DS mismatches

**Output:** root cause at file:line, fix, and one-sentence prevention note.

---

### `/sprint` — Sprint Ceremonies

Runs sprint ceremonies from Jira data. Covers planning, demo prep, and mid-sprint health checks.

**Use when:** starting a sprint, preparing for a demo, or checking if you're on track.

**Examples:**
```
/sprint planning
/sprint demo prep
/sprint review
```

**Planning output:** proposed sprint backlog with points, a sprint goal, stories NOT included and why, and any stories that aren't ready (missing AC, missing estimate, blocked).

**Demo output:** a full demo script with exact steps for each story — context, what changed, how to show it.

**Review output:** burn-down status, what's blocked and for how long, what's at risk, and specific recommendations if you're behind.

---

### `/design-sync` — Figma → Signal DS

Implements Figma designs using Signal DS. Reads the Figma file first, maps every element to a DS component, flags anything not in the DS before writing a line of code.

**Use when:** building a new screen or component from Figma, or checking if an implementation matches the design.

**Example:**
```
/design-sync the appointment booking screen from Figma
```

**What it does:**
1. Fetches the Figma design (via Figma MCP)
2. Audits DS coverage — lists which DS components to use, flags any gaps
3. Audits tokens — maps every color, spacing, and typography value to a DS token, flags any deviations
4. Implements using Signal DS components and CSS module variables
5. Takes screenshots of the result to compare against the design
6. Reports: components used, gaps flagged, token deviations

**Signal DS tokens it enforces:**

| Token | Value | Use |
|-------|-------|-----|
| Primary blue | `#0076F8` | CTAs, active states, links |
| Dark text | `#151B20` | Body text, headings |
| Background | `#F7F9FA` | Page background |
| Surface | `#FFFFFF` | Cards, panels |
| Border | `#EFEEEE` | Dividers, card borders |
| Muted | `#809099` | Secondary text, labels |
| Error | `#CD3232` | Errors, destructive |
| Warning | `#E5A000` | Warnings, alerts |
| Success | `#41AE55` | Confirmations |

---

### `/qa` — QA Testing

Tests a feature against its acceptance criteria. Starts a local dev server, takes screenshots, walks interactions, checks DS compliance, and produces a pass/fail report.

**Use when:** verifying a feature is complete, checking staging before a release, or testing a specific user flow.

**Example:**
```
/qa DEV-2270 on staging
/qa the appointment filter feature
```

**What it tests:**
1. Takes a baseline screenshot — first impression pass/fail
2. Walks every acceptance criterion from the Jira story
3. Audits Signal DS compliance on every visible element
4. Tests interactions — click, fill, submit — and captures state changes
5. Checks responsive layout at 375px (mobile) and 1280px (desktop)
6. Navigates to adjacent pages to check for regressions

**Output:** a QA report with per-criterion pass/fail, screenshots, DS violations, and a final verdict (READY · MERGE WITH NOTES · BLOCK).

---

### `/brief` — Morning Brief

Pulls Jira sprint status, open PRs, blockers, and synthesizes today's priorities.

**Use when:** starting your day, running a standup, or asking "what should I work on."

**Example:**
```
/brief
```

**Output:**
```
## Scrips Morning Brief — Thursday, April 17

Sprint 4 Status — Day 8 of 10 | 34 points done / 45 committed (76%)
Status: AT RISK

In Progress
- DEV-2270 [Andrew] — Department management UI — day 4

Blocked
- DEV-2301 — API contract not finalized — 2 days — ACTION NEEDED

Open PRs
- [DEV-2270] Admin department CRUD (#142) — awaiting review since Tuesday

Today's priorities
1. Unblock DEV-2301 — agree on API contract with Andrew this morning
2. Review PR #142 — it's been waiting 2 days
3. DEV-2289 if time allows — stretch goal for sprint
```

---

### `/retro` — Sprint Retrospective

Sprint retro from real data. What shipped, what didn't (and the honest reason why), what broke, what was learned. Commitments that are specific enough to actually change behavior.

**Use when:** the sprint ends, or you want a mid-sprint health check.

**Example:**
```
/retro
```

**What it refuses to do:** vague commitments ("communicate better"), inflated velocity, or sanitized post-mortems. If the sprint went badly, the retro says so.

---

### `/cso` — Security Audit

OWASP Top 10 + STRIDE threat model for the Scrips stack. Every finding has a file:line, an impact description, and a fix.

**Use when:** before a major release, when adding auth or data features, or any time you want a security check.

**Example:**
```
/cso
/cso the new patient data endpoint
```

**Coverage:**
- Database access control — every endpoint authorized, no cross-tenant leakage
- .NET `[Authorize]` — every non-public endpoint
- JWT expiry and refresh token rotation
- Flutter — deep link validation, `flutter_secure_storage`, no keys in source
- React — no `dangerouslySetInnerHTML` with user input, no secrets in localStorage
- STRIDE threat model for new features

**Severity levels:** CRITICAL (block the PR) · HIGH · MEDIUM · LOW

---

### `/checkpoint` — Save Progress

Writes a resumable context file so you can pick up exactly where you left off in a future session.

**Use when:** wrapping up mid-task, context window is getting full, or you know you'll need to continue later.

**Example:**
```
/checkpoint
```

**Output:** a dated file at `~/.claude/projects/scrips/checkpoints/` with what was in progress, where things stand, the next steps, and any open decisions. On resume, Claude reads it and picks up without re-explaining.

---

### `/onboard` — New Developer Onboarding

Generates a full onboarding guide for a new engineer or contractor: repo map, access checklist, stack conventions, first-day tasks — tailored to their role.

**Use when:** a new developer joins the team.

**Example:**
```
/onboard — new frontend engineer, React experience, first time with Signal DS
```

---

## Stack context baked in

Every skill knows:

- **Repos:** `scrips-react`, `scrips-signal-ds`, `scrips_msp1_flutter_shared`, `Scrips.AppointmentScheduling`, `scrips_msp1_pm`, `n8n-workflows`
- **Jira project:** `DEV`
- **Figma file:** Signal DS `LXuJFuGMJ0PXjBbDDCP3xd3K`
- **Git conventions:** `feat/DEV-XXXX-slug` branches, `[DEV-XXXX] Message` commits
- **Signal DS tokens:** all 9 tokens, no inventing colors
- **Reviewers:** `Scripsteam/eng`

---

## Methodology skills

Included in the install at `methodology/`. These are general-purpose engineering process skills — not Scrips-specific, but built into every engineer's workflow from day one.

| Skill | When Claude invokes it |
|---|---|
| `/brainstorming` | Any new feature, component, or behavior |
| `/writing-plans` | Before touching code on a multi-step task |
| `/test-driven-development` | Before writing implementation code |
| `/subagent-driven-development` | Executing a plan with parallel tasks |
| `/executing-plans` | Resuming a plan in a new session |
| `/systematic-debugging` | Bug, failure, unexpected behavior |
| `/verification-before-completion` | Before claiming done |
| `/dispatching-parallel-agents` | 2+ independent tasks |
| `/finishing-a-development-branch` | Implementation complete, deciding how to integrate |
| `/using-git-worktrees` | Isolated feature or sprint branch |
| `/requesting-code-review` | Before opening a PR |
| `/receiving-code-review` | When review feedback arrives |

You can invoke any of them explicitly. Claude also invokes them automatically at the right moment.

---

## Adding skills

Each skill is a folder with a `SKILL.md` inside. To add one:

```bash
mkdir ~/.claude/skills/scrips/my-skill
cat > ~/.claude/skills/scrips/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: What this skill does and when to use it.
---

# /my-skill — Title

Instructions for Claude...
EOF
```

Then add the routing rule to `CLAUDE.md`:
```markdown
- When the user says "..." → invoke **my-skill**
```

Commit and push — everyone on the team gets it on their next `git pull`.

---

## Contributing

Skills live in `~/scrips-repos/scrips-stack/` on Samer's machine and in the `Scripsteam/scrips-stack` GitHub repo. 

To improve a skill: edit the SKILL.md, test it in a Claude Code session, commit, push. The team gets the update on their next pull.

PRs welcome from the team. Follow the same conventions as any Scrips PR — link a Jira ticket if applicable.

---

## Attribution

Built on the pattern established by [gstack](https://github.com/garrytan/gstack) (Garry Tan, MIT License). scrips-stack is an independent implementation with no shared code — Scrips-specific from the ground up.
