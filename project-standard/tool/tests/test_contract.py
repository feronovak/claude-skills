import unittest

from fixtures import TempRepo
from project_standard.contract import find_contract, load, parse_contract

BLOCK = """# Repo

Prose a human reads.

## project-standard

```yaml
adopted: 4f3a91c
profile: product
http-api: no
  reason: app/api is Auth.js callbacks only, no public surface
channels: [web, mobile]
direction: docs/NORTH_STAR.md
critical-paths:
  - services/verdict/
  - services/scoring/
```

More prose.
"""


class TestContractParser(unittest.TestCase):
    def test_parses_scalars_lists_and_reasons(self):
        c = parse_contract(BLOCK)
        self.assertEqual(c.adopted, "4f3a91c")
        self.assertEqual(c.profile, "product")
        self.assertIs(c.http_api, False)
        self.assertEqual(c.reasons["http-api"],
                         "app/api is Auth.js callbacks only, no public surface")
        self.assertEqual(c.channels, ["web", "mobile"])
        self.assertEqual(c.direction, "docs/NORTH_STAR.md")
        self.assertEqual(c.critical_paths,
                         ["services/verdict/", "services/scoring/"])
        self.assertEqual(c.errors, [])

    def test_missing_block_is_a_finding_not_a_crash(self):
        c = parse_contract("# Readme\n\nnothing machine readable here")
        self.assertIsNone(c.adopted)
        self.assertTrue(any("no `## project-standard` block" in e
                            for e in c.errors))

    def test_a_critical_path_may_declare_its_required_reading(self):
        """The mapping form is additive: bare strings and mappings coexist in one list."""
        c = parse_contract(
            "## project-standard\n\n```yaml\ncritical-paths:\n"
            "  - services/scoring/\n"
            "  - path: src/integrations/\n"
            "    reference: docs/reference/FIELD_MAP.md\n```\n")
        # Every existing consumer asks for paths and must still get plain strings.
        self.assertEqual(c.critical_paths, ["services/scoring/", "src/integrations/"])
        self.assertEqual(c.critical_path_refs,
                         [("src/integrations/", "docs/reference/FIELD_MAP.md")])

    def test_a_bare_critical_path_list_declares_no_references(self):
        """Adopting the key must cost nothing: the common contract keeps behaving exactly as it did."""
        c = parse_contract(BLOCK)
        self.assertEqual(c.critical_path_refs, [])

    def test_a_mapping_without_a_reference_is_still_just_a_path(self):
        c = parse_contract("## project-standard\n\n```yaml\ncritical-paths:\n"
                           "  - path: services/scoring/\n```\n")
        self.assertEqual(c.critical_paths, ["services/scoring/"])
        self.assertEqual(c.critical_path_refs, [])

    def test_empty_critical_paths_is_present_but_empty(self):
        c = parse_contract("## project-standard\n\n```yaml\n"
                           "critical-paths:\n```\n")
        self.assertEqual(c.critical_paths, [])
        self.assertIsNotNone(c.critical_paths)

    def test_override_without_reason_is_recorded(self):
        c = parse_contract("## project-standard\n\n```yaml\nprofile: library\n```\n")
        self.assertEqual(c.profile, "library")
        self.assertIn("profile", c.missing_reasons)

    def test_override_with_reason_is_not_flagged(self):
        c = parse_contract("## project-standard\n\n```yaml\nprofile: library\n"
                           "  reason: published to PyPI\n```\n")
        self.assertNotIn("profile", c.missing_reasons)

    def test_malformed_line_becomes_an_error_never_an_exception(self):
        c = parse_contract("## project-standard\n\n```yaml\n"
                           "this line has no colon\n```\n")
        self.assertTrue(any("cannot parse" in e for e in c.errors))

    def test_booleans_and_inline_lists(self):
        c = parse_contract("## project-standard\n\n```yaml\n"
                           "http-api: yes\nchannels: [web]\n```\n")
        self.assertIs(c.http_api, True)
        self.assertEqual(c.channels, ["web"])


DOCUMENTED_EXAMPLE = """## project-standard

```yaml
adopted: 4f3a91c              # baseline commit; attribution errors start here
profile: product              # omit unless overriding detection
http-api: no                  # omit unless overriding detection
  reason: app/api is Auth.js callbacks only, no public surface
channels: [web, mobile]       # omit unless overriding detection
direction: docs/NORTH_STAR.md # which file holds mission/vision/north star
ai-attribution: allow         # this repo wants the trailers
critical-paths:               # may be empty, may not be absent
  - services/verdict/
```
"""


class TestDocumentedGrammar(unittest.TestCase):
    """The examples in the spec, SKILL.md and README all carry inline comments.

    A parser that cannot read its own documentation is broken, and this one
    failed silently rather than loudly: `http-api: no  # ...` produced a
    non-empty string, which is truthy, inverting the declared value.
    """

    def test_the_documented_example_parses(self):
        c = parse_contract(DOCUMENTED_EXAMPLE)
        self.assertEqual(c.errors, [])
        self.assertEqual(c.adopted, "4f3a91c")
        self.assertEqual(c.profile, "product")
        self.assertEqual(c.direction, "docs/NORTH_STAR.md")
        self.assertEqual(c.critical_paths, ["services/verdict/"])

    def test_a_commented_boolean_is_not_inverted(self):
        c = parse_contract(DOCUMENTED_EXAMPLE)
        self.assertIs(c.http_api, False)

    def test_a_commented_inline_list_still_parses(self):
        c = parse_contract(DOCUMENTED_EXAMPLE)
        self.assertEqual(c.channels, ["web", "mobile"])

    def test_a_commented_policy_value_is_recognised(self):
        from project_standard.defaults import attribution_policy
        self.assertEqual(attribution_policy(parse_contract(DOCUMENTED_EXAMPLE)),
                         "allow")

    def test_a_hash_inside_quotes_survives(self):
        c = parse_contract('## project-standard\n\n```yaml\n'
                           'direction: "docs/A#B.md"\n```\n')
        self.assertEqual(c.direction, "docs/A#B.md")


class TestContractDiscovery(unittest.TestCase):
    def test_either_filename_satisfies_the_slot(self):
        for name in ("CLAUDE.md", "AGENTS.md"):
            with self.subTest(name=name), TempRepo() as r:
                r.write(name, "# x\n")
                r.commit()
                self.assertEqual(find_contract(r.dir, [name]), name)

    def test_claude_md_wins_when_both_exist(self):
        with TempRepo() as r:
            r.write("CLAUDE.md", "# a\n")
            r.write("AGENTS.md", "# b\n")
            r.commit()
            self.assertEqual(
                find_contract(r.dir, ["CLAUDE.md", "AGENTS.md"]), "CLAUDE.md")

    def test_absent_contract_reports_an_error(self):
        with TempRepo() as r:
            r.write("README.md", "# x\n")
            r.commit()
            c = load(r.dir, ["README.md"])
            self.assertTrue(any("no agent contract" in e for e in c.errors))


if __name__ == "__main__":
    unittest.main()
