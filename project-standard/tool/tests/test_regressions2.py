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
