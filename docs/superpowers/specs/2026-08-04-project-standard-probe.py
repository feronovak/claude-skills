#!/usr/bin/env python3
"""Throwaway probe: apply the project-standard mechanical checks to every repo
under ~/projects/apps. Prototype of `project_standard.py check`, stdlib only."""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

APPS = Path.home() / "projects" / "apps"

LOCAL_ONLY = [
    "docs/exec-summaries/", "session-notes/", "logs/", "test_results/",
    ".agenthub/", ".playwright-mcp/", ".interface-design/", ".cursor/", ".ruff_cache/",
    ".claude/settings.local.json", ".claude/worktrees/", ".claude/scheduled_tasks.lock",
]
TRACK_CLAUDE = [".claude/agents/", ".claude/skills/"]

SEMVER_TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)(?:-(.+))?$")


def git(repo, *args, ok=(0,)):
    p = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, text=True)
    return p.stdout.strip() if p.returncode in ok else None


def detect_http_api(repo):
    hits = []
    for pat, label in [
        (r"FastAPI\(", "FastAPI"), (r"Flask\(__name__", "Flask"),
        (r"\bapp\.listen\(", "Express"),
    ]:
        out = git(repo, "grep", "-l", "-E", pat, "--", "*.py", "*.ts", "*.js") or ""
        if out:
            hits.append(f"{label}:{out.splitlines()[0]}")
    routes = git(repo, "ls-files", "*/api/*/route.ts", "*/api/*/route.js",
                 "pages/api/*", "app/api/*") or ""
    if routes:
        hits.append(f"routes:{len(routes.splitlines())}")
    return hits


METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS")
_M = "|".join(METHODS)
# `GET /x`, `GET·POST /x`, and markdown table rows `| GET·POST | \`/x\` |`
DOC_INLINE = re.compile(rf"\b((?:{_M})(?:\s*[·/,]\s*(?:{_M}))*)\s+(/[^\s`\"'|)\],]*)")
DOC_ROW = re.compile(
    rf"^\s*\|\s*\**((?:{_M})(?:\s*[·/,]\s*(?:{_M}))*)\**\s*\|\s*\**`?([^`|*]+?)`?\**\s*\|",
    re.M)
FLASK_RT = re.compile(
    r"""@\w+\.route\(\s*["']([^"']+)["'](?:[^)]*methods\s*=\s*\[([^\]]*)\])?""", re.S)
EXPRESS_RT = re.compile(
    r"""\b(?:app|router)\.(get|post|put|patch|delete)\(\s*["'`]([^"'`]+)""")


def norm(path):
    """Collapse parameter syntax so <int:id>, [id] and :id compare equal."""
    p = re.sub(r"<[^>]*>|\[[^\]]*\]|:\w+", "{}", path)
    p = re.sub(r"/+", "/", p).rstrip("/")
    return p or "/"


def code_endpoints(repo):
    """Enumerate (METHOD, path) the code actually exposes.

    Returns (endpoints, unresolved) — `unresolved` names frameworks whose real
    paths cannot be derived statically, so the caller reports a limitation
    instead of emitting false 'undocumented route' findings."""
    eps, unresolved = set(), []
    files = (git(repo, "ls-files") or "").splitlines()

    # Flask: a decorator's path is relative to its blueprint, and blueprints
    # nest — the prefix is composed at register_blueprint time, across modules.
    # Static regex cannot resolve that; app.url_map at dev time can.
    py = [f for f in files if f.endswith(".py")]
    if any(FLASK_RT.search((repo / f).read_text(errors="ignore"))
           for f in py if (repo / f).is_file()):
        nested = any("register_blueprint" in (repo / f).read_text(errors="ignore")
                     for f in py if (repo / f).is_file())
        unresolved.append("flask" + (" (nested blueprints)" if nested else ""))

    for f in files:
        m = re.match(r"(?:src/)?(?:app|pages)/(api/.+?)/route\.[tj]sx?$", f)
        if m:
            try:
                src = (repo / f).read_text(errors="ignore")
            except Exception:
                continue
            for meth in METHODS:
                if re.search(rf"export\s+(?:async\s+)?function\s+{meth}\b", src) or \
                   re.search(rf"export\s+const\s+{meth}\b", src):
                    eps.add((meth, norm("/" + m.group(1))))
        elif re.match(r"(?:src/)?pages/api/.+\.[tj]sx?$", f):
            p = re.sub(r"^(?:src/)?pages", "", f)
            p = re.sub(r"\.[tj]sx?$", "", p)
            p = re.sub(r"/index$", "", p)
            eps.add(("ANY", norm(p)))

    for f in files:
        if not f.endswith((".ts", ".js", ".mjs")) or "node_modules" in f:
            continue
        try:
            src = (repo / f).read_text(errors="ignore")
        except Exception:
            continue
        for meth, path in EXPRESS_RT.findall(src):
            if path.startswith("/"):
                eps.add((meth.upper(), norm(path)))
    return eps, unresolved


