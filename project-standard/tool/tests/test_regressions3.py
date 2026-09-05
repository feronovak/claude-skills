"""Third-round regressions, from a review of the finished skill.

Each of these is a defect that shipped past both earlier fix passes. Two of
them are the same failure twice: a fix that was made and a test that was
written to pin something narrower than the commit claimed, so the real bug
stayed live under a green suite.
"""

import os
import unittest
from pathlib import Path

from fixtures import TempRepo, by_check, ctx_for
from project_standard import baselines, cli, detect, runner
from project_standard.contract import parse_contract
from project_standard.gitio import Git, repo_root


class TestSubdirectoryInvocation(unittest.TestCase):
    """The same repository, the same answer — including from inside it.

    `TestInvocationIndependence` varies the working directory but always hands
    `runner.run()` the repository's absolute path, so it pins link resolution
    only. The path where the repo argument *is* the working directory — an
    omitted `--repo`, the most natural way to run the tool — went unexercised,
    and `git -C <subdir> ls-files` quietly returned a truncated, wrongly-rooted
    file list. Every root-level document then read as missing.
    """

    def test_resolve_repos_anchors_on_the_git_root(self):
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            here = os.getcwd()
            try:
                os.chdir(r.dir / "docs")
                args = type("A", (), {"repo": [], "fleet": False})()
                resolved = cli.resolve_repos(args)
            finally:
                os.chdir(here)
            self.assertEqual([Path(p).resolve() for p in resolved],
                             [r.dir.resolve()])

    def test_findings_are_identical_from_a_subdirectory(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/deep/nested.md", "# Nested\n")
            r.commit()

            from_root = sorted(f.render() for f in runner.run(r.dir).findings)
            here = os.getcwd()
            try:
                for sub in ("docs", "src", "docs/deep"):
                    os.chdir(r.dir / sub)
                    seen = sorted(f.render()
                                  for f in runner.run(Path.cwd()).findings)
                    self.assertEqual(from_root, seen,
                                     f"findings changed when run from {sub}")
            finally:
                os.chdir(here)

    def test_a_subdirectory_does_not_invent_missing_documents(self):
        # The original symptom: root-level documents that plainly exist were
        # reported missing, because the file list was scoped to the subtree.
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            rendered = " ".join(f.render()
                                for f in runner.run(r.dir / "docs").findings)
            for missing in ("missing README", "missing agent contract",
                            "no agent contract"):
                self.assertNotIn(missing, rendered)

    def test_repo_root_leaves_a_non_repository_alone(self):
        # The not-a-repository finding must still name what the caller asked
        # for, rather than silently retargeting some enclosing repository.
        import tempfile
        plain = Path(tempfile.mkdtemp(prefix="ps-plain-"))
        try:
            self.assertEqual(repo_root(plain), plain)
        finally:
            import shutil
            shutil.rmtree(plain, ignore_errors=True)


class TestRouteDetectionMatchesEnumeration(unittest.TestCase):
    """Detection and enumeration must agree on what a route file is.

    They drifted: detection required a path segment, so a repo whose only HTTP
    surface was a root-level `app/route.ts` was never resolved as serving HTTP.
    `api.check()` returns early on that, so the entire coverage check silently
    never ran — the worst shape of failure for a validator.
    """

    def test_the_two_modules_share_one_pattern(self):
        from project_standard import api
        self.assertIs(detect.NEXT_ROUTE, api.NEXT_ROUTE)
        self.assertIs(detect.NEXT_PAGES_API, api.NEXT_PAGES_API)

    def test_a_root_level_route_file_counts_as_an_http_surface(self):
        self.assertTrue(detect.NEXT_ROUTE.match("app/route.ts"))
        self.assertTrue(detect.NEXT_ROUTE.match("src/app/route.js"))
        self.assertTrue(detect.NEXT_ROUTE.match("app/api/thing/route.ts"))

    def test_a_single_webhook_repo_is_detected_as_serving_http(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("app/route.ts", "export async function POST() {}\n")
            r.commit()
            ctx = ctx_for(r.dir)
            self.assertTrue(
                ctx.resolved.http_api,
                "a repo whose only endpoint is app/route.ts was not detected")

    def test_coverage_actually_runs_for_that_repo(self):
        from project_standard import api
        with TempRepo() as r:
            r.standard_repo()
            r.write("app/route.ts", "export async function POST() {}\n")
            r.commit()
            out = api.check(ctx_for(r.dir))
            self.assertTrue(out, "the coverage check produced no findings at all")


class TestUnknownContractKeys(unittest.TestCase):
    """A closed grammar, because a typo is far likelier than an extension.

    `chanels:` parsed clean, the typed accessor returned None, and that is
    indistinguishable from never declaring it — so the mismatch check could
    not fire either. The author's override silently never took effect.
    """

    def _parse(self, body):
        return parse_contract("## project-standard\n\n```yaml\n"
                              + body + "\n```\n", path="CLAUDE.md")

    def test_a_typo_is_an_error_with_a_suggestion(self):
        c = self._parse("chanels: [web, mobile]")
        self.assertTrue(c.errors)
        self.assertIn("chanels", c.errors[0])
        self.assertIn("channels", c.errors[0])

    def test_an_unrecognisable_key_lists_the_grammar(self):
        c = self._parse("wibble: 1")
        self.assertTrue(c.errors)
        self.assertIn("known keys", c.errors[0])

    def test_every_known_key_parses_without_complaint(self):
        from project_standard.contract import KNOWN_KEYS
        for key in KNOWN_KEYS:
            c = self._parse(f"{key}: x")
            self.assertEqual([], c.errors, f"`{key}` was rejected")

    def test_the_grammar_covers_every_key_the_checks_read(self):
        # The guard against the closed set going stale: a check that reads a
        # key the parser rejects would fail every repo that declares it.
        import re
        from project_standard.contract import KNOWN_KEYS
        src_dir = Path(__file__).resolve().parents[1] / "project_standard"
        read = set()
        for path in src_dir.glob("*.py"):
            read |= set(re.findall(r"raw\.get\(\"([a-z-]+)\"",
                                   path.read_text()))
            read |= set(re.findall(r"raw\[\"([a-z-]+)\"\]", path.read_text()))
        self.assertEqual(set(), read - set(KNOWN_KEYS),
                         "a check reads a key the contract grammar rejects")

    def test_the_grammar_covers_the_keys_read_indirectly(self):
        # Grepping for `raw.get("literal")` cannot see a key reached through a
        # lookup table. It missed `next-steps` and `release-flow`, and the
        # closed grammar then rejected a contract the standard blesses.
        from project_standard.artifacts import LOCAL_ALLOWED
        from project_standard.contract import KNOWN_KEYS
        self.assertEqual(set(), set(LOCAL_ALLOWED.values()) - set(KNOWN_KEYS),
                         "a slot may be declared local under a key the "
                         "contract grammar rejects")

    def test_a_contract_declaring_slots_local_parses_clean(self):
        c = self._parse("next-steps: local\nrelease-flow: local\nprds: local")
        self.assertEqual([], c.errors)

    def test_a_reason_line_is_still_not_a_key(self):
        c = self._parse("profile: docs\n  reason: a collection of skills")
        self.assertEqual([], c.errors)
        self.assertEqual("a collection of skills", c.reasons["profile"])


class TestBaselinesRatchet(unittest.TestCase):
    """A baseline records progress made; it may not absorb a regression.

    Nothing compared a baseline to anything but the value sitting in the
    contract right now — so the commit that removed the documentation could
    edit the number that would have caught it, in the same breath.
    """

    def _repo(self, r, **keys):
        r.standard_repo(**keys)
        return r

    def test_lowering_api_coverage_is_an_error(self):
        with TempRepo() as r:
            self._repo(r, adopted="HEAD", api_coverage=35)
            r.commit()
            r.write("CLAUDE.md", r.contract_block(**{
                "critical-paths": [], "adopted": "HEAD", "api-coverage": 5}))
            hits = by_check(baselines.check(ctx_for(r.dir)), "42")
            self.assertTrue(hits, "a lowered api-coverage went unreported")
            self.assertIn("35", hits[0].message)

    def test_raising_api_coverage_is_silent(self):
        with TempRepo() as r:
            self._repo(r, adopted="HEAD", api_coverage=35)
            r.commit()
            r.write("CLAUDE.md", r.contract_block(**{
                "critical-paths": [], "adopted": "HEAD", "api-coverage": 40}))
            self.assertEqual([], by_check(baselines.check(ctx_for(r.dir)), "42"))

    def test_raising_the_scaffold_allowance_is_an_error(self):
        with TempRepo() as r:
            self._repo(r, adopted="HEAD", scaffold=4)
            r.commit()
            r.write("CLAUDE.md", r.contract_block(**{
                "critical-paths": [], "adopted": "HEAD", "scaffold": 9}))
            hits = by_check(baselines.check(ctx_for(r.dir)), "42")
            self.assertTrue(hits, "a raised scaffold allowance went unreported")

    def test_lowering_the_scaffold_allowance_is_silent(self):
        with TempRepo() as r:
            self._repo(r, adopted="HEAD", scaffold=4)
            r.commit()
            r.write("CLAUDE.md", r.contract_block(**{
                "critical-paths": [], "adopted": "HEAD", "scaffold": 1}))
            self.assertEqual([], by_check(baselines.check(ctx_for(r.dir)), "42"))

    def test_the_ratchet_survives_the_loosening_being_committed(self):
        # A comparison against HEAD alone would go green the moment the edit
        # lands. The recorded extreme is what makes it durable.
        with TempRepo() as r:
            self._repo(r, adopted="HEAD", api_coverage=35)
            r.commit()
            r.write("CLAUDE.md", r.contract_block(**{
                "critical-paths": [], "adopted": "HEAD", "api-coverage": 5}))
            r.commit("chore: loosen the baseline")
            hits = by_check(baselines.check(ctx_for(r.dir)), "42")
            self.assertTrue(hits, "the ratchet forgot once the edit was committed")

    def test_lowering_a_floor_with_a_reason_is_sanctioned(self):
        # A documented route can be removed with its reference entry, lowering
        # the floor honestly. The reset is trusted when the contract says why,
        # exactly as every other override in this standard is.
        with TempRepo() as r:
            self._repo(r, adopted="HEAD", api_coverage=35)
            r.commit()
            block = r.contract_block(**{
                "critical-paths": [], "adopted": "HEAD", "api-coverage": 5})
            block = block.replace(
                "api-coverage: 5\n",
                "api-coverage: 5\n  reason: a documented route was retired "
                "with its reference entry\n")
            r.write("CLAUDE.md", block)
            self.assertEqual([], by_check(baselines.check(ctx_for(r.dir)), "42"),
                             "a reasoned floor reset was reported as a breach")

    def test_a_reasoned_reset_stays_sanctioned_once_committed(self):
        # The reason lives in the tracked contract, so the sanction is durable
        # — it does not evaporate the release after the reset lands.
        with TempRepo() as r:
            self._repo(r, adopted="HEAD", api_coverage=35)
            r.commit()
            block = r.contract_block(**{
                "critical-paths": [], "adopted": "HEAD", "api-coverage": 5})
            block = block.replace(
                "api-coverage: 5\n",
                "api-coverage: 5\n  reason: a documented route was retired\n")
            r.write("CLAUDE.md", block)
            r.commit("release: reset the floor for a removed route")
            self.assertEqual([], by_check(baselines.check(ctx_for(r.dir)), "42"))

    def test_a_reason_on_a_different_key_does_not_sanction(self):
        # The reason must sit on the baseline that moved. A reason attached to
        # some other key is not a licence to lower this one silently.
        with TempRepo() as r:
            self._repo(r, adopted="HEAD", api_coverage=35)
            r.commit()
            block = r.contract_block(**{
                "critical-paths": [], "adopted": "HEAD", "profile": "product",
                "api-coverage": 5})
            block = block.replace(
                "profile: product\n",
                "profile: product\n  reason: detection is confused here\n")
            r.write("CLAUDE.md", block)
            hits = by_check(baselines.check(ctx_for(r.dir)), "42")
            self.assertTrue(hits, "a reason on another key sanctioned the drop")

    def test_walking_adopted_forward_is_an_error(self):
        with TempRepo() as r:
            self._repo(r)
            first = r.commit()
            r.write("CLAUDE.md", r.contract_block(**{
                "critical-paths": [], "adopted": first}))
            r.commit()
            r.write("x.txt", "x")
            later = r.commit()
            r.write("CLAUDE.md", r.contract_block(**{
                "critical-paths": [], "adopted": later}))
            hits = by_check(baselines.check(ctx_for(r.dir)), "42")
            self.assertTrue(hits, "adopted was walked forward unreported")

    def test_moving_adopted_backwards_is_silent(self):
        with TempRepo() as r:
            self._repo(r)
            first = r.commit()
            r.write("x.txt", "x")
            later = r.commit()
            r.write("CLAUDE.md", r.contract_block(**{
                "critical-paths": [], "adopted": later}))
            r.commit()
            r.write("CLAUDE.md", r.contract_block(**{
                "critical-paths": [], "adopted": first}))
            self.assertEqual([], by_check(baselines.check(ctx_for(r.dir)), "42"),
                             "widening the audited range was reported as a breach")

    def test_a_placeholder_replaced_by_a_real_commit_is_silent(self):
        # `adopted: HEAD` is what people write while adopting. Replacing it
        # with the actual commit is a correction, not a walk forward — and
        # HEAD resolves as an ancestor of everything, so a naive comparison
        # reports it forever.
        with TempRepo() as r:
            self._repo(r, adopted="HEAD")
            first = r.commit()
            r.write("CLAUDE.md", r.contract_block(**{
                "critical-paths": [], "adopted": first}))
            self.assertEqual([], by_check(baselines.check(ctx_for(r.dir)), "42"))

    def test_a_garbage_baseline_is_not_a_traceback(self):
        with TempRepo() as r:
            self._repo(r, adopted="not-a-sha", api_coverage="lots")
            r.commit()
            baselines.check(ctx_for(r.dir))  # must not raise

    def test_a_repo_with_no_baselines_is_silent(self):
        with TempRepo() as r:
            self._repo(r)
            r.commit()
            self.assertEqual([], by_check(baselines.check(ctx_for(r.dir)), "42"))

    def test_the_check_is_skipped_on_a_shallow_clone(self):
        self.assertIn("42", runner.HISTORY_CHECKS)


if __name__ == "__main__":
    unittest.main()
