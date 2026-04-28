# Update & Amendment Protocol

The user may invoke /app-factory on an existing project. Detect this when:
- The user references an existing project folder
- `docs/product-spec.md` already exists
- Source code exists in `src/`

---

## Update Types

1. **SPEC CHANGE** (e.g., "add a feature", "change the pricing page"):
   - Strategist updates `docs/product-spec.md`
   - Present changes to user for approval
   - Designer updates affected docs
   - Engineer implements changes
   - QA re-tests affected areas only
   - Skip Phase 3 unless changes are major

2. **FIX ISSUES** (e.g., "fix the issues from the review"):
   - Read existing `docs/review-*.md` files
   - Send fix tasks to engineer
   - Re-run affected reviewers only

3. **REBUILD** (e.g., "start the build over with this new spec"):
   - Treat as a fresh build but in the same folder
   - Preserve `docs/product-spec.md` if still valid

---

## Resuming Incomplete Builds

Check what exists:
- Only `docs/product-spec.md` → resume from Phase 2 (designer)
- Design docs exist but no `src/` → resume from engineer
- Source code exists but no reviews → resume from Phase 3
- Reviews exist with issues → resume fix loop