def doc_endpoints(repo):
    ref = repo / "docs" / "API_REFERENCE.md"
    if not ref.exists():
        return None
    txt = ref.read_text(errors="ignore")
    out = set()
    for methods, path in list(DOC_ROW.findall(txt)) + list(DOC_INLINE.findall(txt)):
        path = path.strip()
        if not path.startswith("/"):
            continue
        for m in re.findall(_M, methods):
            out.add((m.upper(), norm(path)))
    return out


def detect_channels(repo):
    ch = []
    files = (git(repo, "ls-files") or "").splitlines()
    fs = set(files)
    if any(f.endswith("manifest.json") and "node_modules" not in f for f in files):
        for f in files:
            if f.endswith("manifest.json") and "node_modules" not in f:
                try:
                    if "manifest_version" in (repo / f).read_text():
                        ch.append("extension")
                        break
                except Exception:
                    pass
    if any(f.startswith("android-native/") or "capacitor.config" in f for f in files):
        ch.append("mobile")
    if any(f.startswith("src-tauri/") or "electron" in f.lower() for f in files):
        ch.append("desktop")
    if not ch or any(f.startswith(("src/", "app/", "public/")) for f in files):
        ch.insert(0, "web")
    return list(dict.fromkeys(ch))


def detect_profile(repo):
    pkg = repo / "package.json"
    pyp = repo / "pyproject.toml"
    if pkg.exists():
        try:
            d = json.loads(pkg.read_text())
            if any(k in d for k in ("publishConfig", "bin")) or \
               (d.get("files") and not d.get("private")):
                return "library"
        except Exception:
            pass
    if pyp.exists():
        t = pyp.read_text()
        if "[project.scripts]" in t or "build-backend" in t:
            return "library"
    files = (git(repo, "ls-files") or "").splitlines()
    src = [f for f in files if f.startswith(("src/", "app/", "lib/", "components/"))
           or f.endswith((".py", ".ts", ".tsx", ".js", ".jsx"))]
    return "product" if src else "docs"


def version_source(repo):
    pkg, pyp, ver = repo / "package.json", repo / "pyproject.toml", repo / "VERSION"
    out = []
    if pkg.exists():
        try:
            v = json.loads(pkg.read_text()).get("version")
            if v:
                out.append(("package.json", v))
        except Exception:
            pass
    if pyp.exists():
        m = re.search(r'^version\s*=\s*"([^"]+)"', pyp.read_text(), re.M)
        if m:
            out.append(("pyproject.toml", m.group(1)))
    if ver.exists():
        out.append(("VERSION", ver.read_text().strip()))
    return out


