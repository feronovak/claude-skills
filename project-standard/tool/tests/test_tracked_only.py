"""The verdict is a property of the commit, not of anyone's disk.

The spec's scoping rule — "tracked, not the filesystem" — was stated once and
then broken in the profile classifier, which sits upstream of every required
slot. A gitignored `package.json` turned one commit into two different
verdicts: 3 errors as a docs repo on a clean clone, 9 as a product on the
machine that had the stray file.

`TestInvocationIndependence` varied the working *directory*; nothing varied the
working *tree*, which is why this survived two review passes.
"""

import unittest
from pathlib import Path

from fixtures import TempRepo, by_check, ctx_for
from project_standard import detect, release, runner, vendored


class TestUntrackedFilesCannotChangeTheVerdict(unittest.TestCase):

    def test_a_gitignored_manifest_does_not_flip_the_profile(self):
        with TempRepo() as r:
            r.write("README.md", "# demo\n")
            r.write(".gitignore", "package.json\n")
            r.commit()
            before = ctx_for(r.dir).resolved.profile

            # Never tracked, and git is configured to ignore it.
            (r.dir / "package.json").write_text('{"name":"x","version":"1.0.0"}')
            after = ctx_for(r.dir).resolved.profile

            self.assertEqual(before, after,
                             "an untracked manifest changed the profile")
            self.assertEqual("docs", after)

    def test_a_gitignored_manifest_does_not_change_the_findings(self):
        with TempRepo() as r:
            r.write("README.md", "# demo\n")
            r.write(".gitignore", "package.json\n")
            r.commit()
            before = sorted(f.render() for f in runner.run(r.dir).findings)
            (r.dir / "package.json").write_text('{"name":"x","version":"9.9.9"}')
            after = sorted(f.render() for f in runner.run(r.dir).findings)
            self.assertEqual(before, after)

    def test_an_untracked_manifest_supplies_no_version(self):
        with TempRepo() as r:
            r.write("README.md", "# demo\n")
            r.write(".gitignore", "VERSION\n")
            r.commit()
            (r.dir / "VERSION").write_text("4.5.6\n")
            self.assertEqual([], release.candidates(r.dir, ctx_for(r.dir).tracked))

    def test_a_tracked_manifest_still_counts(self):
        # The gate must not swing the other way and start ignoring real files.
        with TempRepo() as r:
            r.write("README.md", "# demo\n")
            r.write("package.json", '{"name":"x","version":"1.2.3"}')
            r.commit()
            ctx = ctx_for(r.dir)
            self.assertIn("package.json", detect.manifests(r.dir, ctx.tracked))
            self.assertEqual(("package.json", "1.2.3"),
                             release.version_source(r.dir, [], ctx.tracked))

    def test_an_untracked_secret_scanner_config_does_not_silence_check_40(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write(".gitignore", ".gitleaks.toml\n")
            r.commit()
            (r.dir / ".gitleaks.toml").write_text("[allowlist]\n")
            hits = by_check(runner.run(r.dir).findings, "40")
            self.assertTrue(hits, "an untracked scanner config silenced check 40")

    def test_an_untracked_direction_doc_does_not_satisfy_the_slot(self):
        with TempRepo() as r:
            r.standard_repo(direction="docs/NORTH_STAR.md")
            r.write(".gitignore", "docs/NORTH_STAR.md\n")
            r.commit()
            (r.dir / "docs").mkdir(exist_ok=True)
            (r.dir / "docs/NORTH_STAR.md").write_text("# North star\n")
            hits = by_check(runner.run(r.dir).findings, "30")
            self.assertTrue(hits, "an untracked direction doc satisfied check 30")

    def test_a_link_to_an_untracked_file_is_broken(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/PROJECT_MAP.md", "# Code map\n\n[gone](secret.md)\n")
            r.write(".gitignore", "docs/secret.md\n")
            r.commit()
            (r.dir / "docs/secret.md").write_text("# Secret\n")
            hits = by_check(runner.run(r.dir).findings, "4")
            self.assertTrue(hits, "a link to an untracked file resolved")

    def test_a_link_to_a_directory_still_resolves(self):
        # Git tracks no directories, so the tracked-only rule must not turn
        # every directory link into a false broken-link finding.
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/PROJECT_MAP.md", "# Code map\n\n[prds](prds)\n")
            r.write("docs/prds/thing.md", "# Thing\n\n**Status:** draft\n")
            r.commit()
            hits = [f for f in by_check(runner.run(r.dir).findings, "4")
                    if "prds" in f.message]
            self.assertEqual([], hits, "a link to a tracked directory read broken")


class TestVendoredDrift(unittest.TestCase):
    """Check 17 — and the reason it compares content, not just the version."""

    def _vendor(self, r, mutate=None, version=None):
        import shutil
        src = Path(vendored.__file__).resolve().parent
        dst = r.dir / "scripts" / "project_standard"
        dst.mkdir(parents=True, exist_ok=True)
        for path in src.glob("*.py"):
            shutil.copy2(path, dst / path.name)
        if version is not None:
            init = dst / "__init__.py"
            init.write_text(init.read_text().replace(
                f'VERSION = "{vendored.VERSION}"', f'VERSION = "{version}"'))
        if mutate:
            mutate(dst)
        r.commit()
        return dst

    def test_an_identical_copy_is_silent(self):
        with TempRepo() as r:
            r.standard_repo()
            self._vendor(r)
            self.assertEqual([], by_check(vendored.check(ctx_for(r.dir)), "17"))

    def test_a_copy_at_an_older_version_is_reported(self):
        with TempRepo() as r:
            r.standard_repo()
            self._vendor(r, version="0.0.1")
            hits = by_check(vendored.check(ctx_for(r.dir)), "17")
            self.assertTrue(hits)
            self.assertIn("0.0.1", hits[0].message)

    def test_a_copy_that_differs_at_the_same_version_is_reported(self):
        # The failure measured on the real fleet: nine modules changed, the
        # version string untouched. A version-only comparison calls this
        # current, which is worse than not checking at all.
        with TempRepo() as r:
            r.standard_repo()

            def drop_a_module(dst):
                (dst / "baselines.py").unlink()

            self._vendor(r, mutate=drop_a_module)
            hits = by_check(vendored.check(ctx_for(r.dir)), "17")
            self.assertTrue(hits, "same-version drift went unreported")
            self.assertIn("same version", hits[0].message)
            self.assertIn("baselines.py", hits[0].message)

    def test_a_repo_with_no_vendored_copy_is_silent(self):
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            self.assertEqual([], by_check(vendored.check(ctx_for(r.dir)), "17"))

    def test_an_untracked_vendored_copy_is_not_examined(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write(".gitignore", "scripts/\n")
            r.commit()
            self._vendor(r, version="0.0.1")
            self.assertEqual([], by_check(vendored.check(ctx_for(r.dir)), "17"))


if __name__ == "__main__":
    unittest.main()
