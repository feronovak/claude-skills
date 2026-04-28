# Update & Amendment Protocol

The user may invoke /brainstormers-idea to UPDATE an existing brainstorm rather than start fresh. Detect this when:
- The user says "add X to [existing project]", "update [project] with...", or references an existing project folder
- The {project-folder} already exists with completed section files

---

## Update Mode (not a full re-run)

1. Read `00-idea-brief.md` and the user's new information to understand the scope of the change.

2. Classify the update:

   - **BRIEF-ONLY** (e.g., "I forgot to mention I have an existing audience of 10K"): Update `00-idea-brief.md` with the new information. Then assess which researchers' findings would materially change — only re-run those + idea-architect.

   - **SECTION-SPECIFIC** (e.g., "I found a new competitor" or "dig deeper into the timing"): Spin up the relevant researcher with `00-idea-brief.md` + their existing section file + the new information. The researcher OVERWRITES their section. Then idea-architect re-synthesizes `05` and `06`.

   - **DIRECTION CHANGE** (e.g., "I want to pivot from B2C to B2B" or "let's focus on a different audience"): Update `00-idea-brief.md` with the new direction. Re-run all 4 researchers + idea-architect. This is effectively a full re-run in the same folder.

3. For BRIEF-ONLY and SECTION-SPECIFIC updates: only spin up the affected researchers. Re-running all 4 wastes time and tokens when only one angle changed.

4. After any update, idea-architect must re-read all section files and update both `05-refined-idea.md` and `06-strategy-brief.md`. The Reality Check verdict may change based on new information.

5. Present the updated findings to the user, highlighting what changed: "Based on the new information about [X], the market-explorer updated their analysis. Key changes: [summary]. The Reality Check verdict moved from RECONSIDER to PROMISING because [reason]."

---

## Resuming an Incomplete Brainstorm

If the user returns to a project where some phases completed but not all:
- Check which files exist in `{project-folder}/docs/`
- Resume from where it left off — don't re-run completed phases
- If `00-idea-brief.md` exists but research files are missing, go straight to Phase 2
- If research files exist but `05`/`06` are missing, go straight to Phase 3
