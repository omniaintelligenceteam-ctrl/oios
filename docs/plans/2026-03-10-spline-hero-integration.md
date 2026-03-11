# Spline Hero Integration (React + shadcn)

This workspace currently does not contain a React TypeScript app with Tailwind/shadcn configuration (`package.json`, `components.json`, `tailwind.config.*` were not found at root).

## Setup (if needed)

```bash
npx create-next-app@latest getoios-web --typescript --tailwind --eslint --app
cd getoios-web
npx shadcn@latest init
```

When shadcn asks component path, use `components`. This keeps reusable UI in `components/ui`, which is the standard location for:
- predictable imports (`@/components/ui/...`)
- compatibility with copied shadcn community components
- cleaner separation between primitives and feature-level components

## Required installs

```bash
npm install @splinetool/runtime @splinetool/react-spline framer-motion lucide-react clsx tailwind-merge
```

## Files added in this workspace

- `components/ui/splite.tsx`
- `components/ui/demo.tsx`
- `components/ui/spotlight.tsx`
- `components/ui/spotlight-motion.tsx`
- `components/ui/card.tsx`
- `lib/utils.ts`
- `app/page.tsx` (hero usage example)
- `app/globals.css` (loader + spotlight animation)

## Notes

- Default style entry for shadcn + App Router is `app/globals.css`.
- If your current site uses a different hero file, move the `SplineSceneBasic` usage from `app/page.tsx` into that hero section.
