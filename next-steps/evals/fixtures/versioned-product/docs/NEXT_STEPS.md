# Fixture Product — Next Steps

Future work only. Completed work lives in git history.

**Last reviewed:** 2026-07-30.

Priority: 🟥 near-term · 🟧 scheduled · ⬜ backlog / until-trigger

---

## Auth

- 🟥 **Session expiry on the magic-link flow** (~2 hr). Links currently never
  expire once issued.
- 🟧 **Rate-limit the login endpoint** (~1 hr). Depends on session expiry
  landing first.
- ⬜ **Passkey support** (~8 hr). No user has asked; the magic link works.

## Billing

- 🟧 **Invoice PDF generation** (~6 hr). Customers ask for it monthly.
- ⬜ **Proration on plan change** (~4 hr).

## Platform

- 🟧 **Move image processing off the request path** (~5 hr). Uploads over 4 MB
  time out.
- ⬜ **Multi-region read replicas** (~20 hr).
- ⬜ **Replace the CSV exporter** (~3 hr).
