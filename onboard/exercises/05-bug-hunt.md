# Exercise 5 — Bug hunt with systematic debugging

**Time:** 1 hour
**Builds:** Debugging discipline, refusing to guess

---

## Goal
Use `/systematic-debugging` to find a real bug. You'll learn the hypothesis-test-evidence loop and unlearn the urge to "just try this."

## What to do

### Setup — Pick a real recent bug

Open Jira and find a recently-closed bug ticket (status: Done, type: Bug). Read the ticket and the linked PR.

Ideally pick a bug whose root cause is non-obvious — not a typo, but a state machine mistake or a race condition.

Examples to look for:
- Async violations (recently fixed in SND-329, SND-348, SND-370)
- Tenant isolation bugs (SND-323)
- gRPC metadata issues (PROD-505)

### Step 1 — Reproduce mentally

Read the bug report. Before reading the fix, ask yourself:
- What would I check first?
- What hypothesis would I form?
- How would I prove or disprove it?

Write your answer in a note — don't share with Claude yet.

### Step 2 — Run the protocol

In Claude:

```
/systematic-debugging
```

Then describe the bug as if it just happened:
> "I'm seeing [symptom from Jira]. The user does [steps from ticket]. Help me find the root cause."

Watch Claude:
- Refuse to guess
- Demand symptoms first
- Form a falsifiable hypothesis
- Ask for evidence (logs, network, code paths)
- Iterate until the root cause is identified

DO NOT tell Claude the answer from the PR. Let it work.

### Step 3 — Compare to the actual fix

Once Claude reaches a root cause hypothesis, compare to the actual fix in the PR.

- Did Claude reach the same conclusion?
- Did it take more or fewer iterations than the original engineer?
- What evidence was decisive?

### Step 4 — Reflect on what `/systematic-debugging` REFUSED to let you do

The skill enforces discipline. Specifically:
- It refuses to suggest fixes before symptoms are stated
- It refuses to "just try this"
- It demands evidence over intuition
- It iterates hypotheses, doesn't abandon them

These are the things humans (especially senior engineers) skip when in a hurry. The skill keeps you honest.

## Success looks like

After 1 hour:

- [ ] You reached a root cause hypothesis using the protocol
- [ ] You can recite the loop: hypothesis → test → evidence → next hypothesis
- [ ] You felt the urge to "just try this" at least once, and resisted
- [ ] You understand WHY guessing is more expensive than checking, even when checking is slower

## The principle

**Guessing is more expensive than checking.** Every hour you spend guessing-and-trying is an hour Claude could have spent reading-and-thinking. Reading is cheap. Trying broken fixes is expensive (review cycles, regressions, lost trust).

Senior engineers often think they've earned the right to skip the protocol. They haven't. The protocol catches things the gut misses.

## Self-check question

> "It's Friday at 5pm. Production is down. A 500 error is hitting `/api/Patient/{id}`. What's your first move?"

Wrong answer: "I'll look at recent commits and revert the most likely one."
Right answer: "I'll invoke /systematic-debugging. State the symptom. Form a hypothesis. Check the evidence. The revert might be correct but I won't know until I've reduced the candidate set."

## When you finish

Tell Claude: "Reflect on this debugging session. What did I almost do that the protocol prevented?"

The answer is your future self's protection.
