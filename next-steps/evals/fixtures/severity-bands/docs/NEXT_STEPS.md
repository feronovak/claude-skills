# Next steps — the single forward doc

> **The `P0`–`P3` bands are SEVERITY, not release scope.** A row sits in the band whose
> meaning is true of it. **Never move a row between bands to record that it is in or out of a
> release** — that makes the file assert something false about the consequence of leaving it
> undone. Release scope lives in `## Release 2.4.0` below.

## P0 — a buyer is shown a price that is wrong

- [ ] Currency rounding drops the minor unit on JPY listings (~4 hr)
- [ ] Bid increments computed from the stale reserve after an edit (~6 hr)

## P1 — a buyer is blocked from acting

- [ ] Watchlist page times out over 200 items (~5 hr)
- [ ] Sign-in link expires before the email arrives on slow relays (~3 hr)

## P2 — a seller is inconvenienced, nothing is misstated

- [ ] Bulk listing upload rejects the whole file on one bad row (~8 hr)
- [ ] Photo reordering loses position after a failed save (~2 hr)

## P3 — nothing breaks and nobody is misled

- [ ] Collapse the duplicate date-format helpers (~2 hr)
- [ ] Drop the unused legacy CSV exporter (~1 hr)

## Release 2.4.0

Nothing scoped yet.
