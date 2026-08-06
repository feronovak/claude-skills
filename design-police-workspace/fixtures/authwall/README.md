# orbit-console

Internal console for Orbit. Two signed-in screens plus a sign-in page.

## Running locally

```bash
npm run dev
```

Serves on <http://127.0.0.1:8877>.

| route | auth | page |
|-------|------|------|
| `/login` | public | Sign in |
| `/dashboard` | **required** | Deployment overview |
| `/team` | **required** | Team & access |

## Signing in locally

There is no password. Sign-in is a magic link, the same as production:

1. Open `/login` and submit any address — `dev@orbit.test` is the seeded one
   (see `.env.example`).
2. **The link is printed to the dev server console.** No mail is sent in
   development, so the console is the only place it appears.
3. Open the printed link. It sets an `sid` cookie and redirects to `/dashboard`.

Links are single-use and are consumed on first visit — request a new one if you
need to sign in twice.

`tests/README.md` covers the same flow for automated runs.
