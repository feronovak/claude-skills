"""The seam where a house rule stops being universal.

This tool is meant to be handed to someone else's repositories, so anything
tuned to one setup must be overridable. These tests pin that down: a standard
that hardcodes one team's tooling directories smuggles their habits in as best
practice.
"""

import os
import unittest
from pathlib import Path

from fixtures import TempRepo, by_check, ctx_for
from project_standard import defaults, detect, hygiene
from project_standard.contract import parse_contract
from project_standard.gitio import Git


def profile_of(repo):
    return detect.detect(repo.dir, Git(repo.dir).ls_files()).profile


class TestProfileFromConvention(unittest.TestCase):
    """Detection keys off packaging convention, not an absence test.

    'No source files' is nearly never true — an infrastructure repo holds shell
    scripts — and a markdown ratio misfires too, since a documentation-heavy
    product can be 41% markdown.
    """

    def test_no_manifest_and_no_entrypoint_is_docs(self):
        with TempRepo() as r:
            r.write("README.md", "# infra\n")
            r.write("docs/machine.md", "# machine\n")
            r.write("scripts/deploy.sh", "#!/bin/bash\necho hi\n")
            r.write("memwatch/reaper.py", "x = 1\n")
            r.commit()
            self.assertEqual(profile_of(r), detect.DOCS)

    def test_a_manifest_alone_makes_it_a_product(self):
        with TempRepo() as r:
            r.write("package.json", '{"name":"x","version":"1.0.0","private":true}')
            r.write("index.js", "console.log(1)\n")
            r.commit()
            self.assertEqual(profile_of(r), detect.PRODUCT)

    def test_entrypoint_dir_without_a_manifest_is_a_product(self):
        with TempRepo() as r:
            r.write("src/main.go", "package main\n")
            r.commit()
            self.assertEqual(profile_of(r), detect.PRODUCT)

    def test_distribution_signals_make_it_a_library(self):
        cases = [
            ("package.json", '{"name":"x","version":"1.0.0","bin":{"x":"./x.js"}}'),
            ("pyproject.toml",
             '[project]\nname="x"\nversion="1.0"\n\n[project.scripts]\nx="x:main"\n'),
            ("Cargo.toml", '[package]\nname="x"\n\n[lib]\nname="x"\n'),
        ]
        for name, content in cases:
            with self.subTest(manifest=name), TempRepo() as r:
                r.write(name, content)
                r.write("src/lib.rs", "// x\n")
                r.commit()
                self.assertEqual(profile_of(r), detect.LIBRARY)

    def test_private_package_is_not_a_library(self):
        """`private: true` says explicitly that nobody consumes this."""
        with TempRepo() as r:
            r.write("package.json",
                    '{"name":"x","version":"1.0.0","private":true,'
                    '"exports":"./index.js"}')
            r.write("src/index.js", "export const x = 1\n")
            r.commit()
            self.assertEqual(profile_of(r), detect.PRODUCT)

    def test_scripts_directory_alone_does_not_make_a_product(self):
        with TempRepo() as r:
            r.write("README.md", "# docs repo\n")
            r.write("scripts/tool.py", "x = 1\n")
            r.commit()
            self.assertEqual(profile_of(r), detect.DOCS)


class TestLocalOnlyIsOverridable(unittest.TestCase):
    def test_default_set_combines_common_and_house(self):
        paths = defaults.local_only_paths(None)
        self.assertIn("logs/", paths)
        self.assertIn(".cursor/", paths)

    def test_a_repo_can_extend_the_set(self):
        c = parse_contract("## project-standard\n\n```yaml\n"
                           "local-only:\n  - scratch/\n```\n")
        paths = defaults.local_only_paths(c)
        self.assertIn("scratch/", paths)
        self.assertIn("logs/", paths)

    def test_a_repo_can_replace_the_set(self):
        c = parse_contract("## project-standard\n\n```yaml\n"
                           "local-only:\n  - replace\n  - scratch/\n```\n")
        paths = defaults.local_only_paths(c)
        self.assertEqual(paths, ["scratch/"])

    def test_a_repo_can_keep_tracking_a_default_path(self):
        """Some repos track logs/ on purpose. Being told that is wrong is how a
        guard gets disabled wholesale."""
        c = parse_contract("## project-standard\n\n```yaml\n"
                           "track-anyway:\n  - logs/\n```\n")
        self.assertNotIn("logs/", defaults.local_only_paths(c))

    def test_tracking_a_declared_path_produces_no_finding(self):
        with TempRepo() as r:
            r.standard_repo(**{"track-anyway": ["logs/"]})
            r.write("logs/run.log", "x\n")
            r.commit()
            self.assertEqual(by_check(hygiene.check(ctx_for(r.dir)), "7"), [])

    def test_always_tracked_paths_are_never_flagged(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write(".claude/skills/build.md", "# build\n")
            r.write("docs/superpowers/specs/a.md", "# spec\n")
            r.commit()
            self.assertEqual(by_check(hygiene.check(ctx_for(r.dir)), "7"), [])


class TestAttributionPolicy(unittest.TestCase):
    def test_forbid_is_the_default(self):
        self.assertEqual(defaults.attribution_policy(None), "forbid")

    def test_a_repo_can_declare_it_allows_attribution(self):
        c = parse_contract("## project-standard\n\n```yaml\n"
                           "ai-attribution: allow\n```\n")
        self.assertEqual(defaults.attribution_policy(c), "allow")

    def test_allowing_attribution_stands_the_checks_down(self):
        with TempRepo() as r:
            r.standard_repo(**{"ai-attribution": "allow"})
            base = r.commit("chore: base")
            r.write("x.txt", "x")
            r.commit("feat: work\n\n"
                     "Co-Authored-By: Claude <noreply@anthropic.com>")
            findings = hygiene.check(ctx_for(r.dir))
            self.assertEqual(by_check(findings, "8a"), [])

    def test_default_still_flags_attribution(self):
        with TempRepo() as r:
            r.standard_repo()
            r.commit("feat: work\n\n"
                     "Co-Authored-By: Claude <noreply@anthropic.com>")
            findings = hygiene.check(ctx_for(r.dir))
            self.assertTrue(by_check(findings, "14"))


class TestFleetRoot(unittest.TestCase):
    def test_env_var_wins(self):
        original = os.environ.get("PROJECT_STANDARD_FLEET")
        os.environ["PROJECT_STANDARD_FLEET"] = "/tmp/some-fleet"
        try:
            self.assertEqual(defaults.fleet_root(), Path("/tmp/some-fleet"))
        finally:
            if original is None:
                del os.environ["PROJECT_STANDARD_FLEET"]
            else:
                os.environ["PROJECT_STANDARD_FLEET"] = original

    def test_no_hardcoded_personal_path_in_the_source(self):
        """The fastest way to make a tool useless to anyone else."""
        src = Path(__file__).resolve().parents[1] / "project_standard"
        for path in src.glob("*.py"):
            with self.subTest(module=path.name):
                text = path.read_text()
                self.assertNotIn("projects/apps", text)
                self.assertNotIn("/home/", text)


if __name__ == "__main__":
    unittest.main()
