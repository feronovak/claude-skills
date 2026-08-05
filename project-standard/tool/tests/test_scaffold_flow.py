"""Scaffold a repository from the templates and judge the result.

Nothing had ever done this. The templates, the baselines and the setup
instructions were each reviewed as prose and never executed together, which is
how a documented baseline that no code read survived three rounds of review.

This test performs the retrofit exactly as SKILL.md describes it and asserts
the outcome the skill promises: not green, but honestly and finitely red, with
a baseline that makes the debt explicit rather than a gate nobody can pass.
"""

import shutil
import unittest
from pathlib import Path

from fixtures import TempRepo, by_check, ctx_for
from project_standard import docmap, runner

TEMPLATES = Path(__file__).resolve().parents[2] / "templates"

# The slot each template fills, as `setup` would place it.
PLACEMENT = {
    "agent-contract.md.tmpl": "CLAUDE.md",
    "PROJECT_MAP.md.tmpl": "docs/PROJECT_MAP.md",
    "FEATURE_MAP.md.tmpl": "docs/FEATURE_MAP.md",
    "NEXT_STEPS.md.tmpl": "docs/NEXT_STEPS.md",
    "DEVELOPMENT_FLOW.md.tmpl": "docs/DEVELOPMENT_FLOW.md",
    "NORTH_STAR.md.tmpl": "docs/NORTH_STAR.md",
    "CHANGELOG.md.tmpl": "CHANGELOG.md",
}


def scaffold(r, declare_baseline=True):
    """Run the documented setup: place every template, generate the index."""
    r.write("README.md", "# Scaffolded\n\nA new project.\n")
    r.write("src/index.ts", "export const x = 1\n")
    for template, target in PLACEMENT.items():
        dest = r.dir / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(TEMPLATES / template, dest)
    r.commit("chore: scaffold the standard")

    head = r.git("rev-parse", "HEAD")
    contract = (r.dir / "CLAUDE.md").read_text()
    contract = contract.replace(
        "adopted: <!-- TODO(project-standard): the commit where this repo "
        "adopted the standard -->", f"adopted: {head}")
    if declare_baseline:
        scaffolded = sum(1 for t in PLACEMENT.values()
                         if "TODO(project-standard)" in (r.dir / t).read_text())
        contract = contract.replace("critical-paths:",
                                    f"scaffold: {scaffolded}\ncritical-paths:")
    r.write("CLAUDE.md", contract)
    r.commit("chore: record the adoption baseline")

    # setup finishes by generating the index — it has no template and only the
    # generator can produce one that check 3 will accept.
    r.write("docs/DOCMAP.md", docmap.render(ctx_for(r.dir)))
    r.commit("docs: generate the documentation map")
    r.write("docs/DOCMAP.md", docmap.render(ctx_for(r.dir)))
    r.commit("docs: regenerate now that the map is itself tracked")
    return r


class TestScaffoldedRepo(unittest.TestCase):
    def test_the_declared_baseline_absorbs_the_scaffolding_debt(self):
        """The promise setup makes: a repo can adopt today and pay down later.

        Without a baseline that check 23 reads, a freshly scaffolded repo exits
        1 on documents the tool itself just wrote, and the gate gets switched
        off on day one.
        """
        with TempRepo() as r:
            scaffold(r, declare_baseline=True)
            report = runner.run(r.dir)
            token_errors = [f for f in report.errors if f.check == "23"]
            self.assertEqual([f.render() for f in token_errors], [])
            self.assertTrue([f for f in report.warns if f.check == "23"],
                            "the debt must still be reported, as a warn")

    def test_without_a_baseline_the_debt_is_an_error(self):
        with TempRepo() as r:
            scaffold(r, declare_baseline=False)
            report = runner.run(r.dir)
            self.assertTrue([f for f in report.errors if f.check == "23"])

    def test_the_generated_index_is_never_itself_flagged(self):
        """A scaffolded heading is `# <!-- TODO... -->`; copying it into the
        generated index put a token inside a file that says do not edit."""
        with TempRepo() as r:
            scaffold(r)
            offenders = [f for f in runner.run(r.dir).findings
                         if f.check == "23" and f.path == "docs/DOCMAP.md"]
            self.assertEqual(offenders, [])

    def test_declaring_what_detection_already_found_is_not_an_override(self):
        """`init` is told to record its answers as declarations. Declaring
        values that agree with detection must not report an override."""
        with TempRepo() as r:
            scaffold(r)
            contract = (r.dir / "CLAUDE.md").read_text()
            r.write("CLAUDE.md", contract.replace(
                "critical-paths:",
                "profile: product\nhttp-api: no\nchannels: [web]\n"
                "critical-paths:"))
            r.commit("chore: record what init asked")
            offenders = [f.render() for f in runner.run(r.dir).findings
                         if f.check in ("2", "6")
                         and ("override" in f.message
                              or "contradicts" in f.message)]
            self.assertEqual(offenders, [])

    def test_a_scaffolded_repo_satisfies_the_contract_sections(self):
        with TempRepo() as r:
            scaffold(r)
            section_errors = [f.render() for f in runner.run(r.dir).errors
                              if f.check == "2"]
            self.assertEqual(section_errors, [])

    def test_the_scaffold_leaves_no_slot_unfilled(self):
        with TempRepo() as r:
            scaffold(r)
            missing = [f.render() for f in runner.run(r.dir).findings
                       if f.check in ("1", "30")]
            self.assertEqual(missing, [])

    def test_the_generated_index_is_accepted_by_its_own_freshness_check(self):
        with TempRepo() as r:
            scaffold(r)
            self.assertEqual(by_check(runner.run(r.dir).findings, "3"), [])


if __name__ == "__main__":
    unittest.main()
