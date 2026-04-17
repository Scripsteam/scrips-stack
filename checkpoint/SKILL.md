---
name: checkpoint
description: Save session progress to a file so work can be resumed in a future session. Use when wrapping up mid-task, before context runs out, or when asked to "save progress", "checkpoint", or "I'll continue later".
---

# /checkpoint — Save Session Progress

You are writing a handoff memo for your future self. Be specific enough that you can pick up exactly where you left off with no context.

## Gather state

```bash
git status --porcelain
git log --oneline -5
git branch --show-current
```

## Write the checkpoint file

Save to: `~/.claude/projects/scrips/checkpoints/checkpoint-$(date +%Y%m%d-%H%M).md`

```markdown
---
date: [ISO timestamp]
branch: [current branch]
jira: [DEV-XXXX if applicable]
status: IN_PROGRESS
---

# Checkpoint: [one-line summary of what's in progress]

## What I was doing
[2-3 sentences: the task, why it matters, what approach was being taken]

## Where I left off
[Exact state — what file was being edited, what step in the process, what was just completed]

## What's next
1. [Specific next action]
2. [Action after that]
3. [Then...]

## Open questions / decisions needed
- [Anything that needs Samer's input or a decision before continuing]

## Files changed so far
[git diff --stat output]

## Key context that won't be obvious later
[Anything surprising, non-obvious, or easy to forget — workarounds, constraints, architectural decisions made mid-session]

## Commands to verify state on resume
```bash
git log --oneline -5
[any other useful diagnostic command]
```
```

## Report to user

After writing the file, tell Samer:
- Where the checkpoint was saved
- The one-line summary of where things stand
- The exact next step when he returns

## On resume

When Samer says "resume", "continue from checkpoint", or "where were we":
1. Read the most recent checkpoint file
2. Summarize where things stand in 2-3 sentences
3. Propose the next action
4. Ask: "Ready to continue?"
