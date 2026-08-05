"""Regression tests for defects found by adversarial review.

Each of these pins a behaviour that was wrong once. A fix without a test is a
fix that comes back, and every case below was shipped and reported before it
was caught — so the test matters more than the patch.
"""

import json
import unittest
from pathlib import Path

from fixtures import TempRepo, by_check, ctx_for
from project_standard import api, defaults, docs, hygiene, runner
from project_standard.gitio import Git


class TestNextEnumeration(unittest.TestCase):
    def test_route_groups_are_stripped_from_the_url(self):
        """`app/(payload)/api/x` serves `/api/x`. Keeping the group invents a
        URL that does not exist — and then reports the real one as phantom."""
        with TempRepo() as r:
            r.write("app/(payload)/api/graphql/route.ts",
                    "export async function POST() {}\n")
            r.commit()
            eps, _ = api.code_endpoints(r.dir, Git(r.dir).ls_files())
            self.assertEqual(eps, {("POST", "/api/graphql")})

    def test_destructured_exports_are_counted(self):
        """`export const { GET, POST } = handlers` is how Auth.js v5 mounts a
        route; matching only `export function` contributed zero endpoints."""
        with TempRepo() as r:
            r.write("app/api/auth/[...nextauth]/route.ts",
                    "import { handlers } from '@/auth'\n"
                    "export const { GET, POST } = handlers\n")
            r.commit()
            eps, _ = api.code_endpoints(r.dir, Git(r.dir).ls_files())
            self.assertEqual(eps, {("GET", "/api/auth/{}"),
                                   ("POST", "/api/auth/{}")})

    def test_re_exported_handlers_are_counted(self):
        with TempRepo() as r:
            r.write("app/api/thing/route.ts", "export { GET } from './impl'\n")
            r.commit()
            eps, _ = api.code_endpoints(r.dir, Git(r.dir).ls_files())
            self.assertIn(("GET", "/api/thing"), eps)


class TestExpressIsHonest(unittest.TestCase):
    def test_express_is_reported_unresolved_not_zero(self):
        """Returning an empty set reads as 'no endpoints', which looks like
        complete coverage and flags every documented route as a phantom."""
        with TempRepo() as r:
            r.write("src/server.ts",
                    "const app = express()\n"
                    "app.get('/api/health', h)\napp.listen(3000)\n")
            r.commit()
            eps, unresolved = api.code_endpoints(r.dir, Git(r.dir).ls_files())
            self.assertEqual(eps, set())
            self.assertIn("express", unresolved)

    def test_a_dev_script_is_not_the_product_api(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("scripts/rate-limit-probe.ts",
                    "const app = express()\napp.listen(9999)\n")
            r.commit()
            self.assertFalse(ctx_for(r.dir).resolved.http_api)


class TestParameterNormalisation(unittest.TestCase):
    def test_every_parameter_syntax_collapses_together(self):
        forms = ["/items/<int:id>", "/items/[id]", "/items/:id", "/items/{item_id}"]
        collapsed = {api.normalise(f) for f in forms}
        self.assertEqual(len(collapsed), 1, collapsed)


class TestLinkResolution(unittest.TestCase):
    def test_site_relative_links_are_not_filesystem_paths(self):
        """Joining an absolute target onto the repo discards the repo, so `/tmp`
        would 'exist' and a real content route would not."""
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/PROJECT_MAP.md",
                    "# Code map\n\n[guide](/fix/dark-photo) and [tmp](/tmp)\n")
            r.commit()
            found = by_check(docs.check(ctx_for(r.dir)), "4")
            self.assertEqual(found, [])

    def test_link_titles_are_not_part_of_the_target(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/PROJECT_MAP.md",
                    '# Code map\n\n[readme](../README.md "The readme")\n')
            r.commit()
            self.assertEqual(by_check(docs.check(ctx_for(r.dir)), "4"), [])

    def test_a_genuinely_broken_relative_link_still_fails(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/PROJECT_MAP.md", "# Code map\n\n[x](./missing.md)\n")
            r.commit()
            self.assertTrue(by_check(docs.check(ctx_for(r.dir)), "4"))

    def test_url_paths_in_the_code_map_are_not_treated_as_files(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/PROJECT_MAP.md",
                    "# Code map\n\nThe endpoint `/api/vet` lives in `src/`.\n")
            r.commit()
            self.assertEqual(by_check(docs.check(ctx_for(r.dir)), "24"), [])


class TestWorkspaces(unittest.TestCase):
    def test_a_monorepo_announces_its_bounded_scope(self):
        """A workspace tree that reports nothing reads as fully covered."""
        with TempRepo() as r:
            r.standard_repo()
            r.write("package.json",
                    json.dumps({"name": "root", "version": "0.1.0",
                                "workspaces": ["content-site"]}))
            r.write("content-site/package.json", '{"name":"c","version":"0.1.0"}')
            r.commit()
            found = by_check(runner.run(r.dir).findings, "16")
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].severity, "warn")
            self.assertIn("content-site", found[0].message)

    def test_a_single_package_repo_says_nothing(self):
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            self.assertEqual(by_check(runner.run(r.dir).findings, "16"), [])


