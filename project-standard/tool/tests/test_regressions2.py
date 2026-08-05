"""Second-round regressions.

Each pins a defect that survived the first fix pass — several of them fixes
that were made without a test, which is how they survived.
"""

import unittest
from pathlib import Path

from fixtures import TempRepo, by_check, ctx_for
from project_standard import api, runner
from project_standard.contract import parse_contract
from project_standard.gitio import Git


class TestCommentStripping(unittest.TestCase):
    """A regex lookbehind cannot express 'not inside a quoted span'."""

    def test_a_quoted_value_followed_by_a_comment(self):
        c = parse_contract('## project-standard\n\n```yaml\n'
                           'direction: "a b.md" # which file holds it\n```\n')
        self.assertEqual(c.direction, "a b.md")

    def test_a_hash_inside_a_quoted_value_survives(self):
        c = parse_contract('## project-standard\n\n```yaml\n'
                           'direction: "my docs #1.md"\n```\n')
        self.assertEqual(c.direction, "my docs #1.md")

    def test_a_free_text_reason_keeps_its_hash(self):
        c = parse_contract('## project-standard\n\n```yaml\n'
                           'profile: library\n'
                           '  reason: see issue #42 for why\n```\n')
        self.assertEqual(c.reasons["profile"], "see issue #42 for why")

    def test_an_unquoted_trailing_comment_is_still_stripped(self):
        c = parse_contract('## project-standard\n\n```yaml\n'
                           'http-api: no   # auth callbacks only\n```\n')
        self.assertIs(c.http_api, False)


class TestEveryDetectedFrameworkIsAccountedFor(unittest.TestCase):
    def test_django_is_unresolved_not_zero_routes(self):
        """Detection knows six frameworks; enumeration knew three. The gap
        turned every documented route in a Django repo into a phantom."""
        with TempRepo() as r:
            r.standard_repo()
            r.write("app/urls.py",
                    "urlpatterns = [path('api/items/', views.items)]\n")
            r.write("docs/API_REFERENCE.md",
                    "# API\n\n| Method | Path |\n|---|---|\n"
                    "| GET | `/api/items` |\n")
            r.commit()
            findings = api.check(ctx_for(r.dir))
            self.assertEqual(by_check(findings, "10b"), [],
                             "a documented route must not become a phantom")
            self.assertTrue(by_check(findings, "10d"))

    def test_an_unknown_framework_says_so_instead_of_zero(self):
        with TempRepo() as r:
            r.standard_repo()
            contract = r.contract_block(**{"critical-paths": []})
            r.write("CLAUDE.md", contract.replace(
                "critical-paths:\n",
                "http-api: yes\n  reason: served by a Go router\n"
                "critical-paths:\n"))
            r.write("docs/API_REFERENCE.md", "# API\n")
            r.commit()
            findings = api.check(ctx_for(r.dir))
            self.assertEqual(by_check(findings, "10a"), [])
            self.assertTrue(by_check(findings, "10d"))


class TestAppRouterOutsideApi(unittest.TestCase):
    def test_a_webhook_route_is_an_endpoint(self):
        """`app/webhooks/stripe/route.ts` is a real App Router endpoint."""
        with TempRepo() as r:
            r.write("app/webhooks/stripe/route.ts",
                    "export async function POST() {}\n")
            r.commit()
            eps, _ = api.code_endpoints(r.dir, Git(r.dir).ls_files())
            self.assertEqual(eps, {("POST", "/webhooks/stripe")})


