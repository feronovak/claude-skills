"""Endpoint coverage: what the code exposes versus what the reference documents.

Two hard-won rules:

  - The document format rule accepts what good documentation already looks
    like. A table with the method and path in separate cells is the strongest
    API doc in this fleet; an earlier rule demanding a literal adjacent
    `GET /path` failed it and would have demanded a rewrite into a worse
    format to satisfy a parser.
  - Enumeration comes from the framework, not from scraping decorators. A
    Flask route's path is relative to its blueprint, blueprints nest, and the
    real path is composed at registration across modules. Regex over
    decorators produced 107 phantom routes against a document correctly
    describing 55. Where enumeration cannot be resolved, we warn — a checker
    that cannot enumerate says so rather than inventing findings.
"""

import json
import re
from pathlib import Path

from . import findings as F

METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS")
_M = "|".join(METHODS)

DOC_INLINE = re.compile(rf"\b((?:{_M})(?:\s*[·/,|]\s*(?:{_M}))*)\s+(/[^\s`\"'|)\],]*)")
DOC_ROW = re.compile(
    rf"^\s*\|\s*\**((?:{_M})(?:\s*[·/,]\s*(?:{_M}))*)\**\s*\|\s*\**`?([^`|*]+?)`?\**\s*\|",
    re.M)

NEXT_ROUTE = re.compile(r"^(?:src/)?(?:app|pages)/(?P<path>.*api/.*)/route\.[tj]sx?$")
NEXT_PAGES_API = re.compile(r"^(?:src/)?pages/(?P<path>api/.+)\.[tj]sx?$")
EXPORTED = r"export\s+(?:async\s+)?(?:function|const)\s+{m}\b"

FLASK_SIGNS = re.compile(r"\bBlueprint\(|@\w+\.route\(")
FASTAPI_SIGNS = re.compile(r"\bFastAPI\(|@\w+\.(?:get|post|put|patch|delete)\(")

MANIFEST = "docs/api/routes.json"
REFERENCE = "docs/API_REFERENCE.md"


def normalise(path):
    """Collapse parameter syntax so <int:id>, [id] and :id compare equal."""
    p = re.sub(r"<[^>]*>|\[[^\]]*\]|:\w+", "{}", path or "")
    p = re.sub(r"/+", "/", p).rstrip("/")
    return p or "/"


def parse_doc_endpoints(text):
    out = set()
    pairs = list(DOC_ROW.findall(text or "")) + list(DOC_INLINE.findall(text or ""))
    for methods, path in pairs:
        path = path.strip()
        if not path.startswith("/"):
            continue
        for m in re.findall(_M, methods):
            out.add((m.upper(), normalise(path)))
    return out


def doc_endpoints(repo, tracked):
    if REFERENCE not in set(tracked):
        return None
    text = (Path(repo) / REFERENCE).read_text(errors="ignore")
    return parse_doc_endpoints(text)


def code_endpoints(repo, tracked):
    """-> (endpoints, unresolved_frameworks)"""
    repo = Path(repo)
    eps, unresolved = set(), []

    manifest = repo / MANIFEST
    if manifest.is_file():
        try:
            data = json.loads(manifest.read_text(errors="ignore"))
            for r in data.get("routes", []):
                eps.add((str(r["method"]).upper(), normalise(r["path"])))
            return eps, unresolved
        except (ValueError, KeyError, TypeError):
            unresolved.append("routes.json (unreadable)")

    for rel in tracked:
        m = NEXT_ROUTE.match(rel)
        if m:
            src = _read(repo, rel)
            for meth in METHODS:
                if re.search(EXPORTED.format(m=meth), src):
                    eps.add((meth, normalise("/" + m.group("path"))))
            continue
        m = NEXT_PAGES_API.match(rel)
        if m:
            path = re.sub(r"/index$", "", "/" + m.group("path"))
            eps.add(("ANY", normalise(path)))

    frameworks = set()
    for rel in tracked:
        if not rel.endswith(".py") or "/test" in rel:
            continue
        src = _read(repo, rel)
        if FASTAPI_SIGNS.search(src):
            frameworks.add("fastapi")
        elif FLASK_SIGNS.search(src):
            frameworks.add("flask")
    for fw in sorted(frameworks):
        unresolved.append(fw)

    return eps, unresolved


def check(ctx):
    out = []
    if not ctx.resolved.http_api:
        return out

    tracked = set(ctx.tracked)
    docs = doc_endpoints(ctx.repo, tracked)
    code, unresolved = code_endpoints(ctx.repo, tracked)

    if unresolved:
        out.append(F.warn(
            "10d", "route enumeration needs the framework's own route table for "
                   + ", ".join(unresolved)
                   + f"; run `project-standard routes` to write {MANIFEST}. "
                   + (f"The reference documents {len(docs)} endpoint(s), "
                      f"not diffed." if docs else
                      "No API reference to compare against.")))
        return out

    if docs is None:
        out.append(F.error(
            "10a", f"{len(code)} route(s) in code and no `{REFERENCE}` — "
                   f"0/{len(code)} documented"))
        return out

    undocumented = sorted(code - docs)
    phantom = sorted(docs - code)

    baseline = _baseline(ctx)
    covered = len(code) - len(undocumented)
    out.append(F.warn("10", f"endpoint coverage: {covered}/{len(code)} documented"))

    if undocumented:
        shown = ", ".join(f"{m} {p}" for m, p in undocumented[:5])
        severity = F.ERROR
        note = ""
        if baseline is not None and covered >= baseline:
            severity = F.WARN
            note = (f" — at or above the declared api-coverage baseline "
                    f"({baseline}), so this is debt, not a regression")
        out.append(F.Finding(
            "10a", severity,
            f"{len(undocumented)} undocumented route(s): {shown}"
            + (" …" if len(undocumented) > 5 else "") + note))

    if phantom:
        shown = ", ".join(f"{m} {p}" for m, p in phantom[:5])
        out.append(F.error(
            "10b", f"{len(phantom)} documented route(s) no longer exist in code: "
                   f"{shown}" + (" …" if len(phantom) > 5 else ""),
            path=REFERENCE))

    out += _freshness(ctx, tracked)
    return out


def _baseline(ctx):
    raw = ctx.contract.raw.get("api-coverage")
    if raw is None:
        return None
    try:
        return int(str(raw).split("/")[0])
    except (ValueError, TypeError):
        return None


def _freshness(ctx, tracked):
    """Check 10c — compared by last-commit time, never mtime.

    Git does not store mtimes; a fresh clone stamps every file with the
    checkout time, so an mtime comparison in CI passes or fails at random.
    """
    out = []
    spec = next((p for p in (MANIFEST, "docs/api/openapi.yaml") if p in tracked),
                None)
    if not spec:
        return out
    spec_at = ctx.git.file_committed_at(spec)
    if not spec_at:
        return out
    for rel in tracked:
        if not (NEXT_ROUTE.match(rel) or NEXT_PAGES_API.match(rel)):
            continue
        if ctx.git.file_committed_at(rel) > spec_at:
            out.append(F.error(
                "10c", f"`{spec}` was last committed before the routes it "
                       f"documents (e.g. `{rel}`)", path=spec))
            break
    return out


def _read(repo, rel, limit=400_000):
    p = Path(repo) / rel
    try:
        if p.is_file() and p.stat().st_size <= limit:
            return p.read_text(errors="ignore")
    except OSError:
        pass
    return ""
