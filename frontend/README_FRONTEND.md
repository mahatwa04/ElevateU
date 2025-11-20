# ElevateU Frontend

This README explains how to start the frontend project and where global CSS must live when using the Next.js app router.

## Run locally

1. Install dependencies (only required once):

```powershell
cd "C:\Users\ABHINAV KUMAR\OneDrive\Desktop\ElevateU\frontend"
npm install
```

2. Start dev server:

```powershell
npm run dev
```

Open http://localhost:3000

## Important: Global CSS location

When using the Next.js app router, your global CSS file must live in the `app/` directory and be imported from `app/layout.tsx`:

- Use: `app/globals.css`
- Avoid: `src/styles/globals.css` (Next.js won't automatically load from `src`)

If you previously had `src/styles/globals.css`, it was moved to `app/globals.css` to follow Next.js conventions.

## Notes

- React Query Provider and DevTools are in `src/providers/Providers.tsx` (client wrapper) so `app/layout.tsx` can stay a server component.
- The app requires Node.js + npm installed on your machine.