def check(repo):
    name = repo.name
    r = {"repo": name, "errors": [], "warns": [], "info": {}}
    tracked = set((git(repo, "ls-files") or "").splitlines())

    profile = detect_profile(repo)
    api = detect_http_api(repo)
    channels = detect_channels(repo)
    r["info"]["profile"] = profile
    r["info"]["http-api"] = "yes" if api else "no"
    r["info"]["api-evidence"] = ",".join(api)[:60]
    r["info"]["channels"] = "+".join(channels)

    # 1 required artifacts
    contract = [f for f in ("CLAUDE.md", "AGENTS.md") if (repo / f).exists()]
    if not contract:
        r["errors"].append("no agent contract (CLAUDE.md or AGENTS.md)")
    r["info"]["contract"] = "+".join(contract) or "-"

    required = ["README.md", "docs/DOCMAP.md"]
    if profile != "docs":
        required += ["docs/PROJECT_MAP.md", "docs/FEATURE_MAP.md",
                     "docs/DEVELOPMENT_FLOW.md", "CHANGELOG.md"]
    if api:
        required += ["docs/API_REFERENCE.md"]
    if profile == "library":
        required += ["CONTRIBUTING.md", "SECURITY.md", "RELEASING.md"]
    missing = [f for f in required if not (repo / f).exists()]
    if missing:
        r["errors"].append(f"missing {len(missing)}: {', '.join(missing)}")

    # 2 contract required sections (rough proxy)
    if contract:
        txt = (repo / contract[0]).read_text(errors="ignore").lower()
        gaps = [s for s, k in [("critical-paths", "critical-path"),
                               ("git-hygiene", "co-authored"),
                               ("docmap pointer", "docmap")] if k not in txt]
        if gaps:
            r["errors"].append("contract missing: " + ", ".join(gaps))

    # 10a/10b/10c endpoint coverage
    code_eps, unresolved = code_endpoints(repo)
    doc_eps = doc_endpoints(repo)
    if unresolved:
        r["warns"].append(
            "route enumeration needs runtime introspection for "
            + ", ".join(unresolved)
            + f"; documented set has {len(doc_eps) if doc_eps else 0} entries, not diffed")
        r["info"]["coverage"] = f"?/{len(doc_eps) if doc_eps else 0}"
    elif code_eps:
        if doc_eps is None:
            r["errors"].append(
                f"{len(code_eps)} routes in code, no docs/API_REFERENCE.md — 0/{len(code_eps)} documented")
            r["info"]["coverage"] = f"0/{len(code_eps)}"
        else:
            undoc = sorted(code_eps - doc_eps)
            phantom = sorted(doc_eps - code_eps)
            r["info"]["coverage"] = f"{len(code_eps) - len(undoc)}/{len(code_eps)}"
            if undoc:
                s = ", ".join(f"{m} {p}" for m, p in undoc[:4])
                r["errors"].append(
                    f"{len(undoc)} undocumented route(s): {s}"
                    + (" …" if len(undoc) > 4 else ""))
            if phantom:
                s = ", ".join(f"{m} {p}" for m, p in phantom[:4])
                r["errors"].append(
                    f"{len(phantom)} documented route(s) not in code: {s}"
                    + (" …" if len(phantom) > 4 else ""))
    elif doc_eps:
        r["info"]["coverage"] = f"0/{len(doc_eps)}?"
        r["warns"].append(
            f"API_REFERENCE.md documents {len(doc_eps)} routes but none detected in code")
    else:
        r["info"]["coverage"] = "-"

    # 5 release agreement
    vs = version_source(repo)
    if len(vs) > 1:
        r["errors"].append("multiple version sources: " +
                           ", ".join(f"{s}={v}" for s, v in vs))
    tag = git(repo, "describe", "--tags", "--abbrev=0")
    r["info"]["version"] = vs[0][1] if vs else "-"
    r["info"]["tag"] = tag or "-"
    if tag and vs:
        m = SEMVER_TAG.match(tag)
        if m:
            base = f"{m.group(1)}.{m.group(2)}.{m.group(3)}"
            prerelease = bool(m.group(4))
            head_tags = (git(repo, "tag", "--points-at", "HEAD") or "").splitlines()
            if tag in head_tags:
                if base != vs[0][1]:
                    r["errors"].append(f"tag {tag} vs {vs[0][0]}={vs[0][1]}")
                if not prerelease and (repo / "CHANGELOG.md").exists():
                    if f"[{base}]" not in (repo / "CHANGELOG.md").read_text(errors="ignore") \
                       and f"## {base}" not in (repo / "CHANGELOG.md").read_text(errors="ignore"):
                        r["errors"].append(f"no CHANGELOG section for {base}")
    # 15 higher semver tag exists
    alltags = [t for t in (git(repo, "tag") or "").splitlines() if SEMVER_TAG.match(t)]
    if vs and alltags:
        cur = tuple(int(x) for x in re.findall(r"\d+", vs[0][1])[:3] or [0])
        hi = [t for t in alltags
              if tuple(int(x) for x in SEMVER_TAG.match(t).groups()[:3]) > cur]
        if hi:
            r["warns"].append(f"tags above current version: {', '.join(sorted(hi))}")

    # 7 tracked local-only
    leaked = sorted({p for p in LOCAL_ONLY
                     for f in tracked if f == p.rstrip("/") or f.startswith(p)})
    if leaked:
        r["errors"].append("tracked local-only: " + ", ".join(leaked))

    # 8 Claude trailers
    log = git(repo, "log", "--format=%an%x00%b", "-500") or ""
    trailers = sum(1 for l in log.split("\n")
                   if "co-authored-by: claude" in l.lower()
                   or "generated with [claude" in l.lower())
    authors = {l.split("\x00")[0] for l in log.split("\n") if "\x00" in l}
    if trailers:
        r["errors"].append(f"{trailers} Claude trailers in last 500 commits")
    if any("claude" in a.lower() for a in authors):
        r["errors"].append("Claude appears as commit author")

    # 9 gitignore block
    gi = (repo / ".gitignore").read_text(errors="ignore") if (repo / ".gitignore").exists() else ""
    missing_ign = [p for p in LOCAL_ONLY if p.rstrip("/").split("/")[-1] not in gi
                   and p.rstrip("/") not in gi]
    if missing_ign:
        r["errors"].append(f"gitignore missing {len(missing_ign)}/{len(LOCAL_ONLY)} local-only entries")

    # 22 .claude tracked
    for p in TRACK_CLAUDE:
        if (repo / p).exists() and not any(f.startswith(p) for f in tracked):
            r["warns"].append(f"{p} present but untracked")

    # 12 stamp coverage
    docs = sorted((repo / "docs").rglob("*.md")) if (repo / "docs").exists() else []
    stamped = sum(1 for d in docs
                  if "last reviewed" in d.read_text(errors="ignore")[:800].lower())
    r["info"]["stamps"] = f"{stamped}/{len(docs)}" if docs else "0/0"

    # 16 workspaces
    if (repo / "package.json").exists():
        try:
            if json.loads((repo / "package.json").read_text()).get("workspaces"):
                r["warns"].append("workspaces detected, root only validated")
        except Exception:
            pass
    return r


