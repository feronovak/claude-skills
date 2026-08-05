import unittest

from fixtures import TempRepo, ctx_for, sev_for
from project_standard import detect
from project_standard.gitio import Git


def detect_for(repo):
    return detect.detect(repo.dir, Git(repo.dir).ls_files())


class TestProfile(unittest.TestCase):
    def test_source_tree_is_a_product(self):
        with TempRepo() as r:
            r.write("src/index.ts", "export const x = 1\n")
            r.commit()
            self.assertEqual(detect_for(r).profile, detect.PRODUCT)

    def test_publish_config_makes_it_a_library(self):
        with TempRepo() as r:
            r.write("package.json", '{"name":"x","publishConfig":{"access":"public"}}')
            r.write("src/i.ts", "export const x = 1\n")
            r.commit()
            self.assertEqual(detect_for(r).profile, detect.LIBRARY)

    def test_pyproject_scripts_make_it_a_library(self):
        with TempRepo() as r:
            r.write("pyproject.toml",
                    '[project]\nname="x"\nversion="1.0.0"\n\n'
                    '[project.scripts]\nx = "x:main"\n')
            r.write("x.py", "def main(): pass\n")
            r.commit()
            self.assertEqual(detect_for(r).profile, detect.LIBRARY)

    def test_markdown_only_repo_is_docs(self):
        with TempRepo() as r:
            r.write("README.md", "# infra\n")
            r.write("docs/machine.md", "# machine\n")
            r.commit()
            self.assertEqual(detect_for(r).profile, detect.DOCS)


class TestHttpApi(unittest.TestCase):
    def test_next_route_files_set_http_api(self):
        with TempRepo() as r:
            r.write("app/api/vet/route.ts", "export async function POST() {}\n")
            r.commit()
            self.assertTrue(detect_for(r).http_api)

    def test_flask_app_sets_http_api(self):
        with TempRepo() as r:
            r.write("app/__init__.py", "from flask import Flask\n"
                                       "def create(): return Flask(__name__)\n")
            r.commit()
            self.assertTrue(detect_for(r).http_api)

    def test_plain_spa_has_no_http_api(self):
        with TempRepo() as r:
            r.write("src/main.ts", "document.body.innerHTML = 'hi'\n")
            r.write("index.html", "<html></html>")
            r.commit()
            self.assertFalse(detect_for(r).http_api)


class TestChannels(unittest.TestCase):
    def test_extension_suppresses_web(self):
        """An extension's source looks exactly like a web app's; a phantom web
        channel arms a release gate that can never pass."""
        with TempRepo() as r:
            r.write("manifest.json", '{"manifest_version": 3, "name": "x"}')
            r.write("src/content.ts", "export const x = 1\n")
            r.commit()
            self.assertEqual(detect_for(r).channels, ["extension"])

    def test_mobile_and_desktop_compose_with_web(self):
        with TempRepo() as r:
            r.write("src/main.ts", "export const x = 1\n")
            r.write("android-native/app/build.gradle", "// x\n")
            r.write("src-tauri/tauri.conf.json", "{}")
            r.commit()
            self.assertEqual(detect_for(r).channels,
                             ["web", "mobile", "desktop"])

    def test_plain_repo_is_web(self):
        with TempRepo() as r:
            r.write("src/main.ts", "export const x = 1\n")
            r.commit()
            self.assertEqual(detect_for(r).channels, ["web"])


class TestResolveAndOverride(unittest.TestCase):
    def test_override_without_reason_is_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("app/api/vet/route.ts", "export async function POST() {}\n")
            r.write("CLAUDE.md", r.contract_block(**{"http-api": "no",
                                                     "critical-paths": []}))
            r.commit()
            findings = detect.check(ctx_for(r.dir))
            self.assertEqual(sev_for(findings, "6"), "error")

    def test_override_with_reason_is_a_warn(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("app/api/auth/route.ts", "export async function GET() {}\n")
            block = r.contract_block(**{"critical-paths": []})
            block = block.replace("```\n", "http-api: no\n"
                                  "  reason: auth callbacks only\n```\n", 1) \
                if False else block
            r.write("CLAUDE.md", block.replace(
                "critical-paths:\n", "http-api: no\n"
                "  reason: auth callbacks only\ncritical-paths:\n"))
            r.commit()
            findings = detect.check(ctx_for(r.dir))
            self.assertEqual(sev_for(findings, "6"), "warn")

    def test_no_override_produces_no_finding(self):
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            self.assertEqual(detect.check(ctx_for(r.dir)), [])


if __name__ == "__main__":
    unittest.main()
