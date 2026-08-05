import unittest

from fixtures import TempRepo, by_check, ctx_for, sev_for
from project_standard import hygiene

# Every marker the harness can append. Guarding only the first leaves the rule
# half-enforced, and the session line is the one that actually got through.
MARKERS = [
    ("8a", "Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"),
    ("8b", "Claude-Session: https://claude.ai/code/session_018abc"),
    ("8c", "Signed-off-by: Claude <noreply@anthropic.com>"),
    ("8e", "🤖 Generated with [Claude Code](https://claude.com/claude-code)"),
]


def repo_with_marker(marker, adopted_first=True):
    r = TempRepo().__enter__()
    r.standard_repo()
    base = r.commit("chore: base")
    r.write("later.txt", "x")
    r.commit(f"feat: work\n\n{marker}")
    adopted = base if adopted_first else "HEAD"
    r.write("CLAUDE.md", r.contract_block(adopted=adopted,
                                          **{"critical-paths": []}))
    r.commit("chore: adopt")
    return r


class TestAttribution(unittest.TestCase):
    def test_each_marker_after_the_baseline_is_an_error(self):
        for check_id, marker in MARKERS:
            with self.subTest(check=check_id):
                r = repo_with_marker(marker)
                try:
                    findings = hygiene.check(ctx_for(r.dir))
                    self.assertEqual(sev_for(findings, check_id), "error",
                                     f"{check_id} should be an error")
                finally:
                    r.__exit__()

    def test_markers_before_the_baseline_are_warns(self):
        r = TempRepo().__enter__()
        try:
            r.standard_repo()
            r.commit("feat: old\n\nCo-Authored-By: Claude <noreply@anthropic.com>")
            head = r.git("rev-parse", "HEAD")
            r.write("CLAUDE.md", r.contract_block(adopted=head,
                                                  **{"critical-paths": []}))
            r.commit("chore: adopt")
            findings = hygiene.check(ctx_for(r.dir))
            self.assertEqual(by_check(findings, "8a"), [])
            self.assertEqual(sev_for(findings, "14"), "warn")
        finally:
            r.__exit__()

    def test_claude_author_identity_is_an_error(self):
        r = TempRepo().__enter__()
        try:
            r.standard_repo()
            base = r.commit("chore: base")
            r.write("x.txt", "x")
            r.commit("feat: work",
                     author="Claude Opus 5 <noreply@anthropic.com>")
            r.write("CLAUDE.md", r.contract_block(adopted=base,
                                                  **{"critical-paths": []}))
            r.commit("chore: adopt")
            self.assertEqual(sev_for(hygiene.check(ctx_for(r.dir)), "8d"), "error")
        finally:
            r.__exit__()

    def test_clean_history_produces_no_attribution_error(self):
        with TempRepo() as r:
            r.standard_repo()
            base = r.commit("chore: base")
            r.write("CLAUDE.md", r.contract_block(adopted=base,
                                                  **{"critical-paths": []}))
            r.commit("chore: adopt")
            findings = hygiene.check(ctx_for(r.dir))
            for check_id, _ in MARKERS:
                self.assertEqual(by_check(findings, check_id), [])
            self.assertEqual(by_check(findings, "8d"), [])


class TestLocalOnly(unittest.TestCase):
    def test_tracked_local_only_path_is_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/exec-summaries/2026-08-01.md", "# summary\n")
            r.commit()
            found = by_check(hygiene.check(ctx_for(r.dir)), "7")
            self.assertTrue(any(f.severity == "error" for f in found))

    def test_exec_summary_by_pattern_is_a_warn(self):
        """Exact paths catch the convention; a summary written outside it needs
        a pattern, and a filename is a hint rather than proof."""
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/EXECUTIVE-SUMMARY.md", "# summary\n")
            r.commit()
            found = [f for f in by_check(hygiene.check(ctx_for(r.dir)), "7")
                     if f.severity == "warn"]
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].path, "docs/EXECUTIVE-SUMMARY.md")

    def test_gitignore_block_only_required_when_opted_in(self):
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            self.assertEqual(by_check(hygiene.check(ctx_for(r.dir)), "9"), [])

    def test_opted_in_repo_missing_entries_is_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write(".gitignore", hygiene.MARKER_LINE + "\nlogs/\n")
            r.commit()
            self.assertEqual(sev_for(hygiene.check(ctx_for(r.dir)), "9"), "error")

    def test_opted_in_repo_with_full_block_passes(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write(".gitignore", hygiene.MARKER_LINE + "\n"
                    + "\n".join(hygiene.LOCAL_ONLY) + "\n")
            r.commit()
            self.assertEqual(by_check(hygiene.check(ctx_for(r.dir)), "9"), [])


class TestHooks(unittest.TestCase):
    def test_hooks_path_without_guards_is_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            found = by_check(hygiene.check(ctx_for(r.dir)), "11b")
            self.assertTrue(found, "an override pointing at an empty dir must fail")
            self.assertEqual(found[0].severity, "error")

    def test_hooks_path_with_both_guards_passes(self):
        with TempRepo() as r:
            r.standard_repo()
            hooks = r.dir / ".nohooks"
            (hooks / "pre-commit").write_text("#!/bin/bash\nexit 0\n")
            (hooks / "commit-msg").write_text("#!/bin/bash\nexit 0\n")
            r.commit()
            findings = hygiene.check(ctx_for(r.dir))
            self.assertEqual(by_check(findings, "11"), [])
            self.assertEqual(by_check(findings, "11b"), [])


if __name__ == "__main__":
    unittest.main()
