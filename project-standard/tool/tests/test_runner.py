import json
import tempfile
import unittest
from pathlib import Path

from fixtures import TempRepo, ctx_for
from project_standard import cli, docmap, runner
from project_standard.findings import ERROR, SKIPPED, WARN, Report, error, warn


class TestReport(unittest.TestCase):
    def test_error_sets_exit_one_and_warn_does_not(self):
        self.assertEqual(Report([warn("1", "x")]).exit_code, 0)
        self.assertEqual(Report([error("1", "x")]).exit_code, 1)

    def test_skipped_never_fails(self):
        from project_standard.findings import skipped
        self.assertEqual(Report([skipped("11", "no hooks on a runner")]).exit_code, 0)

    def test_ranking_puts_errors_first(self):
        rep = Report([warn("2", "w"), error("9", "e")])
        self.assertEqual([f.severity for f in rep.ranked()], [ERROR, WARN])


class TestRunner(unittest.TestCase):
    def test_non_repo_is_refused_not_passed(self):
        d = Path(tempfile.mkdtemp())
        rep = runner.run(d)
        self.assertEqual(rep.exit_code, 1)
        self.assertIn("not a git repository", rep.findings[0].message)

    def test_ci_profile_skips_hook_checks(self):
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            rep = runner.run(r.dir, profile=runner.CI)
            skipped_ids = {f.check for f in rep.findings if f.severity == SKIPPED}
            self.assertIn("11", skipped_ids)
            self.assertIn("11b", skipped_ids)

    def test_skipped_checks_emit_no_findings_of_their_own(self):
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            rep = runner.run(r.dir, profile=runner.CI)
            hook_findings = [f for f in rep.findings
                             if f.check in ("11", "11b") and f.severity != SKIPPED]
            self.assertEqual(hook_findings, [])

    def test_dev_profile_skips_nothing(self):
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            rep = runner.run(r.dir, profile=runner.DEV)
            self.assertEqual([f for f in rep.findings if f.severity == SKIPPED], [])

    def test_only_filter_narrows_findings(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/exec-summaries/x.md", "# x\n")
            r.commit()
            rep = runner.run(r.dir, only=["local-only"])
            self.assertTrue(rep.findings)
            self.assertTrue(all("local-only" in f.message.lower()
                                for f in rep.findings))

    def test_a_broken_checker_does_not_hide_the_others(self):
        original = runner.MODULES
        def boom(ctx):
            raise RuntimeError("deliberate")
        try:
            runner.MODULES = (("boom", boom),) + original
            with TempRepo() as r:
                r.standard_repo()
                r.commit()
                rep = runner.run(r.dir)
                self.assertTrue(any(f.check == "internal" for f in rep.findings))
                self.assertTrue(len(rep.findings) > 1)
        finally:
            runner.MODULES = original

    def test_summary_describes_the_resolution(self):
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            text = runner.summary(ctx_for(r.dir))
            self.assertIn("product", text)
            self.assertIn("channels=web", text)


class TestDocmap(unittest.TestCase):
    def test_output_is_byte_identical_across_runs(self):
        """A single run date would make the freshness check permanently red."""
        with TempRepo() as r:
            r.standard_repo()
            for name in ("A", "B", "C"):
                r.write(f"docs/{name}.md",
                        f"# {name}\n\n**Last reviewed:** 2026-08-01\n")
            r.commit()
            first = docmap.render(ctx_for(r.dir))
            second = docmap.render(ctx_for(r.dir))
            self.assertEqual(first, second)

    def test_three_states_are_distinguished(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/S.md", "# S\n\n**Last reviewed:** 2026-08-01\n")
            r.write("docs/U.md", "# U\n")
            r.write("docs/K.md", "# K\n\n**Status:** scaffolded\n")
            r.commit()
            text = docmap.render(ctx_for(r.dir))
            self.assertIn("| stamped |", text)
            self.assertIn("| unstamped |", text)
            self.assertIn("| scaffolded |", text)

    def test_stale_docmap_is_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/DOCMAP.md", "# Documentation map\n\nstale\n")
            r.commit()
            findings = docmap.check(ctx_for(r.dir))
            self.assertEqual(findings[0].check, "3")
            self.assertEqual(findings[0].severity, ERROR)

    def test_freshly_generated_docmap_matches(self):
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            text = docmap.render(ctx_for(r.dir))
            r.write("docs/DOCMAP.md", text)
            r.commit()
            # regenerating with DOCMAP now tracked must still agree
            r.write("docs/DOCMAP.md", docmap.render(ctx_for(r.dir)))
            r.commit()
            self.assertEqual(docmap.check(ctx_for(r.dir)), [])


class TestCli(unittest.TestCase):
    def test_json_output_is_parseable(self):
        import contextlib, io
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                cli.main(["check", "--repo", str(r.dir), "--json"])
            payload = json.loads(buf.getvalue())
            self.assertEqual(len(payload), 1)
            self.assertIn("findings", payload[0])

    def test_generate_writes_docmap(self):
        import contextlib, io
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            with contextlib.redirect_stdout(io.StringIO()):
                cli.main(["generate", "--repo", str(r.dir)])
            self.assertTrue((r.dir / "docs/DOCMAP.md").is_file())

    def test_routes_without_app_explains_why(self):
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            code = cli.main(["routes", "--repo", "."])
        self.assertEqual(code, 2)
        self.assertIn("--app is required", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
