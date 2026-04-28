# Update & Amendment Protocol

The user may invoke /business-sharks to UPDATE an existing analysis rather than create a new one. Detect this when:
- The user says "add X to [existing project]", "update [project] with...", or references an existing project folder
- The {project-folder} already exists with completed section files

---

## Update Mode (not a full re-run)

1. Read `00-business-idea.md` and the user's new information to understand the scope of the change.

2. Classify the update:

   - **SCORE-ONLY** (e.g., "team grew from 1 to 3 people"): Spin up chief-shark to update affected section files (09, 11, 12, 13, 14, 15). No Phase 1 re-run needed.
   - **SECTION-SPECIFIC** (e.g., "new competitor launched"): Spin up the relevant Phase 1 analyst + chief-shark. The analyst overwrites their section(s), then chief-shark re-synthesizes.
   - **FULL RE-RUN** (e.g., "we pivoted the entire business model"): Treat as a new analysis in the same folder. Run full Phase 1 + Phase 2.

3. For SCORE-ONLY and SECTION-SPECIFIC updates: do NOT spin up all 4 Phase 1 agents. Only spin up what's needed.

4. After the update, chief-shark must recalculate the composite average, re-evaluate the verdict, and update `12-scorecard.md` and `13-executive-summary.md`.

5. The scorecard shows current scores only (not version history columns). Add a brief note at the top: "Updated [date]: [what changed]."

---

## Cross-Project Context

When analyzing a product that is part of a portfolio or ecosystem:

- Check if a `team.md` file exists in the parent directory (e.g., `_ideas/team.md`). If it does, read it for team composition and shared context.
- Check if other project folders exist alongside this one. If the user mentions an ecosystem or portfolio, reference other analyses by folder name but do NOT re-analyze them.
- If the user has a separate ecosystem analysis (e.g., `<your-ecosystem>/`), individual product analyses should note their ecosystem role but score STANDALONE viability. The ecosystem analysis handles the portfolio view.
- If ecosystem context is detected, trigger Part C of the YC evaluation (see chief-shark responsibilities, section 4).
