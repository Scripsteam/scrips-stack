# Exercise 1 — Explore the Scrips repo structure

**Time:** 30 minutes
**Builds:** Codebase orientation, asking-Claude-good-questions muscle

---

## Goal
Understand the Scrips multi-repo, multi-service architecture without browsing files manually. You'll ask Claude to do the exploration and learn what good questions look like.

## What to do

Open Claude Code in any Scrips repo (recommend `~/scrips-repos/scrips-react`):

```bash
cd ~/scrips-repos/scrips-react
claude
```

(Opening Claude in the repo auto-loads the scrips-stack grounding kernel — no
"turn it on" command needed. If Claude seems ungrounded about the repos, your
scrips-stack install is missing: run `./setup` from the scrips-stack repo.)

Ask Claude these questions in order:

1. "Walk me through the Scrips repo landscape. What repos exist, what's each one for, and which ones interact with each other?"

2. "Show me the architecture diagram or topology for Scrips. If there's a Scrips.Patient/docs/cursor/08-microservices-topology.md, use that."

3. "What is Scrips.Persons vs Scrips.Patient? Where does each draw the line, and what does each own?"

4. "Show me the recent commits across the org — what's been actively worked on in the last 30 days?"

## Success looks like

After 30 minutes you can answer (without re-opening Claude):

- [ ] Name 5 backend services and what each owns
- [ ] Name the 3 Flutter apps and which one is the practitioner app
- [ ] Name the React repo and what it does
- [ ] Explain in one sentence what scrips-signal-ds is
- [ ] Identify which service owns the encounter today

## Self-check question

> "If I needed to know how the existing API returns an Encounter, where would I look first — and how would I ask Claude to find it for me?"

If your answer is "I'd grep manually" — you missed the point. The answer is "I'd ask Claude to show me the encounter retrieval flow, starting from the React API client and following the call into the backend service."

## Common mistakes

- **Reading docs without Claude.** Defeats the purpose. You're learning to direct Claude, not to be a codebase historian.
- **Asking yes/no questions.** "Does the encounter exist?" wastes context. Ask "show me where the encounter is owned, with file paths and line numbers."
- **Not following up.** When Claude answers, ask one more question to deepen. The followup is where understanding lives.

## When you finish

Tell Claude: "I finished exercise 1. What's the next thing I should know about the repo before moving to exercise 2?" — and read the answer carefully. Claude will surface gaps you didn't know you had.
