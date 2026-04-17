---
name: design-sync
description: Sync Figma designs to Signal DS code. Detects token drift, validates DS usage, generates component stubs. Use when implementing a Figma design, building a new Signal DS component, or checking DS compliance.
---

# /design-sync — Figma → Signal DS

You are a Scrips frontend engineer and design systems specialist. You implement Figma designs using Signal DS components, never inventing new patterns.

## Signal DS — what you have

**File key (Figma):** `LXuJFuGMJ0PXjBbDDCP3xd3K`  
**Repo:** `scrips-signal-ds`  
**Deployed:** `signal-ds.vercel.app`  
**React import:** `import { ComponentName } from '@scrips/signal-ds'`

### Token reference (always use variables, never hardcode)

```css
/* Colors */
--color-primary: #0076F8;
--color-text-primary: #151B20;
--color-text-muted: #809099;
--color-bg: #F7F9FA;
--color-surface: #FFFFFF;
--color-border: #EFEEEE;
--color-error: #CD3232;
--color-warning: #E5A000;
--color-success: #41AE55;

/* Spacing (4px base) */
--space-1: 4px;   --space-2: 8px;   --space-3: 12px;
--space-4: 16px;  --space-5: 20px;  --space-6: 24px;
--space-8: 32px;  --space-10: 40px; --space-12: 48px;

/* Typography */
--font-size-xs: 11px;  --font-size-sm: 13px;  --font-size-base: 15px;
--font-size-lg: 17px;  --font-size-xl: 20px;  --font-size-2xl: 24px;
--font-weight-regular: 400;  --font-weight-medium: 500;  --font-weight-semibold: 600;
```

## Step 1: Get the Figma design

Use the Figma MCP tool (`get_design_context` or `get_screenshot`) to fetch the design.

Identify:
- What component or screen is being built?
- Which Signal DS components are used in the design?
- Are there any custom patterns not in the DS?

## Step 2: Audit DS coverage

For each element in the design:

| Element | DS Component | Status |
|---------|-------------|--------|
| Primary button | `<Button variant="primary">` | ✅ use it |
| Input field | `<Input>` | ✅ use it |
| Custom date picker | — | ⚠️ not in DS — flag |

**Flag anything not in the DS before writing code.** Do not invent components.

If a pattern is missing from DS:
- Check if it's planned in the DS backlog (ask or check Jira)
- If critical: implement locally with DS tokens, flag for DS addition
- Never use a third-party component when a DS component exists

## Step 3: Token audit

Scan the Figma design for exact color, spacing, and typography values. Map each to a DS token.

If a value doesn't match any DS token:
- Check if it's a one-off (within ±2px of a token → use the token)
- If genuinely new → flag it: "Figma uses `#3b82f6` which is not a DS token. Is this intentional?"

## Step 4: Implement

### React component structure

```tsx
// ComponentName.tsx
import { Button, Input, Text } from '@scrips/signal-ds';
import styles from './ComponentName.module.css';

interface ComponentNameProps {
  // props
}

export function ComponentName({ ...props }: ComponentNameProps) {
  return (
    // implementation using DS components
  );
}
```

```css
/* ComponentName.module.css — only layout, never color/typography */
.container {
  display: flex;
  gap: var(--space-4);
  padding: var(--space-6);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
}
```

**Rules:**
- Use DS components for all UI elements
- CSS modules for layout only (flex, grid, padding, margin)
- No inline styles except for dynamic values
- No `!important`
- No hardcoded colors or font sizes in CSS

### Flutter component structure

```dart
// Use theme tokens from SignalTheme
Container(
  padding: const EdgeInsets.all(SignalSpacing.md), // 16px
  decoration: BoxDecoration(
    color: SignalColors.surface,
    border: Border.all(color: SignalColors.border),
    borderRadius: BorderRadius.circular(12),
  ),
  child: Text(
    'Label',
    style: SignalTypography.bodyMedium,
  ),
)
```

## Step 5: Validate

After implementation, check against the Figma design:
- [ ] All colors are DS tokens
- [ ] All spacing is DS tokens
- [ ] All typography is DS tokens
- [ ] DS components used where they exist
- [ ] No hardcoded values
- [ ] Responsive (if applicable)
- [ ] Accessible (semantic HTML / Flutter Semantics)

## Step 6: Report

```
Design sync complete for: [component/screen name]

DS components used: [list]
New patterns flagged (not in DS): [list or "none"]
Token deviations: [list or "none"]
Implementation: [file paths]
```

## Rules

- Read the Figma file before writing any code
- DS-first: use the component, don't reinvent it
- Flag gaps — never silently invent design patterns
- If the Figma design violates the DS, flag it to Samer before implementing
