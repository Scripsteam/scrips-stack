# scrips-stack — Claude Code Instructions

## Stack context

You are working on the Scrips Healthcare codebase. Key facts:

- **Mobile:** Flutter/Dart — repo `scrips_msp1_flutter_shared`, `Scrips.AppointmentScheduling`
- **API:** .NET C# — repo `scrips_msp1_pm`
- **Admin:** React + TypeScript — repo `scrips-react`
- **Design system:** Signal DS — repo `scrips-signal-ds`, deployed at `signal-ds.vercel.app`
- **Database:** SQL Server (current) — possible PostgreSQL migration in future
- **Project management:** Jira (project key: DEV), Confluence
- **Design:** Figma (Signal DS file key: `LXuJFuGMJ0PXjBbDDCP3xd3K`)

## Signal DS tokens (always use these, never invent)

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
| Success | `#41AE55` | Confirmations, success |

## Git conventions

- Branch format: `{type}/{jira-ticket}-{short-description}` (e.g. `feat/DEV-2270-admin-department-mgmt`)
- Commit format: `[DEV-XXXX] Short description` (imperative, present tense)
- PR title: `[DEV-XXXX] Feature description`
- Always link Jira ticket in PR body
- Reviewers: Andrew (@Scripsteam/eng) unless specified

## Skill routing

When the user's request matches a scrips-stack skill, ALWAYS invoke it using the Skill tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.

Key routing rules:
- Ship, deploy, create PR, push branch → invoke **ship**
- Code review, check my diff, review this PR → invoke **review**
- Bug, error, crash, 500, why is this broken → invoke **investigate**
- Sprint planning, sprint demo, sprint review, Jira ceremony → invoke **sprint**
- Figma to code, Signal DS, component → invoke **design-sync**
- QA, test the feature, acceptance criteria, staging → invoke **qa**
- Morning brief, what's the plan today, standup → invoke **brief**
- Retrospective, retro, what did we ship → invoke **retro**
- Security audit, OWASP, vulnerabilities, DB access control → invoke **cso**
- Save progress, checkpoint, resume later → invoke **checkpoint**

Methodology routing (auto-invoke without being asked):
- User starts describing a new feature, component, or behavior → invoke **brainstorming** FIRST
- Requirements clear, about to write code → invoke **writing-plans**
- Implementing from a plan → invoke **test-driven-development** before each unit
- Plan has parallel independent tasks → invoke **subagent-driven-development**
- User says "done", "finished", "it works" → invoke **verification-before-completion** FIRST
- Bug, test failure, "why isn't this working" → invoke **systematic-debugging** FIRST
- About to open a PR → invoke **requesting-code-review**
- Review feedback received → invoke **receiving-code-review** before implementing

## Available scrips-stack skills

Installed at: `~/.claude/skills/scrips/`

/ship · /review · /investigate · /sprint · /design-sync · /qa · /brief · /retro · /cso · /checkpoint

## Engineering methodology skills

These are Samer's personal superpowers — general-purpose engineering process skills available to all agents, including Andrew's sessions. Installed at `~/.claude/skills/`.

| Skill | When to use |
|---|---|
| `brainstorming` | **Before any creative work** — new features, new components, new behavior. Explores intent and requirements before a line is written. |
| `writing-plans` | After requirements are clear, before touching code. Produces a step-by-step implementation plan saved to `docs/`. |
| `subagent-driven-development` | When executing an implementation plan with independent tasks. Fans out work to parallel agents. |
| `executing-plans` | When resuming a written plan in a new session with review checkpoints. |
| `test-driven-development` | Before writing any implementation code. Write the test first, then implement. |
| `verification-before-completion` | **Before claiming done.** Runs verification commands, confirms output. Evidence before assertions. |
| `systematic-debugging` | When you hit a bug, test failure, or unexpected behavior. Prevents random fix attempts. |
| `dispatching-parallel-agents` | When 2+ independent tasks can run simultaneously. |
| `finishing-a-development-branch` | When implementation is complete and you need to decide: PR, merge, or cleanup. |
| `using-git-worktrees` | For isolated sprint or feature branches. Keeps main workspace clean. |
| `requesting-code-review` | Before opening a PR or asking for review — structures the review request. |
| `receiving-code-review` | When review feedback arrives — before implementing suggestions. |

### Routing for Andrew

If you're Andrew using this CLAUDE.md:
- Starting a new feature → `brainstorming` first, then `writing-plans`
- Implementing from a plan → `test-driven-development` + `subagent-driven-development`
- Hit a bug → `systematic-debugging` (not random guessing)
- About to say "done" → `verification-before-completion` first
- Opening a PR → `requesting-code-review`
