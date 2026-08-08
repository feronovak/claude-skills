# The release plan

Produced at step 3, for the **Musts and Shoulds only**. Coulds are not ordered
— by definition nothing depends on them.

## The three readiness states

| State | Means |
|---|---|
| `ready` | Can start now. Nothing blocks it and nothing needs designing first. |
| `blocked by <n>` | Depends on another item **in this release**, named by its row number. |
| `needs spec` | Non-trivial, and no `docs/prds/<name>.md` exists for it. |

An item blocked by something **outside** this release is not `blocked by`. Never record an unsatisfiable dependency — say what is actually true:

- **A Must that cannot ship** means either the blocker belongs in the release or this item does not. Force that question.
- **A Should that cannot ship** drops out of the build order. Its absence is a disappointment, not a failure, so it does not force the release open. Name it under `Gaps:` with what blocks it — dropping it silently is the one thing this rule exists to prevent.

## Output format

```
Release 1.5.0 — build order

1. Expire share links after 30 days         ready
2. Revoke links on password reset           blocked by 1
3. Compress uploads in a worker             needs spec
4. Weekly summary email                     ready · parallel with 1

Gaps: 1 Must has no PRD (item 3).
      1 Should dropped — team billing seats needs the
      billing migration, which is not in this release.
```

Order is dependency order, not importance order — importance was already
settled by the letter. Where two items are independent, say so with
`· parallel with <n>`; a reader who does not know they can be done at once will
serialise them for no reason.

## The `needs spec` judgment

This is the weakest call in the skill, and it must behave like it knows that.

An item needs a spec when it is non-trivial **and** has no PRD. "Non-trivial"
means the work has open design questions — not merely that it is large. A
20-hour migration with one obvious path needs no spec; a 3-hour change to how
pricing is calculated does.

Three rules:

1. **State the reason.** Never just `needs spec` — say what is undecided.
2. **It is overruled in the same free-text pass as everything else.** The user
   saying "3 is fine, just build it" ends the matter without argument.
3. **Never hand off without agreement.** `brainstorming` is offered, never
   invoked on the user's behalf. Routing work to a design session the user did
   not ask for is the failure mode this rule prevents.

## What this is not

This is not an implementation plan. It says *which items, in what order, and
which cannot start yet*. How to build any one of them is `writing-plans`, at a
different altitude, invoked separately and per item.
