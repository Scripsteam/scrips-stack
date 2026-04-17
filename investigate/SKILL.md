---
name: investigate
description: Debug and root-cause issues in the Scrips stack — .NET API, Flutter, React Admin, Supabase, or infrastructure. Use when something is broken, throwing errors, or behaving unexpectedly.
---

# /investigate — Scrips Debug Workflow

You are a senior Scrips engineer diagnosing a production or development issue. Be systematic. Every hypothesis needs evidence. No guessing.

## Step 1: Classify the issue

Ask or infer:
- Which layer? Flutter app · .NET API · React admin · Supabase · Infrastructure · Auth flow
- What's the symptom? Error message · Wrong data · Crash · Slow · Missing feature
- Where? Dev · Staging · Production
- When did it start? After a deploy · Always · Intermittent

## Step 2: Gather evidence

### If .NET API issue
```bash
# Check recent commits to the API
git log --oneline -10 -- scrips_msp1_pm/

# Find the failing endpoint
grep -rn "route\|endpoint\|controller" --include="*.cs" | grep -i "<keyword>"

# Check for recent migration
ls -lt scrips_msp1_pm/Migrations/ | head -5
```

Common .NET patterns to check:
- `NullReferenceException` → check nullable reference types, missing `[Required]`
- 401/403 → check `[Authorize]` attributes, JWT config, Supabase RLS
- 500 → check `ILogger` calls, unhandled exceptions in controllers
- Slow queries → check missing indexes, N+1 patterns in Entity Framework

### If Flutter issue
```bash
# Find the relevant widget/service
grep -rn "<keyword>" --include="*.dart" lib/

# Check for recent changes
git log --oneline -10 -- lib/
```

Common Flutter patterns to check:
- `setState after dispose` → async gap with widget lifecycle
- `Null check operator` → uninitialized nullable, timing issue
- Black screen / infinite loader → Future not completing, missing error handler
- Navigation crash → route not registered, wrong context

### If Supabase / database issue
- Check RLS policies: does the user's role have access?
- Check if the query works in Supabase Studio SQL editor with the same params
- Check Edge Function logs in Supabase dashboard
- Check if a recent migration changed column names or types

### If React Admin issue
```bash
# Find the component
grep -rn "<keyword>" --include="*.tsx" --include="*.ts" src/

# Check API calls
grep -rn "fetch\|axios\|useQuery\|useMutation" --include="*.tsx" src/ | grep "<endpoint>"
```

Common React patterns to check:
- Data not loading → network tab, check CORS, check auth headers
- Component not updating → stale closure, missing dependency in useEffect
- DS mismatch → component using wrong token, prop type mismatch with Signal DS

## Step 3: Form hypotheses

List 2-3 ranked hypotheses:
```
H1 (most likely): [what you think is wrong] because [evidence]
H2: [alternative] because [evidence]
H3: [edge case] because [evidence]
```

## Step 4: Verify

Test H1 first. Find the specific file and line. Read the code. Run it if possible.

If confirmed:
- State the root cause precisely: `file.ext:line — description`
- Explain why it fails
- Show the fix

If not confirmed: move to H2.

## Step 5: Fix

- Make the minimal fix
- Add a regression note: `// DEV-XXXX: <why this is here>`
- Write a test that would have caught this (if time allows)

## Step 6: Prevention

One sentence: what would have caught this earlier?
- Missing test coverage?
- Missing null check?
- RLS policy gap?
- Missing error boundary?

## Rules

- Read the actual code before diagnosing
- Never suggest "try clearing cache" as a first step
- If you can't find the root cause in 3 passes, say so and ask for logs/screenshots
- Production issues: state if a hotfix is needed vs. can wait for next sprint
