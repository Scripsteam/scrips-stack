# Exercise 4 — The empty file challenge

**Time:** 1 hour
**Builds:** Context discipline, knowing what Claude needs from you vs what it can infer

---

## Goal
You will create an empty React component file and ask Claude to fill it. The first attempt will produce something that LOOKS right but isn't. By the end you'll know how to give Claude enough context to produce production-quality code on the first try.

## What to do

### Step 1 — Create the empty file

```bash
cd ~/scrips-repos/scrips-react
touch /tmp/EmptyEncounterCard.tsx
```

### Step 2 — Naive first attempt

In Claude:

> "Fill /tmp/EmptyEncounterCard.tsx with a React component that shows an encounter summary card. Use Signal DS."

Let Claude produce the file. Save the output but DON'T commit it.

### Step 3 — Critique what Claude produced

Ask Claude:
> "Critique the file you just wrote. Compared to the actual conventions in `src/scheduling/components/`, what's wrong? What's missing? What did you infer that you shouldn't have?"

Read carefully. You'll see Claude identify gaps like:
- Used inline styles instead of Signal DS tokens
- Guessed at prop types instead of importing real types
- No TanStack Query hook for the encounter data
- No story file
- Missing test

### Step 4 — Give Claude the missing context

Now ask Claude to redo it with full context:

> "Redo /tmp/EmptyEncounterCard.tsx. Before writing, read these first:
> 1. `src/scheduling/components/appointments/appointment-card.tsx` (for the card pattern)
> 2. `Scrips.Patient/Domain/Entities/Encounter.cs` (for the data shape)
> 3. `scrips-signal-ds` Storybook for the Card component
> 4. The two-store rule (Zustand UI / TanStack server)
>
> THEN write the component with: TypeScript types matching the entity, TanStack Query hook for fetching, Signal DS Card component, story file, test stub."

Watch Claude work. The output should be dramatically better.

### Step 5 — Reflect

Compare the two outputs side by side. What changed in the second version that wouldn't have happened without the context?

## Success looks like

After 1 hour:

- [ ] You can name 4+ things Claude got wrong in the first naive attempt
- [ ] You can articulate WHY Claude got them wrong (insufficient context, not Claude's failure)
- [ ] You have a mental model: "before asking Claude to write code, tell it WHAT TO READ FIRST"
- [ ] You understand the difference between "Claude infers" and "Claude knows"

## The principle

**Claude is excellent at writing code that LOOKS right.** Producing code that IS right requires context. Your job as the architect is to give Claude that context.

The cost of context-loading is 30 seconds. The cost of a wrong-but-plausible PR is hours of review + revision + your tech debt.

## Self-check question

> "Before asking Claude to implement a new component, what are the 3-5 things you should have it read first?"

Generic answer:
1. The closest existing analog (same pattern, different domain)
2. The data shape (entity or DTO it consumes)
3. The design source (Storybook component or Figma frame)
4. The convention doc (CLAUDE.md in the repo)
5. The integration point (where it gets called from)

## When you finish

Delete `/tmp/EmptyEncounterCard.tsx` — it was a learning artifact, not production code.
