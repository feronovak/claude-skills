"""The decisions slot, and waiving a slot honestly.

The taxonomy had five documents and no home for "why this and not the obvious
alternative". Direction is where the product is going, the product map is what
it does today, the changelog is what shipped, a PRD is a proposal — none
records a choice. The fleet had already concluded it needed the category and
invented `DECISIONS.md` by hand.

Waiving is allowed because the slot will not fit every repository. Waiving
silently is not: an escape hatch that costs nothing becomes the default, which
is the same reasoning that makes a profile override owe a reason.
"""

import unittest

from fixtures import TempRepo, by_check, ctx_for
from project_standard import artifacts, claims, runner


def _findings(r):
    return runner.run(r.dir).findings


class TestTheSlot(unittest.TestCase):

    def test_a_repo_without_one_is_warned_not_failed(self):
        # Judgement work that accrues over a project's life. Erroring on an
        # empty decision log trains people to scaffold a file nobody writes in.
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            hits = [f for f in by_check(_findings(r), "1")
                    if "decisions" in f.message]
            self.assertEqual(1, len(hits))
            self.assertEqual("warn", hits[0].severity)

    def test_a_single_file_satisfies_it(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/DECISIONS.md", "# Decisions\n\n## Chose X — 2026-01-01\n")
            r.commit()
            self.assertEqual([], [f for f in by_check(_findings(r), "1")
                                  if "decisions" in f.message])

    def test_a_directory_of_records_satisfies_it(self):
        # ADRs are conventionally one file per decision. Git tracks no
        # directories, so the slot is satisfied by anything tracked beneath it.
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/adr/0001-use-sqlite.md", "# Use SQLite\n\n## Context\n")
            r.commit()
            self.assertEqual([], [f for f in by_check(_findings(r), "1")
                                  if "decisions" in f.message])

    def test_a_docs_repo_owes_one_too(self):
        # An infrastructure repo makes architectural decisions like any other,
        # and the fleet's own docs repos are where several of them live.
        with TempRepo() as r:
            r.write("README.md", "# Docs\n")
            r.write("CLAUDE.md", r.contract_block(**{"critical-paths": []}))
            r.commit()
            names = [s.name for s in artifacts.resolve_slots(ctx_for(r.dir))]
            self.assertIn("decisions", names)


class TestWaiving(unittest.TestCase):

    def test_waiving_with_a_reason_removes_the_finding(self):
        with TempRepo() as r:
            r.standard_repo()
            contract = (r.dir / "CLAUDE.md").read_text().replace(
                "critical-paths:",
                "decisions: waived\n  reason: a one-file script, no "
                "architecture to decide\ncritical-paths:")
            r.write("CLAUDE.md", contract)
            r.commit()
            found = _findings(r)
            self.assertEqual([], [f for f in by_check(found, "1")
                                  if "decisions" in f.message])
            self.assertEqual([], [f for f in by_check(found, "2")
                                  if "waived" in f.message])

    def test_waiving_without_a_reason_is_an_error(self):
        with TempRepo() as r:
            r.standard_repo()
            contract = (r.dir / "CLAUDE.md").read_text().replace(
                "critical-paths:", "decisions: waived\ncritical-paths:")
            r.write("CLAUDE.md", contract)
            r.commit()
            hits = [f for f in by_check(_findings(r), "2")
                    if "waived" in f.message]
            self.assertTrue(hits, "a silent waiver went unreported")
            self.assertEqual("error", hits[0].severity)

    def test_waiving_is_in_the_contract_grammar(self):
        from project_standard.contract import KNOWN_KEYS
        for key in artifacts.WAIVABLE.values():
            self.assertIn(key, KNOWN_KEYS,
                          "a waiver key the contract parser would reject")


class TestDecisionUnits(unittest.TestCase):

    def test_each_record_is_a_unit(self):
        text = ("# Decisions\n\n"
                "## Chose SQLite over Postgres — 2026-01-01\n\ncontext\n\n"
                "## Dropped the queue — 2026-02-01\n\ncontext\n")
        units = claims.units_for("docs/DECISIONS.md", text)
        self.assertEqual(2, len(units))
        self.assertEqual({"decision"}, {u.kind for u in units})

    def test_verifying_asks_whether_it_still_holds_not_whether_it_was_right(self):
        text = "# Decisions\n\n## Chose X — 2026-01-01\n"
        verify = claims.units_for("docs/DECISIONS.md", text)[0].verify
        self.assertIn("still governs", verify)
        self.assertIn("supersede", verify)

    def test_an_adr_directory_is_enumerated(self):
        with TempRepo() as r:
            r.standard_repo()
            r.write("docs/adr/0001-thing.md", "# Thing\n\n## Chose X\n\nwhy\n")
            r.commit()
            units, _ = claims.enumerate_repo(ctx_for(r.dir))
            self.assertIn("docs/adr/0001-thing.md", units)

    def test_the_scaffolded_template_contributes_no_unit(self):
        # The template's one entry is a placeholder; counting it would put a
        # unit on the worklist that exists only to be replaced.
        from pathlib import Path
        tmpl = (Path(__file__).resolve().parents[2] / "templates"
                / "DECISIONS.md.tmpl").read_text()
        self.assertEqual([], claims.units_for("docs/DECISIONS.md", tmpl))


if __name__ == "__main__":
    unittest.main()
