# scrips-stack — Claude Code Instructions

## Stack context

You are working on the Scrips Healthcare codebase. Key facts:

- **Mobile:** Flutter/Dart — repo `scrips_msp1_flutter_shared`, `Scrips.AppointmentScheduling`
- **API:** .NET C# — repo `scrips_msp1_pm`
- **Admin:** React + TypeScript — repo `scrips-react`
- **Design system:** Signal DS — repo `scrips-signal-ds`, deployed at `signal-ds.vercel.app`
- **Database:** Supabase (PostgreSQL + RLS + Edge Functions)
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
- Security audit, OWASP, vulnerabilities, Supabase RLS → invoke **cso**
- Save progress, checkpoint, resume later → invoke **checkpoint**

## Available scrips-stack skills

Installed at: `~/.claude/skills/scrips/`

/ship · /review · /investigate · /sprint · /design-sync · /qa · /brief · /retro · /cso · /checkpoint
