"""Run the checker against the real repositories.

Every defect found while designing this standard came from real repos; not one
came from a fixture. Fixtures encode what the author already believes, so this
test is the one that keeps the suite honest. It skips cleanly when the fleet is
absent, so the package stays portable.
"""

import unittest
from pathlib import Path

from project_standard import runner

FLEET = Path.home() / "projects" / "apps"


def fleet_repos():
    if not FLEET.is_dir():
        return []
    return sorted(p for p in FLEET.iterdir() if (p / ".git").exists())


@unittest.skipUnless(fleet_repos(), "fleet not present on this machine")
class TestFleetSmoke(unittest.TestCase):
    def test_every_repo_runs_without_crashing(self):
        for repo in fleet_repos():
            with self.subTest(repo=repo.name):
                report = runner.run(repo)
                self.assertIsInstance(report.findings, list)

    def test_no_checker_reports_an_internal_error(self):
        """An internal error means a checker raised on real input — the exact
        thing fixtures cannot surface."""
        for repo in fleet_repos():
            with self.subTest(repo=repo.name):
                report = runner.run(repo)
                internal = [f for f in report.findings if f.check == "internal"]
                self.assertEqual(internal, [],
                                 f"{repo.name}: {[f.message for f in internal]}")

    def test_ci_profile_runs_everywhere_too(self):
        for repo in fleet_repos():
            with self.subTest(repo=repo.name):
                report = runner.run(repo, profile=runner.CI)
                self.assertIsInstance(report.findings, list)

    def test_every_repo_resolves_a_profile(self):
        for repo in fleet_repos():
            with self.subTest(repo=repo.name):
                ctx = runner.build_ctx(repo)
                self.assertIn(ctx.resolved.profile,
                              ("product", "library", "docs"))
                self.assertTrue(ctx.resolved.channels)


if __name__ == "__main__":
    unittest.main()