def main():
    args = sys.argv[1:]
    only = [a.split("=", 1)[1] for a in args if a.startswith("--only=")]
    want = [a.split("=", 1)[1] for a in args if a.startswith("--repo=")]
    as_json = "--json" in args

    repos = sorted(p for p in APPS.iterdir() if (p / ".git").exists())
    if want:
        repos = [p for p in repos if p.name in want]
        if not repos:
            print(f"no such repo under {APPS}", file=sys.stderr)
            return 2
    results = [check(p) for p in repos]
    if only:
        for r in results:
            r["errors"] = [e for e in r["errors"] if any(k in e.lower() for k in only)]
            r["warns"] = [w for w in r["warns"] if any(k in w.lower() for k in only)]
    if as_json:
        print(json.dumps(results, indent=2))
        return 1 if any(r["errors"] for r in results) else 0
    hdr = (f"{'repo':<28}{'profile':<9}{'channels':<20}{'contract':<12}"
           f"{'ver':<9}{'tag':<20}{'api cov':<10}{'stamps':<9}{'E':>3}{'W':>3}")
    print(hdr)
    print("-" * len(hdr))
    for r in results:
        i = r["info"]
        print(f"{r['repo']:<28}{i['profile']:<9}{i['channels']:<20}"
              f"{i['contract']:<12}{i['version']:<9}{i['tag']:<20}"
              f"{i.get('coverage', '-'):<10}{i['stamps']:<9}"
              f"{len(r['errors']):>3}{len(r['warns']):>3}")
    print()
    for r in results:
        if not (r["errors"] or r["warns"]):
            continue
        print(f"== {r['repo']}  (api evidence: {r['info']['api-evidence'] or 'none'})")
        for e in r["errors"]:
            print(f"   ERROR  {e}")
        for w in r["warns"]:
            print(f"   warn   {w}")
        print()
    tot_e = sum(len(r["errors"]) for r in results)
    tot_w = sum(len(r["warns"]) for r in results)
    print(f"TOTAL across {len(results)} repos: {tot_e} errors, {tot_w} warns")
    return 1 if tot_e else 0


if __name__ == "__main__":
    sys.exit(main() or 0)
