# scrips-stack releases

Newest first. Every team-kit change lands here with a plain-language note — what changed, why, and what
you do differently. (The `scrips-stack-release` skill keeps this honest.)

---

## 2026-06-12 — Open-loops discipline + release discipline  (PR #12)

**What changed:**
- `open-loops-ledger` — new skill. Stops loose ends dying in conversation.
- `scrips-stack-release` — new skill. The rule that produced this very note: no team-kit change ships without a release note + team education + acknowledgement.

**Why:** as we lean harder on agents, the bottleneck isn't generating work — it's *losing* it. Code that isn't deployed, decisions made in chat and never written down, "I'll do X next" with no owner and no tracker. It compounds. These two skills make the debt durable, owned, and visible.

**What you do differently:**
- When you (or your agent) defer something, make a decision, leave a PR open, or need a ticket you haven't filed → it becomes a row in `.claude/open-loops.md` with an **owner** and a **real tracker** (Jira/GH), or it's killed with a reason. Never a vague "next steps" paragraph.
- When you change anything in `scrips-stack` → you write a release note here + a friendly team post + ask everyone to acknowledge.

**Owner / questions:** Samer (rule owner) · this update authored via Claude Code.
