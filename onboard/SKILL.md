---
name: onboard
description: Onboard a new Scrips engineer or contractor. Gives them the stack context, repo map, conventions, and first-day checklist. Use when a new developer joins or when asked to "onboard" someone.
---

# /onboard — New Scrips Developer Onboarding

## Ask first

- What's the developer's name and role? (Frontend · Backend · Mobile · Full-stack)
- What's their experience with the relevant stack?
- Which team? (Product · Platform · Data)

## The Scrips stack (share this)

### Repos (all under github.com/Scripsteam)

| Repo | What it is | Stack |
|------|-----------|-------|
| `scrips-react` | Admin web app | React + TypeScript + Signal DS |
| `scrips-signal-ds` | Design system | React + CSS + Storybook |
| `scrips_msp1_flutter_shared` | Shared Flutter code | Flutter / Dart |
| `Scrips.AppointmentScheduling` | Mobile scheduling app | Flutter / Dart |
| `scrips_msp1_pm` | Backend API | .NET C# |
| `n8n-workflows` | Automation | n8n JSON |

**Personal repos** (github.com/samertad):
- `signal-portal` — Signal DS documentation portal

### Infrastructure
- **Database:** SQL Server (current) — PostgreSQL migration possible in future
- **Auth:** JWT-based (.NET handles auth)
- **Hosting:** Vercel (React admin + Signal DS portal)
- **CI/CD:** GitHub Actions
- **Monitoring:** TBD

### Tools
- **Project management:** Jira (project key: `DEV`)
- **Design:** Figma — Signal DS file `LXuJFuGMJ0PXjBbDDCP3xd3K`
- **Knowledge base:** Confluence
- **Communication:** Slack

## First day checklist

```
### Access requests (Samer provides)
- [ ] GitHub org (Scripsteam)
- [ ] Jira (DEV project)
- [ ] Figma (Signal DS file)
- [ ] Confluence
- [ ] Slack (#dev channel)
- [ ] DB access (ask Samer — SQL Server staging + prod)
- [ ] Vercel (if needed)

### Local setup
- [ ] Clone relevant repos to ~/scrips-repos/
- [ ] Install scrips-stack: `git clone --depth 1 https://github.com/Scripsteam/scrips-stack.git ~/.claude/skills/scrips`
- [ ] Verify methodology skills installed: `ls ~/.claude/skills/scrips/methodology/`
- [ ] Set up Signal DS locally: cd scrips-signal-ds && npm install && npm run storybook
- [ ] Set up React admin: cd scrips-react && npm install && npm run dev
- [ ] Read CLAUDE.md in the repo

### First tasks
- [ ] Read the last 3 sprint retros (in Confluence)
- [ ] Pull and run the dev server
- [ ] Pick up one small DEV ticket labeled "good-first-issue"
```

## AI workflow skills

Scrips engineers get two layers of skills when they install scrips-stack:

**Layer 1 — Scrips skills** (project-specific): `/ship`, `/review`, `/investigate`, `/sprint`, `/design-sync`, `/qa`, `/brief`, `/retro`, `/cso`, `/checkpoint`

**Layer 2 — Methodology skills** (engineering process): available at `~/.claude/skills/scrips/methodology/` — these are the same skills Samer uses and are installed automatically with scrips-stack.

| Skill | Type it when... |
|---|---|
| `/brainstorming` | Starting anything creative — new component, new feature, new behavior |
| `/writing-plans` | You have requirements and need a step-by-step plan before coding |
| `/test-driven-development` | Before writing implementation code — test first |
| `/subagent-driven-development` | Executing a plan with independent parallel tasks |
| `/executing-plans` | Resuming a plan in a new session |
| `/systematic-debugging` | Hit a bug or unexpected behavior — before guessing |
| `/verification-before-completion` | Before saying "done" — runs checks, requires evidence |
| `/dispatching-parallel-agents` | 2+ independent tasks that can run at the same time |
| `/finishing-a-development-branch` | Implementation done — need to decide: PR, merge, or cleanup |
| `/using-git-worktrees` | Starting isolated feature work |
| `/requesting-code-review` | Before opening a PR |
| `/receiving-code-review` | When review feedback arrives |

**The rule:** Claude will invoke these automatically when the moment is right. You can also type them explicitly at any time.

## Key conventions to know

1. **Every PR links a Jira ticket.** No exceptions.
2. **Branch format:** `feat/DEV-XXXX-short-description`
3. **Commit format:** `[DEV-XXXX] Description`
4. **DS first:** Always use Signal DS components. Never invent UI.
5. **Signal DS tokens:** Use the CSS variables, never hardcode hex values.
6. **DB access control:** Every endpoint is authorized. No raw data exposed without auth.
7. **No `console.log` in commits.**

## Tailor by role

### If frontend (React):
Point them to:
- `scrips-signal-ds` Storybook — know what components exist
- The Signal DS token reference in `scrips-stack/CLAUDE.md`
- Start with a small UI ticket

### If mobile (Flutter):
Point them to:
- `scrips_msp1_flutter_shared` and how it's imported
- Dart/Flutter conventions in the codebase
- Start with a simple widget or service fix

### If backend (.NET):
Point them to:
- The API architecture doc in Confluence
- Entity Framework setup and migration conventions
- DB access patterns via Entity Framework — understand before touching migrations

## Output

Send a formatted onboarding doc to Samer and (if applicable) directly to the new dev via Slack.
