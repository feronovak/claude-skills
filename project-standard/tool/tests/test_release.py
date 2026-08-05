import unittest

from fixtures import TempRepo, by_check, ctx_for, sev_for
from project_standard import release
from project_standard.gitio import Git, parse_tag


class TestTagParsing(unittest.TestCase):
    def test_plain_channel_and_prerelease(self):
        self.assertEqual(parse_tag("v1.2.3"), ("web", (1, 2, 3), None))
        self.assertEqual(parse_tag("android/v1.7.5"), ("android", (1, 7, 5), None))
        self.assertEqual(parse_tag("v1.5.0-pre-mobile"),
                         ("web", (1, 5, 0), "pre-mobile"))
        self.assertIsNone(parse_tag("release-candidate"))


class TestVersionSource(unittest.TestCase):
    def test_single_manifest_is_used(self):
        with TempRepo() as r:
            r.write("package.json", '{"version": "1.5.0"}')
            r.commit()
            self.assertEqual(release.version_source(r.dir, []),
                             ("package.json", "1.5.0"))

    def test_polyglot_picks_the_source_the_tags_corroborate(self):
        """A flat 'npm wins' rule selects the one number no tag agrees with."""
        with TempRepo() as r:
            r.write("package.json", '{"version": "5.0.0"}')
            r.write("VERSION", "0.13.2\n")
            r.write("app.py", "x = 1\n")
            r.commit()
            r.tag("v0.13.2")
            self.assertEqual(release.version_source(r.dir, Git(r.dir).tags()),
                             ("VERSION", "0.13.2"))

    def test_no_corroboration_falls_back_to_the_backend(self):
        with TempRepo() as r:
            r.write("package.json", '{"version": "5.0.0"}')
            r.write("pyproject.toml", '[project]\nname="x"\nversion="0.2.0"\n')
            r.commit()
            self.assertEqual(release.version_source(r.dir, [])[0],
                             "pyproject.toml")

    def test_disagreeing_sources_are_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("VERSION", "0.13.2\n")
            r.write("package.json", '{"version": "5.0.0"}')
            r.commit()
            r.tag("v0.13.2")
            found = by_check(release.check(ctx_for(r.dir)), "5b")
            self.assertTrue(any("disagree" in f.message for f in found))


class TestReleaseGate(unittest.TestCase):
    def test_tag_without_changelog_section_is_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("package.json", '{"version": "1.0.0"}')
            r.write("CHANGELOG.md", "# Changelog\n\n## [0.9.0] - 2026-01-01\n")
            r.commit()
            r.tag("v1.0.0")
            found = by_check(release.check(ctx_for(r.dir)), "5")
            self.assertTrue(any("no `1.0.0` section" in f.message for f in found))

    def test_matching_tag_version_and_changelog_passes(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("package.json", '{"version": "1.0.0"}')
            r.write("CHANGELOG.md", "# Changelog\n\n## [1.0.0] - 2026-01-01\n")
            r.commit()
            r.tag("v1.0.0")
            self.assertEqual(by_check(release.check(ctx_for(r.dir)), "5"), [])

    def test_prerelease_needs_no_changelog_section(self):
        """A pre-release cut released nothing."""
        with TempRepo() as r:
            r.standard_repo()
            r.write("package.json", '{"version": "1.5.0"}')
            r.write("CHANGELOG.md", "# Changelog\n\n## [1.4.0] - 2026-01-01\n")
            r.commit()
            r.tag("v1.5.0-pre-mobile")
            self.assertEqual(by_check(release.check(ctx_for(r.dir)), "5"), [])


class TestRegressions(unittest.TestCase):
    def _repo_with_regression(self, adopted_before):
        """A repo that renumbered downward: v2.2.0 then v1.7.0.

        `adopted_before=True` puts the baseline before the regression (so it is
        a breach); False puts it after (so it is pre-existing history).
        """
        r = TempRepo().__enter__()
        r.standard_repo()
        r.write("package.json", '{"version": "1.7.0"}')
        r.write("CHANGELOG.md", "# Changelog\n\n## [1.7.0] - 2026-07-01\n")
        first = r.commit("chore: one")
        r.tag("v2.2.0")
        r.write("b.txt", "b")
        r.commit("chore: two")
        r.tag("v1.7.0")
        r.write("c.txt", "c")
        later = r.commit("chore: three")
        adopted = first if adopted_before else later
        r.write("CLAUDE.md", r.contract_block(adopted=adopted,
                                              **{"critical-paths": []}))
        r.commit("chore: adopt")
        return r

    def test_regression_after_adopted_is_an_error(self):
        r = self._repo_with_regression(adopted_before=True)
        try:
            self.assertEqual(sev_for(release.check(ctx_for(r.dir)), "38"), "error")
        finally:
            r.__exit__()

    def test_regression_before_adopted_is_a_warn(self):
        """One fact pattern must not be filed as both warn and error."""
        r = self._repo_with_regression(adopted_before=False)
        try:
            findings = release.check(ctx_for(r.dir))
            self.assertEqual(by_check(findings, "38"), [])
            self.assertTrue(any("lower than" in f.message
                                for f in by_check(findings, "15")))
        finally:
            r.__exit__()

    def test_channels_gate_independently(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("package.json", '{"version": "1.7.5"}')
            r.commit("chore: one")
            r.tag("web/v1.7.4")
            r.write("b.txt", "b")
            r.commit("chore: two")
            r.tag("android/v1.7.5")
            findings = release.check(ctx_for(r.dir))
            self.assertEqual(by_check(findings, "38"), [])


class TestUnreleasedAndBumpTable(unittest.TestCase):
    def test_commits_since_tag_without_unreleased_warns(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("package.json", '{"version": "1.0.0"}')
            r.write("CHANGELOG.md", "# Changelog\n\n## [1.0.0] - 2026-01-01\n")
            r.commit("chore: release")
            r.tag("v1.0.0")
            r.write("later.txt", "x")
            r.commit("feat: more work")
            self.assertEqual(sev_for(release.check(ctx_for(r.dir)), "29"), "warn")

    def test_missing_bump_table_is_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/DEVELOPMENT_FLOW.md", "# Flow\n\nWe ship when ready.\n")
            r.commit()
            self.assertEqual(sev_for(release.check(ctx_for(r.dir)), "37"), "error")

    def test_generic_semver_without_a_consumer_warns(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/DEVELOPMENT_FLOW.md",
                    "# Flow\n\n| Bump | When |\n|---|---|\n"
                    "| major | breaking change |\n| minor | new feature |\n"
                    "| patch | bug fix |\n")
            r.commit()
            self.assertEqual(sev_for(release.check(ctx_for(r.dir)), "37b"), "warn")

    def test_consumer_named_passes(self):
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            self.assertEqual(by_check(release.check(ctx_for(r.dir)), "37b"), [])


if __name__ == "__main__":
    unittest.main()
