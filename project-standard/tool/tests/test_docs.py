import unittest

from fixtures import TempRepo, by_check, ctx_for, sev_for
from project_standard import docs

# Real paths from the fleet that a naive filename match flags as a second
# backlog. None of them is one.
EXCLUDED_CASES = [
    ".github/ISSUE_TEMPLATE/todo.md",
    "implementation/archived/v3.2.0/NEXT_STEPS_PLAN.md",
    "project-management/archives/v5.10/NEXT_STEPS_ANALYSIS.md",
    "docs/done/ROADMAP.md",
    "docs/superpowers/plans/2026-01-01-todo.md",
    "next-steps/evals/fixtures/two-backlogs/ROADMAP.md",
    "next-steps/evals/fixtures/two-backlogs/docs/NEXT_STEPS.md",
]


class TestDuplicateDocuments(unittest.TestCase):
    def test_excluded_directories_never_trigger_duplicate_backlog(self):
        for path in EXCLUDED_CASES:
            with self.subTest(path=path), TempRepo() as r:
                r.standard_repo()
                r.write(path, "# Roadmap\n\n- [ ] a thing\n")
                r.commit()
                self.assertEqual(by_check(docs.check(ctx_for(r.dir)), "26"), [],
                                 f"{path} should be carved out")

    def test_live_second_backlog_is_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/ROADMAP.md", "# Roadmap\n")
            r.commit()
            self.assertEqual(sev_for(docs.check(ctx_for(r.dir)), "26"), "error")

    def test_todo_beside_next_steps_is_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/TODO.md", "# Todo\n")
            r.commit()
            self.assertEqual(sev_for(docs.check(ctx_for(r.dir)), "26"), "error")

    def test_two_product_truth_docs_warn(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/PRODUCT.md", "# Product\n")
            r.commit()
            self.assertEqual(sev_for(docs.check(ctx_for(r.dir)), "18"), "warn")


class TestScaffoldingTokens(unittest.TestCase):
    def test_token_in_required_doc_is_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/FEATURE_MAP.md",
                    "# Product map\n\n<!-- TODO(project-standard): list features -->\n")
            r.commit()
            found = by_check(docs.check(ctx_for(r.dir)), "23")
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].severity, "error")
            self.assertEqual(found[0].path, "docs/FEATURE_MAP.md")

    def test_scaffolded_plus_stamp_is_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/FEATURE_MAP.md",
                    "# Product map\n\n**Status:** scaffolded\n"
                    "**Last reviewed:** 2026-08-01\n")
            r.commit()
            self.assertEqual(sev_for(docs.check(ctx_for(r.dir)), "25"), "error")

    def test_stamp_coverage_is_reported_as_a_metric(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/A.md", "# A\n\n**Last reviewed:** 2026-08-01\n")
            r.write("docs/B.md", "# B\n")
            r.commit()
            found = by_check(docs.check(ctx_for(r.dir)), "12")
            self.assertEqual(found[0].severity, "warn")
            self.assertIn("/", found[0].message)


class TestLinks(unittest.TestCase):
    def test_broken_link_in_required_doc_is_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/PROJECT_MAP.md", "# Code map\n\n[gone](./missing.md)\n")
            r.commit()
            self.assertEqual(sev_for(docs.check(ctx_for(r.dir)), "4"), "error")

    def test_broken_link_elsewhere_is_a_warn(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/notes.md", "# Notes\n\n[gone](./missing.md)\n")
            r.commit()
            self.assertEqual(sev_for(docs.check(ctx_for(r.dir)), "19"), "warn")

    def test_resolving_relative_links_upward(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/PROJECT_MAP.md", "# Code map\n\n[readme](../README.md)\n")
            r.commit()
            self.assertEqual(by_check(docs.check(ctx_for(r.dir)), "4"), [])

    def test_external_and_anchor_links_are_ignored(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/PROJECT_MAP.md",
                    "# Code map\n\n[a](https://example.com) [b](#section)\n")
            r.commit()
            self.assertEqual(by_check(docs.check(ctx_for(r.dir)), "4"), [])


class TestCodeMapPaths(unittest.TestCase):
    def test_naming_a_path_that_does_not_exist_is_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/PROJECT_MAP.md",
                    "# Code map\n\n- `src/` the app\n- `nope/gone/` removed\n")
            r.commit()
            found = by_check(docs.check(ctx_for(r.dir)), "24")
            self.assertEqual(len(found), 1)
            self.assertIn("nope/gone", found[0].message)


class TestRoadmapAndPrds(unittest.TestCase):
    def test_completed_items_in_roadmap_warn_not_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/NEXT_STEPS.md",
                    "# Next steps\n\n- [x] shipped thing\n- [ ] open thing\n")
            r.commit()
            self.assertEqual(sev_for(docs.check(ctx_for(r.dir)), "28"), "warn")

    def test_prd_without_status_is_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/prds/thing.md", "# Thing\n\nA feature.\n")
            r.commit()
            self.assertEqual(sev_for(docs.check(ctx_for(r.dir)), "33"), "error")

    def test_prd_with_status_passes(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/prds/thing.md",
                    "# Thing\n\n**Status:** draft\n**Owner:** someone\n")
            r.commit()
            self.assertEqual(by_check(docs.check(ctx_for(r.dir)), "33"), [])

    def test_prd_outside_the_directory_is_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("PRD-2.4.0.md", "# PRD\n\n**Status:** draft\n")
            r.commit()
            self.assertEqual(sev_for(docs.check(ctx_for(r.dir)), "32"), "error")

    def test_untracked_prd_is_invisible(self):
        """Checks read git ls-files, never the filesystem — which is what makes
        a public repo's deliberately gitignored PRDs legal."""
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            r.write("PRD-2.4.0.md", "# PRD\n")
            (r.dir / ".gitignore").write_text("PRD-*.md\n")
            self.assertEqual(by_check(docs.check(ctx_for(r.dir)), "32"), [])

    def test_state_doc_inside_prds_warns(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/prds/implementation-status.md",
                    "# Status\n\n**Status:** shipped v1.0.0\n")
            r.commit()
            self.assertEqual(sev_for(docs.check(ctx_for(r.dir)), "36"), "warn")


if __name__ == "__main__":
    unittest.main()
