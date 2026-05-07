# Update & Amendment Protocol

The user may invoke /brainstormers-content to UPDATE an existing content research rather than start fresh. Detect this when:
- The user says "add X to [existing brief]", "update with...", or references an existing output directory
- The `{output-dir}` already exists with completed research files

---

## Update Mode (not a full re-run)

1. Read `00-brief.md` and the user's new information to understand the scope of the change.

2. Classify the update:

   - **ANGLE SHIFT** (e.g., "actually focus more on the leadership angle" or "narrow to just AI tools"): Update `00-brief.md` with the refined angle. Re-run all 3 researchers + content-strategist.

   - **NEW INFORMATION** (e.g., "I just gave a talk about X" or "we launched a new product"): Update the user profile in `00-brief.md`. Then re-run content-strategist only — the trends and audience data haven't changed, but the Authenticity scores might shift with new experience.

   - **REFRESH** (e.g., "it's been a few weeks, update the trends"): Re-run trend-scanner only, then content-strategist re-synthesizes. Audience demand and competitive content change slowly; trends change fast.

3. For all updates: content-strategist must re-read all files and regenerate `04-recommendations.md`. Scores may change based on new information.

4. Present updated findings highlighting what changed: "After updating your profile with [X], recommendation #3 moved from Authenticity 5 to 8 — it's now your top pick."

---

## Resuming Incomplete Research

If the user returns to a brief where some phases completed but not all:
- Check which files exist in `{output-dir}`
- Resume from where it left off
- If `00-brief.md` exists but research files are missing, go straight to Phase 1
- If research files exist but `04-recommendations.md` is missing, go straight to Phase 2
