# Exercise 3 — Skill invocation drill

**Time:** 30 minutes
**Builds:** Skill ecosystem fluency, knowing what to type when

---

## Goal
Practice invoking 5 key skills against safe targets so you know what each does before you need it under pressure.

## What to do

For each skill below, invoke it and observe Claude's behavior. Don't actually commit anything — this is a dry run.

### Drill A — port planning, grounded on the real Flutter source

There is no magic "port" command — a good port is: **read the real Flutter
widget → plan the React port → implement → verify.** Practice the planning step
on a real file. In `scrips-practitioner-react`:

```
Read this Flutter widget as the spec (don't edit anything):
~/scrips-repos/scrips_msp1_flutter_shared/...  (ask Claude to find a small encounter widget)
Plan its port to a React component using Signal DS. Show me the plan only —
the component shape, the props, the Signal DS components it maps to, the Storybook story.
```

Watch Claude read the actual `.dart` source (not guess), then produce a plan
grounded in it. This is the real porting flow you'll use daily. (`/writing-plans`
formalizes the planning step when the slice is bigger.)

### Drill B — /writing-plans

```
/writing-plans
```

Goal: "Plan the implementation of a new Settings tab in the practitioner app for working-hours config. Don't write code — just produce the plan."

Watch Claude:
- Ask clarifying questions
- Identify dependencies
- Produce a step-by-step plan
- Flag risks

Read the plan critically. Does it match what you'd do? If not, where's the gap?

### Drill C — /systematic-debugging

```
/systematic-debugging
```

Scenario: "My encounter screen renders blank after I added a new prop. The console shows no errors. Walk through the debugging protocol with me."

Watch Claude:
- Force you to state the hypothesis
- Demand evidence (logs, network, props)
- Refuse to guess
- Iterate hypothesis → test → result

### Drill D — /review

```
/review
```

Pick any small recent commit on the current branch and have Claude review it:
"Review the most recent commit on this branch — flag any Signal DS violations, TypeScript issues, missing tests."

Watch the review structure. Note what categories Claude checks.

### Drill E — /design-sync

```
/design-sync
```

Goal: "I'm about to implement a button in the encounter screen. Check Signal DS tokens for the right primary blue and the right border-radius for a primary button."

Watch Claude:
- Reference design-tokens.ts
- Cross-check Storybook
- Surface drift if any

## Success looks like

After 30 minutes:

- [ ] You can explain in one sentence what each of the 5 skills does
- [ ] You can name which skill to invoke for: porting a screen, planning a feature, fixing a bug, before opening a PR, after implementing a UI component
- [ ] You've seen Claude refuse to guess (in /systematic-debugging) and understand why that's the point
- [ ] You've seen Claude read real source before planning, and understand why grounding beats guessing

## Self-check question

> "It's Monday morning. You pick up a ticket to port the Practitioner Schedule sub-tab. What's your FIRST move, and why?"

Answer: **Have Claude read the real Flutter source as the spec, then plan the port** — Jira is a pointer, not a spec, and the Flutter `.dart` is the source of truth for behavior. Plan before code; `/writing-plans` for anything non-trivial.

If you said "just start coding" — re-read. The spec comes from the real source, not from memory; that's what stops the port from drifting.

## When you finish

Tell Claude: "Quiz me on skill routing. Give me 5 scenarios and I'll name the right skill." — and let Claude grade you.
