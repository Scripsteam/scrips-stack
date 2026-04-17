# scrips-stack

> Garry Tan built gstack to ship 600K lines in 60 days. We built scrips-stack to ship Scrips faster.

scrips-stack turns Claude Code into a virtual Scrips engineering team — a release engineer who ships PRs the right way, a QA lead who tests staging, a security officer who runs OWASP audits, a designer who catches Signal DS violations, and a sprint manager who runs Jira ceremonies. Nine skills, all slash commands, all Markdown, all built for your exact stack.

**Stack:** Flutter (mobile) · .NET (API) · React + TypeScript (admin) · Signal DS · Supabase · Jira · Figma

## Install — 30 seconds

Open Claude Code in any Scrips repo and paste:

> Install scrips-stack: run `git clone --depth 1 https://github.com/Scripsteam/scrips-stack.git ~/.claude/skills/scrips && cd ~/.claude/skills/scrips && ./setup` then add scrips-stack routing to CLAUDE.md.

Or manually:

```bash
git clone --depth 1 https://github.com/Scripsteam/scrips-stack.git ~/.claude/skills/scrips
cd ~/.claude/skills/scrips && ./setup
```

Then add to your project's CLAUDE.md:

```bash
cat ~/.claude/skills/scrips/CLAUDE.md >> CLAUDE.md
```

## Skills

| Command | What it does |
|---------|-------------|
| `/ship` | Create PR with Scrips conventions — branch name, commit format, Jira link, reviewer assignment |
| `/review` | Code review against Scrips standards — Flutter/Dart, .NET C#, React/TS, Signal DS |
| `/investigate` | Debug with full Scrips context — Supabase, .NET API, Flutter, Sentry logs |
| `/sprint` | Jira sprint ceremonies — planning, demo prep, retro in one workflow |
| `/design-sync` | Figma → Signal DS code — validates tokens, catches drift, generates component stubs |
| `/qa` | QA test staging URLs against acceptance criteria |
| `/brief` | Morning brief — Jira sprint status, open PRs, blockers, priorities |
| `/retro` | Sprint retrospective — shipped/broke/learned format with Jira data |
| `/cso` | Security audit — OWASP Top 10, STRIDE, Supabase RLS, Flutter deep links |
| `/checkpoint` | Save progress mid-session — writes a resumable context file |

## Team mode (everyone gets it)

Every dev installs globally. Updates are automatic.

```bash
cd ~/.claude/skills/scrips && git pull
```

Add to the repo so new devs get the routing:

```bash
cat ~/.claude/skills/scrips/CLAUDE.md >> CLAUDE.md
git add CLAUDE.md && git commit -m "chore: add scrips-stack skill routing"
```

## Philosophy

Built on the same insight as gstack: AI makes completeness near-free. A design audit that takes a designer half a day takes Claude 3 minutes. A security audit that gets skipped because there's no time runs automatically on every PR.

The goal is not to replace engineers — it's to let Andrew ship like a team of five.

## Attribution

Inspired by [gstack](https://github.com/garrytan/gstack) (Garry Tan, MIT). scrips-stack is independently built for Scrips Healthcare's stack and team conventions.
