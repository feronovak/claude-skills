"""Enumeration gives the judgement pass a denominator.

Five measured runs over one product map each verified a different subset of its
rows, none found all the false ones, and the run whose instruction demanded
thoroughness most forcefully scored worst while claiming to have checked
everything. Exhortation does not raise recall; a numbered worklist does.
"""

import unittest
from pathlib import Path

from fixtures import TempRepo, ctx_for
from project_standard import claims


class TestProductMapUnits(unittest.TestCase):

    def test_every_table_row_becomes_a_claim(self):
        text = ("# Product map\n\n"
                "| Feature | State |\n|---|---|\n"
                "| Confidence scoring | LIVE |\n"
                "| Vision read | LIVE |\n")
        units = claims.units_for("docs/FEATURE_MAP.md", text)
        self.assertEqual(["Confidence scoring", "Vision read"],
                         [u.label for u in units])
        self.assertEqual({"claim"}, {u.kind for u in units})

    def test_the_header_row_is_not_a_claim(self):
        text = "| Feature | State |\n|---|---|\n| Only row | LIVE |\n"
        self.assertEqual(1, len(claims.units_for("docs/FEATURE_MAP.md", text)))

    def test_line_numbers_point_at_the_row(self):
        text = "# Map\n\n| A | B |\n|---|---|\n| first | x |\n| second | y |\n"
        units = claims.units_for("docs/FEATURE_MAP.md", text)
        self.assertEqual([5, 6], [u.line for u in units])

    def test_a_scaffolded_row_is_not_counted_as_a_claim(self):
        # The template ships one placeholder row. Counting it would put a unit
        # on the worklist that exists only to be replaced.
        text = ("| Feature | State |\n|---|---|\n"
                "| `<!-- TODO(project-standard) -->` | unverified |\n")
        self.assertEqual([], claims.units_for("docs/FEATURE_MAP.md", text))

    def test_a_table_without_a_separator_yields_nothing(self):
        text = "| not | really | a table |\n"
        self.assertEqual([], claims.units_for("docs/FEATURE_MAP.md", text))


class TestUnitsDifferByDocument(unittest.TestCase):
    """What verifying means is not the same for every slot."""

    def test_a_backlog_item_is_checked_for_being_open(self):
        text = "# Next steps\n\n## Open\n\n- ship the thing\n- fix the bug\n"
        units = claims.units_for("docs/NEXT_STEPS.md", text)
        self.assertEqual(2, len(units))
        self.assertIn("still open", units[0].verify)

    def test_a_prd_is_never_checked_against_the_code(self):
        # A PRD is intent. Asking whether a proposal is true of the code today
        # would reject every PRD worth writing.
        text = ("# Thing\n\n**Status:** draft\n**Backlog:** none\n"
                "**Owner:** someone\n\n## Problem\n\nreal prose here\n")
        units = claims.units_for("docs/prds/thing.md", text)
        self.assertTrue(units)
        for u in units:
            self.assertNotIn("implementation", u.verify)
            self.assertNotIn("code", u.verify)

    def test_a_prd_section_still_holding_a_token_is_a_unit(self):
        text = ("# Thing\n\n**Status:** draft\n\n## Problem\n\n"
                "<!-- TODO(project-standard): who hurts -->\n")
        kinds = {u.kind for u in claims.units_for("docs/prds/thing.md", text)}
        self.assertIn("prd-section", kinds)

    def test_a_changelog_release_is_checked_against_its_tag(self):
        text = "# Changelog\n\n## [1.2.0] - 2026-01-01\n\n- thing\n"
        units = claims.units_for("CHANGELOG.md", text)
        self.assertEqual(["v1.2.0"], [u.label for u in units])
        self.assertIn("tag", units[0].verify)

    def test_a_code_map_row_is_checked_for_the_path_and_the_responsibility(self):
        text = "| Path | What |\n|---|---|\n| `src/` | the app |\n"
        units = claims.units_for("docs/PROJECT_MAP.md", text)
        self.assertEqual("mapping", units[0].kind)
        self.assertIn("responsibility", units[0].verify)


class TestScope(unittest.TestCase):

    def test_only_the_standards_own_documents_are_counted(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("tests/fixtures/README.md", "# helper\n")
            r.write("vendor/thing/CHANGELOG.md", "## [9.9.9] - 2026-01-01\n")
            r.commit()
            units, skipped = claims.enumerate_repo(ctx_for(r.dir))
            counted = set(units) | set(skipped)
            self.assertNotIn("tests/fixtures/README.md", counted)
            self.assertNotIn("vendor/thing/CHANGELOG.md", counted)

    def test_a_document_with_no_countable_unit_says_so(self):
        # Absence from the worklist must not read as "nothing to check here".
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            _, skipped = claims.enumerate_repo(ctx_for(r.dir))
            self.assertIn("README.md", skipped)
            self.assertTrue(skipped["README.md"])

    def test_prds_are_in_scope(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/prds/thing.md", "# Thing\n\n**Status:** draft\n")
            r.commit()
            units, _ = claims.enumerate_repo(ctx_for(r.dir))
            self.assertIn("docs/prds/thing.md", units)

    def test_an_untracked_document_is_not_enumerated(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write(".gitignore", "docs/FEATURE_MAP.md\n")
            r.commit()
            (r.dir / "docs/FEATURE_MAP.md").write_text(
                "| A | B |\n|---|---|\n| x | y |\n")
            units, _ = claims.enumerate_repo(ctx_for(r.dir))
            self.assertNotIn("docs/FEATURE_MAP.md", units)


class TestTheMissThisExistsToPrevent(unittest.TestCase):
    """The measured failure, reproduced as a fixture.

    A product map carrying a row whose claim is false, among many rows that are
    fine. Every spot-checking run reported the rows it happened to read; the
    worklist puts a number on the row instead.
    """

    def test_the_row_that_five_runs_sampled_differently_is_enumerated(self):
        rows = "\n".join(f"| Feature {i} | LIVE |" for i in range(40))
        text = ("# Product map\n\n| Feature | State |\n|---|---|\n" + rows +
                "\n| Confidence scoring | HIGH/MEDIUM/LOW from data "
                "completeness, validation, price availability |\n")
        units = claims.units_for("docs/FEATURE_MAP.md", text)
        self.assertEqual(41, len(units))
        self.assertEqual("Confidence scoring", units[-1].label)


if __name__ == "__main__":
    unittest.main()