class TestCrashedCheckerFails(unittest.TestCase):
    def test_an_exception_is_an_error_not_a_warn(self):
        """A warn exits zero, which turns CI green on a module that never ran."""
        original = runner.MODULES

        def boom(ctx):
            raise RuntimeError("deliberate")

        try:
            runner.MODULES = (("boom", boom),) + original
            with TempRepo() as r:
                r.standard_repo()
                r.commit()
                report = runner.run(r.dir)
                internal = by_check(report.findings, "internal")
                self.assertEqual(internal[0].severity, "error")
                self.assertEqual(report.exit_code, 1)
        finally:
            runner.MODULES = original


class TestContractSourceOfTruth(unittest.TestCase):
    def test_an_untracked_contract_is_reported_coherently(self):
        """Checks 1 and 2 must not disagree about whether a contract exists."""
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            (r.dir / "CLAUDE.md").unlink()
            r.write("AGENTS.md", "# untracked\n")
            (r.dir / ".gitignore").write_text("AGENTS.md\n")
            r.git("rm", "-q", "--cached", "CLAUDE.md")
            r.commit("chore: drop the tracked contract")
            report = runner.run(r.dir)
            messages = " ".join(f.message for f in report.findings)
            self.assertIn("not tracked", messages)


class TestEcosystemNeutrality(unittest.TestCase):
    def test_a_rust_contract_satisfies_the_run_section(self):
        """A tool that recognises only npm and python tells whole ecosystems
        their contract is wrong."""
        for command in ("cargo test", "go test ./...", "mvn verify",
                        "bundle exec rspec", "dotnet test"):
            with self.subTest(command=command), TempRepo() as r:
                r.standard_repo()
                contract = r.contract_block(adopted="HEAD",
                                            **{"critical-paths": []})
                contract = contract.replace("Run it with `npm run dev`. "
                                            "Tests: `npm test`.",
                                            f"Build and test with `{command}`.")
                r.write("CLAUDE.md", contract)
                r.commit()
                findings = runner.run(r.dir).findings
                self.assertFalse(
                    [f for f in findings
                     if f.check == "2" and "run/test/build" in f.message],
                    f"{command} should satisfy the run section")


class TestHooksAreShipped(unittest.TestCase):
    def test_the_guards_exist_in_the_package(self):
        """Check 11 asks for guards; a package that demands them and does not
        ship them cannot be satisfied by anyone who clones it."""
        hooks = Path(__file__).resolve().parents[2] / "hooks"
        for name in ("pre-commit", "commit-msg"):
            with self.subTest(hook=name):
                path = hooks / name
                self.assertTrue(path.is_file(), f"{name} is not shipped")
                self.assertTrue(path.stat().st_mode & 0o111, f"{name} not executable")

    def test_the_shipped_guard_blocks_every_marker(self):
        import subprocess
        hooks = Path(__file__).resolve().parents[2] / "hooks"
        markers = [
            "Co-Authored-By: Claude <noreply@anthropic.com>",
            "Claude-Session: https://claude.ai/code/session_1",
            "Signed-off-by: Claude <noreply@anthropic.com>",
            "🤖 Generated with [Claude Code](https://claude.com/claude-code)",
        ]
        for marker in markers:
            with self.subTest(marker=marker.split(":")[0]), TempRepo() as r:
                msg = r.dir / "MSG"
                msg.write_text(f"feat: x\n\n{marker}\n")
                proc = subprocess.run([str(hooks / "commit-msg"), str(msg)],
                                      capture_output=True, text=True)
                self.assertEqual(proc.returncode, 1, marker)

    def test_the_shipped_guard_allows_a_clean_message(self):
        import subprocess
        hooks = Path(__file__).resolve().parents[2] / "hooks"
        with TempRepo() as r:
            msg = r.dir / "MSG"
            msg.write_text("feat: an ordinary human commit\n")
            proc = subprocess.run([str(hooks / "commit-msg"), str(msg)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stdout)


class TestApiFreshness(unittest.TestCase):
    def test_a_manifest_older_than_its_routes_is_an_error(self):
        """Check 10c had no test at all, and no real repo exercised it."""
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/api/routes.json", json.dumps(
                {"generated_by": "t",
                 "routes": [{"method": "GET", "path": "/api/old"}]}))
            r.write("docs/API_REFERENCE.md",
                    "# API\n\n| Method | Path |\n|---|---|\n| GET | `/api/old` |\n")
            r.write("app/api/old/route.ts", "export async function GET() {}\n")
            r.commit("chore: manifest and routes together")
            r.write("app/api/old/route.ts",
                    "export async function GET() {}\n// changed later\n")
            r.commit("feat: touch the route after the manifest")
            self.assertTrue(by_check(api.check(ctx_for(r.dir)), "10c"))

    def test_a_manifest_newer_than_its_routes_passes(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("app/api/old/route.ts", "export async function GET() {}\n")
            r.commit("feat: the route")
            r.write("docs/api/routes.json", json.dumps(
                {"generated_by": "t",
                 "routes": [{"method": "GET", "path": "/api/old"}]}))
            r.write("docs/API_REFERENCE.md",
                    "# API\n\n| Method | Path |\n|---|---|\n| GET | `/api/old` |\n")
            r.commit("docs: regenerate the manifest")
            self.assertEqual(by_check(api.check(ctx_for(r.dir)), "10c"), [])


if __name__ == "__main__":
    unittest.main()
