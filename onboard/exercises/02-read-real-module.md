# Exercise 2 — Read a real module end-to-end

**Time:** 45 minutes
**Builds:** Domain pattern fluency, ability to inherit a codebase via Claude

---

## Goal
Understand Andrew's domain folder pattern by having Claude walk you through one fully-shipped module — scheduling. By the end you should be able to build a NEW module that looks identical without being told the pattern again.

## What to do

In `scrips-react`:

```bash
cd ~/scrips-repos/scrips-react
claude
```

Ask Claude:

1. "Walk me through `src/scheduling/` end to end. Show me the folder structure first, then explain how the pieces fit: components, pages, services, store. Use file paths."

2. "Read `src/scheduling/store/scheduling-store.ts` and explain the two-store rule. What's in this Zustand store vs what's NOT in it?"

3. "Read `src/scheduling/services/use-appointments.ts` and explain why services live here, not in a global services folder."

4. "Read `src/scheduling/components/frame-scheduling.tsx` and tell me what FrameScheduling does — is it a layout, a page, or both?"

5. "If I were to add a new domain, say `src/clinical/encounter/`, what files and folders would I need? Generate the skeleton list."

## Success looks like

After 45 minutes:

- [ ] You can recite the folder pattern from memory: `components/ + pages/ + services/ + store/`
- [ ] You can explain why Zustand stores only UI state (not server data)
- [ ] You can explain why TanStack Query owns server state
- [ ] You can name three things Andrew never did (so you won't either)
- [ ] You could draw the dependency arrows: page → store, page → service hook, component → store

## Self-check question

> "Why is `use-appointments.ts` in `src/scheduling/services/` and not in `src/services/scheduling/`?"

If you don't know, re-ask Claude. The answer reveals a key architectural decision.

## The three things Andrew never did (Claude will surface)

After Claude explains, write these down:
1. _______________________________________
2. _______________________________________
3. _______________________________________

If your list is empty, you didn't finish the exercise.

## When you finish

Tell Claude: "I'm going to apply this pattern when I create the encounter module. Critique my plan: I'll create `src/clinical/encounter/components/`, `pages/`, `services/`, `store/`. What am I missing or getting wrong?"

Read carefully. This is where you catch your own future mistakes.
