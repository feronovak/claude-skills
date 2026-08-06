# Automated runs

The console has no password login. To reach `/dashboard` or `/team` in a
browser session:

1. `POST /login` with `email=dev@orbit.test` (form-encoded).
2. Read the magic link from the dev server's stdout.
3. `GET` that link — it sets the `sid` cookie and redirects to `/dashboard`.

The cookie is a plain session id, so any driver that keeps cookies between
requests stays signed in for the rest of the run.
