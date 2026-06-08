# Exercise 3 — Skill invocation drill

**Time:** 30 minutes
**Builds:** Skill ecosystem fluency, knowing what to type when

---

## Goal
Practice invoking 5 key skills against safe targets so you know what each does before you need it under pressure.

## What to do

For each skill below, invoke it and observe Claude's behavior. Don't actually commit anything — this is a dry run.

### Drill A — /port-spec

In `scrips-react`:

```
/port-spec
```

When Claude asks what you're porting, say: "I'm exploring — show me what /port-spec would do if I were porting the Flutter `encounter_review_of_system` module to React."

Watch Claude dispatch 5 parallel subagents (Figma A, Figma B, Backend, Confluence+brain, LIVE FE audit). You don't have to run the full thing — just see the pattern.

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
- [ ] You've seen Claude dispatch subagents (in /port-spec) and understand parallel exploration

## Self-check question

> "It's Monday morning. You pick up PROD-762 (port the Practitioner Schedule sub-tab). What's the FIRST skill you invoke, and why?"

Answer: `/port-spec` — because you're porting a live feature. Jira is a pointer, not a spec. /port-spec produces the spec.

If you said "/sprint" — re-read the /port-spec description. Sprint is for execution. Spec comes first.

## When you finish

Tell Claude: "Quiz me on skill routing. Give me 5 scenarios and I'll name the right skill." — and let Claude grade you.
