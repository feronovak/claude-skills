"""Throwaway git repositories for tests.

Fixtures set `core.hooksPath` to an empty directory so the global git-hygiene
guards never interfere — otherwise a test that deliberately commits a Claude
trailer would be blocked by the very hook the suite is testing the checker for.
"""

import shutil
import subprocess
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from project_standard import contract as contract_mod, detect, release, runner
from project_standard.gitio import Git


class TempRepo:
    def __init__(self):
        self.dir = Path(tempfile.mkdtemp(prefix="ps-test-"))

    def __enter__(self):
        self.git("init", "-q", ".")
        self.git("config", "user.name", "Test Human")
        self.git("config", "user.email", "human@example.com")
        self.git("config", "commit.gpgsign", "false")
        nohooks = self.dir / ".nohooks"
        nohooks.mkdir(exist_ok=True)
        self.git("config", "core.hooksPath", str(nohooks))
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self.dir, ignore_errors=True)

    # -- helpers -----------------------------------------------------------

    def git(self, *args):
        proc = subprocess.run(["git", "-C", str(self.dir), *args],
                              capture_output=True, text=True)
        return proc.stdout.strip()

    def write(self, rel, content=""):
        path = self.dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def commit(self, message="chore: test", author=None):
        self.git("add", "-A")
        args = ["commit", "-q", "-m", message]
        if author:
            args += [f"--author={author}"]
        self.git(*args)
        return self.git("rev-parse", "HEAD")

    def tag(self, name):
        self.git("tag", name)

    # -- convenience -------------------------------------------------------

    def contract_block(self, **keys):
        lines = ["# Test project", "",
                 "Run it with `npm run dev`. Tests: `npm test`.",
                 "",
                 "Claude is never a contributor: no Co-Authored-By trailers.",
                 "Local-only paths stay untracked. See docs/DOCMAP.md.",
                 "", "## project-standard", "", "```yaml"]
        for key, value in keys.items():
            key = key.replace("_", "-")
            if isinstance(value, list):
                lines.append(f"{key}:")
                lines += [f"  - {v}" for v in value]
            else:
                lines.append(f"{key}: {value}")
        lines += ["```", ""]
        return "\n".join(lines)

    def standard_repo(self, profile="product", **contract_keys):
        """A repo that satisfies most slots, so a test can break exactly one."""
        self.write("README.md", "# Test\n")
        self.write("src/index.ts", "export const x = 1\n")
        self.write("docs/PROJECT_MAP.md", "# Code map\n")
        self.write("docs/FEATURE_MAP.md", "# Product map\n")
        self.write("docs/NEXT_STEPS.md", "# Next steps\n")
        self.write("docs/DEVELOPMENT_FLOW.md",
                   "# Flow\n\n| Bump | When |\n|---|---|\n"
                   "| major | the caller must adapt |\n"
                   "| minor | new capability |\n| patch | invisible fixes |\n")
        self.write("docs/NORTH_STAR.md", "# North star\n")
        self.write("CHANGELOG.md", "# Changelog\n\n## [0.1.0] - 2026-01-01\n")
        self.write("package.json", '{"name": "t", "version": "0.1.0"}')
        keys = {"critical-paths": [], **contract_keys}
        self.write("CLAUDE.md", self.contract_block(**keys))
        return self


def ctx_for(repo_dir, profile=runner.DEV):
    return runner.build_ctx(Path(repo_dir), profile=profile)


def findings_for(module_check, repo_dir):
    return module_check(ctx_for(repo_dir))


def by_check(findings, check_id):
    return [f for f in findings if f.check == check_id]


def sev_for(findings, check_id):
    hits = by_check(findings, check_id)
    return hits[0].severity if hits else None
