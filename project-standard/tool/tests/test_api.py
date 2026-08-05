import json
import unittest

from fixtures import TempRepo, by_check, ctx_for, sev_for
from project_standard import api
from project_standard.gitio import Git

# The strongest API document in the fleet writes endpoints as table rows with
# method and path in separate cells. A rule demanding a literal adjacent
# `GET /path` fails it and would demand a rewrite into a worse format.
TABLE_DOC = """# API Reference

| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | `/api/vet` | public | Vet one listing |
| GET | `/api/me` | require_auth | Account summary |
| GET·POST | `/api/me/hunts` | require_auth | List / create hunts |
| PATCH·DELETE | `/api/me/hunts/<id>` | owner | Update / delete |
"""


class TestDocParsing(unittest.TestCase):
    def test_table_rows_are_recognised(self):
        eps = api.parse_doc_endpoints(TABLE_DOC)
        self.assertIn(("POST", "/api/vet"), eps)
        self.assertIn(("GET", "/api/me"), eps)

    def test_combined_methods_expand_to_one_entry_each(self):
        eps = api.parse_doc_endpoints(TABLE_DOC)
        self.assertIn(("GET", "/api/me/hunts"), eps)
        self.assertIn(("POST", "/api/me/hunts"), eps)
        self.assertIn(("PATCH", "/api/me/hunts/{}"), eps)
        self.assertIn(("DELETE", "/api/me/hunts/{}"), eps)

    def test_inline_prose_form_also_works(self):
        eps = api.parse_doc_endpoints("### GET /api/health\n\nLiveness.\n")
        self.assertIn(("GET", "/api/health"), eps)

    def test_parameter_syntaxes_normalise_together(self):
        self.assertEqual(api.normalise("/a/<int:id>"), api.normalise("/a/[id]"))
        self.assertEqual(api.normalise("/a/:id"), api.normalise("/a/<id>"))


class TestEnumeration(unittest.TestCase):
    def test_next_routes_are_enumerated_by_exported_method(self):
        with TempRepo() as r:
            r.write("app/api/vet/route.ts",
                    "export async function POST() {}\n"
                    "export async function GET() {}\n")
            r.commit()
            eps, unresolved = api.code_endpoints(r.dir, Git(r.dir).ls_files())
            self.assertEqual(eps, {("POST", "/api/vet"), ("GET", "/api/vet")})
            self.assertEqual(unresolved, [])

    def test_flask_is_reported_unresolvable_rather_than_guessed(self):
        """Regex over decorators produced 107 phantom routes against a document
        correctly describing 55. A checker that cannot enumerate says so."""
        with TempRepo() as r:
            r.write("app/__init__.py",
                    "from flask import Blueprint\n"
                    "bp = Blueprint('x', __name__)\n"
                    "@bp.route('/thing')\ndef t(): pass\n")
            r.commit()
            eps, unresolved = api.code_endpoints(r.dir, Git(r.dir).ls_files())
            self.assertEqual(eps, set())
            self.assertIn("flask", unresolved)

    def test_manifest_is_preferred_over_heuristics(self):
        with TempRepo() as r:
            r.write("app/__init__.py",
                    "from flask import Blueprint\nbp = Blueprint('x', __name__)\n")
            r.write("docs/api/routes.json", json.dumps(
                {"generated_by": "t",
                 "routes": [{"method": "POST", "path": "/api/vet"}]}))
            r.commit()
            eps, unresolved = api.code_endpoints(r.dir, Git(r.dir).ls_files())
            self.assertEqual(eps, {("POST", "/api/vet")})
            self.assertEqual(unresolved, [])


class TestCoverage(unittest.TestCase):
    def _api_repo(self, doc=None, routes=("POST",)):
        r = TempRepo().__enter__()
        r.standard_repo()
        for method in routes:
            r.write(f"app/api/{method.lower()}thing/route.ts",
                    f"export async function {method}() {{}}\n")
        if doc is not None:
            r.write("docs/API_REFERENCE.md", doc)
        r.commit()
        return r

    def test_no_reference_at_all_is_an_error(self):
        r = self._api_repo(doc=None)
        try:
            found = by_check(api.check(ctx_for(r.dir)), "10a")
            self.assertEqual(found[0].severity, "error")
            self.assertIn("0/1", found[0].message)
        finally:
            r.__exit__()

    def test_undocumented_route_is_an_error(self):
        r = self._api_repo(doc="# API\n\n| Method | Path |\n|---|---|\n")
        try:
            self.assertEqual(sev_for(api.check(ctx_for(r.dir)), "10a"), "error")
        finally:
            r.__exit__()

    def test_documented_route_that_no_longer_exists_is_an_error(self):
        r = self._api_repo(
            doc="# API\n\n| Method | Path |\n|---|---|\n"
                "| POST | `/api/postthing` |\n| GET | `/api/removed` |\n")
        try:
            found = by_check(api.check(ctx_for(r.dir)), "10b")
            self.assertEqual(found[0].severity, "error")
            self.assertIn("/api/removed", found[0].message)
        finally:
            r.__exit__()

    def test_full_coverage_produces_no_error(self):
        r = self._api_repo(
            doc="# API\n\n| Method | Path |\n|---|---|\n"
                "| POST | `/api/postthing` |\n")
        try:
            findings = api.check(ctx_for(r.dir))
            self.assertEqual(by_check(findings, "10a"), [])
            self.assertEqual(by_check(findings, "10b"), [])
            self.assertTrue(any("coverage: 1/1" in f.message
                                for f in by_check(findings, "10")))
        finally:
            r.__exit__()

    def test_no_http_api_means_no_api_findings(self):
        with TempRepo() as r:
            r.standard_repo()
            r.commit()
            self.assertEqual(api.check(ctx_for(r.dir)), [])


if __name__ == "__main__":
    unittest.main()
