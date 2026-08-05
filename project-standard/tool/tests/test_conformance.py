"""The test that should have existed first.

A checker whose own idea of a conformant repository still reports errors is
telling every user their repo is broken for reasons they cannot fix. This
would have caught three separate defects at once: an always-on hook check a
stranger cannot satisfy, a duplicate-document warning fired by the standard's
own required layout, and a local-only rule that bound repos which never opted
in.
"""

import unittest

from fixtures import TempRepo, ctx_for
from project_standard import docmap, runner


def conformant(r):
    """The smallest repository that satisfies every required slot."""
    r.standard_repo()
    hooks = r.dir / ".nohooks"
    (hooks / "pre-commit").write_text("#!/bin/bash\nexit 0\n")
    (hooks / "commit-msg").write_text("#!/bin/bash\nexit 0\n")
    r.commit("chore: base")
    head = r.git("rev-parse", "HEAD")
    r.write("CLAUDE.md", r.contract_block(adopted=head,
                                          **{"critical-paths": []}))
    r.commit("chore: adopt the standard")
    r.write("docs/DOCMAP.md", docmap.render(ctx_for(r.dir)))
    r.commit("docs: generate the map")
    r.write("docs/DOCMAP.md", docmap.render(ctx_for(r.dir)))
    r.commit("docs: regenerate now that the map is tracked")
    return r


class TestConformantRepo(unittest.TestCase):
    def test_a_conformant_repo_reports_no_errors(self):
        with TempRepo() as r:
            conformant(r)
            report = runner.run(r.dir)
            errors = [f.render() for f in report.errors]
            self.assertEqual(errors, [], "a conformant repo must be green")
            self.assertEqual(report.exit_code, 0)

    def test_a_conformant_repo_is_green_in_ci_too(self):
        with TempRepo() as r:
            conformant(r)
            report = runner.run(r.dir, profile=runner.CI)
            self.assertEqual([f.render() for f in report.errors], [])

    def test_a_stranger_without_hooks_is_not_failed(self):
        """No global git config and no hooks — the common first run."""
        with TempRepo() as r:
            conformant(r)
            r.git("config", "--unset", "core.hooksPath")
            report = runner.run(r.dir)
            hook_errors = [f for f in report.errors if f.check in ("11", "11b")]
            self.assertEqual(hook_errors, [])

    def test_a_conformant_repo_has_no_warns_it_cannot_fix(self):
        """The direction doc and the product map are BOTH required slots, so
        counting the direction doc as competing product truth made full
        conformance permanently yellow. Asserting only 'no errors' let that
        survive: re-adding NORTH_STAR to PRODUCT_TRUTH kept every test green."""
        with TempRepo() as r:
            conformant(r)
            report = runner.run(r.dir)
            for check_id in ("18", "26", "24", "16"):
                offenders = [f.render() for f in report.findings
                             if f.check == check_id]
                self.assertEqual(offenders, [],
                                 f"check {check_id} fires on a conformant repo")

    def test_no_internal_errors_on_a_conformant_repo(self):
        with TempRepo() as r:
            conformant(r)
            report = runner.run(r.dir)
            self.assertEqual([f for f in report.findings
                              if f.check == "internal"], [])


if __name__ == "__main__":
    unittest.main()
