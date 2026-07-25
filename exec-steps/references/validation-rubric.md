# Validation rubric

Assign every item exactly one state. When two states are arguable, take the lower one.

## The four states

### Done

Requires a **named artifact you actually looked at**. One of:

- A commit hash containing the change, inside the evidence window.
- A file path confirmed to exist, with content matching the claim.
- A service check you ran that evidences **the change itself** — a version string, the
  changed behaviour. A bare liveness check proves the service is up, not that the new
  build is serving it; on its own that is Partial.
- Test output **you ran during this run**. Output pasted earlier in the conversation
  does not qualify: it may be stale, since later edits can break what passed an hour
  ago. Conversation-quoted output supports at most Partial.

"I made the change" is not an artifact. "I made the change and here is commit `a1b2c3d`
touching that file" is.

### Partial

Started, but the evidence stops short:

- The change exists in the working tree but is **uncommitted** (`git status --short`
  shows it). Uncommitted work is never Done — it is one `git checkout` from gone.
- Some files in a multi-file claim exist, others do not.
- Code is written but the verification the claim depends on (test, deploy, health
  check) has not happened.

### Claimed, unverified

The conversation asserts it is finished and **no artifact was found**. Report it under
this heading, with the claim quoted and the missing evidence named:

> Claimed: bot restarted and receiving messages. No artifact — no commit in window,
> service state not checked.

Do not soften this into Partial. Do not omit it. This state is the highest-value
output of the entire skill.

### Blocked

Not done, with the blocker named and, where known, who or what unblocks it.

## Cases that trip people up

| Situation | State |
|---|---|
| File edited, not committed | Partial |
| Committed, but the test that would prove it was never run | Partial |
| Committed and tests pass | Done |
| "Deployed" with no health check run and none in the conversation | Claimed, unverified |
| Doc written and committed | Done — a doc's artifact is the file itself |
| Decision made, nothing to build | Done, if the decision is recorded somewhere; otherwise Claimed, unverified |
| Work described in the conversation but explicitly deferred | Not an item — it belongs in Next Steps |
| Not a git repository at all | Everything needing a commit → Claimed, unverified |
| Test passed earlier in the conversation, not re-run now | Partial |
| Service returns 200 but nothing proves the new build is live | Partial |
| Evidence lives outside this repo by design — a deploy to a remote host, a change in another repo | **Out of scope for this run.** List it separately with where the evidence lives. Do not label it unverified: it was never in this run's reach, and treating it as suspect is its own kind of dishonesty. |

## The upgrade prohibition

Never move an item to a higher state because:

- The summary looks thin without it.
- The user seemed confident it was done.
- It is *probably* fine.
- Almost everything else in the session was verified.

A summary reporting three Done and two Claimed-unverified is a **more useful
document** than one reporting five Done, because the reader knows exactly which two
claims not to repeat in a meeting. Optimise for that reader, not for the appearance
of a productive session.

## Reporting the ratio

The Status section always opens with the count: how many items, and how many reached
Done. If nothing reached Done, say so plainly in the first line. A session that
produced no verifiable output is a real result and the reader needs it.
