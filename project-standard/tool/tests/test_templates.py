"""Templates must admit what they do not know.

A convincing skeleton that passes the presence check and gets indexed by DOCMAP
is worse than the missing file: a reader coming in cold now believes it.
"""

import re
import unittest
from pathlib import Path

from project_standard.docs import SCAFFOLDED, STAMP, TODO_TOKEN

TEMPLATES = Path(__file__).resolve().parents[2] / "templates"

# Documents whose whole purpose is to assert something a human must supply.
MUST_BE_SCAFFOLD_MARKED = {
    "PROJECT_MAP.md.tmpl", "FEATURE_MAP.md.tmpl", "NEXT_STEPS.md.tmpl",
    "DEVELOPMENT_FLOW.md.tmpl", "NORTH_STAR.md.tmpl", "API_REFERENCE.md.tmpl",
}


def templates():
    return sorted(TEMPLATES.glob("*.tmpl"))


class TestTemplates(unittest.TestCase):
    def test_templates_exist(self):
        self.assertTrue(templates(), "no templates found")

    def test_every_template_admits_an_unwritten_field(self):
        for path in templates():
            with self.subTest(template=path.name):
                self.assertTrue(
                    TODO_TOKEN.search(path.read_text()),
                    f"{path.name} carries no TODO(project-standard) token, so a "
                    f"scaffold from it would pass check 23 while asserting nothing")

    def test_no_template_carries_a_trust_stamp(self):
        """A tool never stamps the document it just wrote."""
        for path in templates():
            with self.subTest(template=path.name):
                self.assertIsNone(
                    STAMP.search(path.read_text()),
                    f"{path.name} carries a Last reviewed stamp")

    def test_judgement_documents_declare_themselves_scaffolded(self):
        for name in MUST_BE_SCAFFOLD_MARKED:
            with self.subTest(template=name):
                text = (TEMPLATES / name).read_text()
                self.assertTrue(SCAFFOLDED.search(text),
                                f"{name} must carry **Status:** scaffolded")

    def test_no_template_contains_plausible_placeholder_prose(self):
        """`Lorem ipsum`, `TBD` and friends read as content. Tokens do not."""
        banned = re.compile(r"lorem ipsum|\bTBD\b|\bXXX\b|coming soon", re.I)
        for path in templates():
            with self.subTest(template=path.name):
                self.assertIsNone(banned.search(path.read_text()))

    def test_agent_contract_template_carries_the_machine_block(self):
        text = (TEMPLATES / "agent-contract.md.tmpl").read_text()
        self.assertIn("## project-standard", text)
        self.assertIn("adopted:", text)
        self.assertIn("critical-paths:", text)
        self.assertIn("DOCMAP", text)
        self.assertIn("Co-Authored-By", text)


if __name__ == "__main__":
    unittest.main()