class TestWorkspaceDeclarations(unittest.TestCase):
    def test_pnpm_workspaces_are_announced(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("pnpm-workspace.yaml", "packages:\n  - 'apps/*'\n  - 'libs/*'\n")
            r.commit()
            found = by_check(runner.run(r.dir).findings, "16")
            self.assertTrue(found, "a pnpm monorepo must not pass silently")

    def test_cargo_workspaces_are_announced(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("Cargo.toml",
                    '[workspace]\nmembers = ["crates/a", "crates/b"]\n')
            r.commit()
            self.assertTrue(by_check(runner.run(r.dir).findings, "16"))


class TestCodeMapSeverity(unittest.TestCase):
    def test_unresolved_paths_are_a_warn_not_an_error(self):
        """Hand-auditing this check against a real code map found most hits
        were prose: a sentence asserting a directory does not exist, an
        indented tree diagram, a proposed future layout."""
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/PROJECT_MAP.md",
                    "# Code map\n\nThere is no `src/legacy/` in this repo.\n")
            r.commit()
            found = by_check(runner.run(r.dir).findings, "24")
            self.assertTrue(found)
            self.assertEqual(found[0].severity, "warn")


class TestThirdRoundNits(unittest.TestCase):
    def test_an_apostrophe_does_not_swallow_a_comment(self):
        c = parse_contract('## project-standard\n\n```yaml\n'
                           "direction: it's-doc.md # which file\n```\n")
        self.assertEqual(c.direction, "it's-doc.md")

    def test_a_root_app_router_handler_is_an_endpoint(self):
        with TempRepo() as r:
            r.write("app/route.ts", "export async function GET() {}\n")
            r.commit()
            eps, _ = api.code_endpoints(r.dir, Git(r.dir).ls_files())
            self.assertEqual(eps, {("GET", "/")})

    def test_a_dated_snapshot_dir_is_not_a_local_only_artifact(self):
        from project_standard import hygiene
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/think-day-2026-01-01/exec-summary.md", "# notes\n")
            r.commit()
            self.assertEqual(by_check(hygiene.check(ctx_for(r.dir)), "7"), [])

    def test_unresolvable_stacks_are_not_told_to_run_an_unhelpful_command(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("app/urls.py", "urlpatterns = []\n")
            r.write("docs/API_REFERENCE.md", "# API\n")
            r.commit()
            msg = by_check(api.check(ctx_for(r.dir)), "10d")[0].message
            self.assertIn("by hand", msg)
            self.assertIn("only loads Flask and FastAPI", msg)


class TestPackagingIsRunnable(unittest.TestCase):
    def test_the_documented_command_exists_and_runs(self):
        """The README, the skill and the tool's own finding text all tell the
        user to run `project-standard`. It has to exist."""
        import subprocess
        wrapper = Path(__file__).resolve().parents[2] / "bin" / "project-standard"
        self.assertTrue(wrapper.is_file(), "bin/project-standard is not shipped")
        self.assertTrue(wrapper.stat().st_mode & 0o111, "not executable")
        proc = subprocess.run([str(wrapper), "--version"],
                              capture_output=True, text=True, cwd="/tmp")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("project-standard", proc.stdout)


if __name__ == "__main__":
    unittest.main()


class TestLocalSlots(unittest.TestCase):
    """A public repository may keep internal working documents out of git.

    The spec blessed this and nothing implemented it — the third documented
    mechanism with no readers, and the one the first real retrofit hit.
    """

    def _repo_with_local(self, filename, declaration):
        r = TempRepo().__enter__()
        r.standard_repo()
        (r.dir / filename).unlink(missing_ok=True)
        r.commit("chore: base")
        contract = r.contract_block(adopted="HEAD", **{"critical-paths": []})
        r.write("CLAUDE.md", contract.replace("critical-paths:",
                                              f"{declaration}\ncritical-paths:"))
        r.write(".gitignore", f"{filename}\n")
        r.commit("chore: declare it local")
        r.write(filename, "# kept out of git on purpose\n")
        return r

    def test_a_declared_local_roadmap_satisfies_the_slot(self):
        r = self._repo_with_local("docs/NEXT_STEPS.md", "next-steps: local")
        try:
            findings = runner.run(r.dir).findings
            missing = [f for f in findings
                       if f.check == "1" and "missing roadmap" in f.message]
            self.assertEqual(missing, [])
            local = [f for f in findings
                     if f.check == "1" and "declared local" in f.message]
            self.assertTrue(local, "being local must still be reported")
            self.assertEqual(local[0].severity, "warn")
        finally:
            r.__exit__()

    def test_an_undeclared_untracked_file_does_not_satisfy_the_slot(self):
        r = self._repo_with_local("docs/NEXT_STEPS.md", "prds: docs/prds/")
        try:
            missing = [f for f in runner.run(r.dir).errors
                       if f.check == "1" and "missing roadmap" in f.message]
            self.assertTrue(missing, "silence must not be inferred as consent")
        finally:
            r.__exit__()

    def test_the_agent_contract_cannot_be_declared_local(self):
        """The declaration would live in the file nobody reads."""
        with TempRepo() as r:
            r.standard_repo()
            contract = r.contract_block(adopted="HEAD",
                                        **{"critical-paths": []})
            r.write("CLAUDE.md", contract.replace(
                "critical-paths:", "agent-contract: local\ncritical-paths:"))
            r.commit()
            offenders = [f for f in runner.run(r.dir).errors
                         if "cannot be declared local" in f.message]
            self.assertTrue(offenders)


class TestSecretPosture(unittest.TestCase):
    """The standard recommends a real scanner and ships none.

    A partial pattern list presented as a gate gives false confidence, which is
    worse than no gate. What it does provide is documentation hygiene: a secret
    value in a tracked document or in the agent contract is a different problem
    from a secret in code, and it is one this tool can honestly speak to.
    """

    def test_a_repo_without_a_scanner_is_told_to_get_one(self):
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            found = by_check(runner.run(r.dir).findings, "40")
            self.assertTrue(found)
            self.assertEqual(found[0].severity, "warn")
            self.assertIn("gitleaks", found[0].message)

    def test_a_configured_scanner_silences_the_recommendation(self):
        for config in (".gitleaks.toml", ".secrets.baseline"):
            with self.subTest(config=config), TempRepo() as r:
                r.standard_repo()
                r.write(config, "{}\n")
                r.commit()
                self.assertEqual(by_check(runner.run(r.dir).findings, "40"), [])

    def test_a_scanner_in_ci_counts(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write(".github/workflows/ci.yml",
                    "jobs:\n  scan:\n    steps:\n"
                    "      - uses: gitleaks/gitleaks-action@v2\n")
            r.commit()
            self.assertEqual(by_check(runner.run(r.dir).findings, "40"), [])

    # Assembled at runtime: a literal example key in a tracked test file would
    # be blocked by the authorship/secret guards, and rightly so.
    FAKE_AWS = "AKIA" + "1234567890" + "ABCDEF"

    def test_a_key_shaped_string_in_a_tracked_doc_is_reported(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/setup.md",
                    f"# Setup\n\nExport the key: {self.FAKE_AWS}\n")
            r.commit()
            found = by_check(runner.run(r.dir).findings, "41")
            self.assertTrue(found)
            self.assertEqual(found[0].severity, "warn")
            self.assertEqual(found[0].path, "docs/setup.md")

    def test_a_redacted_example_is_not_reported(self):
        """A redacted mirror is the recommended pattern, not a violation."""
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/setup.md",
                    f"# Setup\n\nSet `AWS_KEY=REPLACE_ME` — e.g. {self.FAKE_AWS}\n")
            r.commit()
            self.assertEqual(by_check(runner.run(r.dir).findings, "41"), [])

    def test_a_clean_document_is_silent(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/setup.md", "# Setup\n\nRun `npm install`.\n")
            r.commit()
            self.assertEqual(by_check(runner.run(r.dir).findings, "41"), [])


class TestInvocationIndependence(unittest.TestCase):
    """The same repository must produce the same findings from anywhere.

    Link targets were resolved against the process working directory rather
    than the repository, so one repo reported 0 errors or 62 depending on where
    the checker was invoked from. A validator whose answer depends on the
    caller's shell is not a validator.
    """

    def test_results_do_not_depend_on_the_working_directory(self):
        import os
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/PROJECT_MAP.md",
                    "# Code map\n\n[readme](../README.md) [flow](DEVELOPMENT_FLOW.md)\n")
            r.write("docs/deep/nested.md", "# Nested\n\n[up](../PROJECT_MAP.md)\n")
            r.commit()

            here = os.getcwd()
            seen = []
            try:
                for where in (r.dir, r.dir / "docs", Path("/tmp"), Path.home()):
                    os.chdir(where)
                    findings = runner.run(r.dir).findings
                    seen.append(sorted(f.render() for f in findings))
            finally:
                os.chdir(here)

            for other in seen[1:]:
                self.assertEqual(seen[0], other,
                                 "findings changed with the working directory")

    def test_relative_links_resolve_against_the_repo(self):
        import os
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/PROJECT_MAP.md",
                    "# Code map\n\n[readme](../README.md)\n")
            r.commit()
            here = os.getcwd()
            try:
                os.chdir("/tmp")
                self.assertEqual(by_check(runner.run(r.dir).findings, "4"), [])
            finally:
                os.chdir(here)
