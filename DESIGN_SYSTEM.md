# Zomorod Melal Design System

## Brand direction
Use the official Zomorod Melal visual identity: deep agricultural green, gold accents, warm cream backgrounds and clean white surfaces.

## UI principles
1. Persian-first, RTL by default.
2. Mobile-first responsive layout.
3. Consistent spacing, radius, typography and focus states.
4. Reusable components instead of page-specific duplication.
5. Accessibility: keyboard focus, semantic HTML, readable contrast and touch-friendly controls.

## Canonical CSS structure
```
static/
  css/
    tokens.css
    base.css
    layout.css
    components.css
    responsive.css
    pages/
```

Until migration is complete, existing CSS remains in place. New pages should consume shared tokens/components rather than inventing page-local visual primitives.
