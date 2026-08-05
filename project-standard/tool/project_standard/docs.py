"""Document checks: stamps, scaffolding tokens, links, duplicate documents.

The carve-outs below are load-bearing. Without them the duplicate-backlog check
fires on `.github/ISSUE_TEMPLATE/todo.md`, on archived version directories and
on `docs/done/ROADMAP.md` — none of which is a second live roadmap, all of
which the standard elsewhere blesses as legitimately tracked history.
"""

import re
from fnmatch import fnmatch
from pathlib import Path

from . import findings as F
from .artifacts import resolve_slots

TODO_TOKEN = re.compile(r"<!--\s*TODO\(project-standard\)", re.I)
STAMP = re.compile(r"\*\*Last reviewed:\*\*\s*(\d{4}-\d{2}-\d{2})", re.I)
AS_OF = re.compile(r"\*\*As of:\*\*\s*v?(\d+\.\d+\.\d+)", re.I)
SCAFFOLDED = re.compile(r"\*\*Status:\*\*\s*scaffolded", re.I)
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)#][^)]*)\)")

# Directories that hold history, templates or archives. Excluded from every
# duplicate-document check.
EXCLUDED = (
    "*/archived/*", "archived/*",
    "*/archive/*", "archives/*", "*/archives/*",
    "docs/done/*", "*/history/*", "history/*",
    ".github/*", "*/.github/*",
    "docs/superpowers/*",
    "*think-day-*/*", "*dev-day-*/*",
    "*/v[0-9]*/*",
)

BACKLOG_NAMES = ("ROADMAP.md", "TODO.md", "BACKLOG.md", "PLAN.md",
                 "IMPLEMENTATION_ROADMAP.md", "NEXT_STEPS.md")
PRODUCT_TRUTH = ("FEATURE_MAP.md", "FEATURES.md", "CAPABILITIES.md",
                 "NORTH_STAR.md", "PRODUCT.md")
CANONICAL_BACKLOG = "docs/NEXT_STEPS.md"

DONE_MARKERS = re.compile(r"^\s*[-*]\s*\[x\]|~~[^~]+~~|✅", re.M)


def excluded(path):
    return any(fnmatch(path, pat) for pat in EXCLUDED)


def markdown_files(tracked):
    return [f for f in tracked if f.endswith(".md")]


def check(ctx):
    out = []
    tracked = list(ctx.tracked)
    docs = [f for f in markdown_files(tracked) if f.startswith("docs/")]
    required = {s.satisfied_by for s in resolve_slots(ctx) if s.satisfied_by}

    out += _tokens_and_stamps(ctx, tracked, docs, required)
    out += _links(ctx, tracked, required)
    out += _duplicates(ctx, tracked)
    out += _claude_dir(ctx, tracked)
    return out


def _read(ctx, rel):
    try:
        return (Path(ctx.repo) / rel).read_text(errors="ignore")
    except OSError:
        return ""


def _tokens_and_stamps(ctx, tracked, docs, required):
    out = []
    stamped = 0
    for rel in docs:
        text = _read(ctx, rel)
        head = text[:800]
        is_scaffold = bool(SCAFFOLDED.search(head))
        has_stamp = bool(STAMP.search(head))

        if has_stamp:
            stamped += 1
        if is_scaffold and has_stamp:
            out.append(F.error(
                "25", "document is marked scaffolded and also carries a trust "
                      "stamp — a generated skeleton was never read against the code",
                path=rel))

        m = AS_OF.search(head)
        if m and ctx.version and _older(m.group(1), ctx.version):
            out.append(F.warn(
                "13", f"unverified since v{m.group(1)} (current {ctx.version})",
                path=rel))

    for rel in sorted(required):
        text = _read(ctx, rel)
        hit = TODO_TOKEN.search(text)
        if hit:
            line = text[:hit.start()].count("\n") + 1
            out.append(F.error(
                "23", "required document still carries an unresolved "
                      "TODO(project-standard) token — scaffolded, not written",
                path=rel, line=line))

    if docs:
        out.append(F.warn(
            "12", f"trust stamps: {stamped}/{len(docs)} documents under docs/ "
                  f"carry `Last reviewed:`"))

    # Check 24 — a code map that names paths which do not exist.
    if "docs/PROJECT_MAP.md" in required:
        text = _read(ctx, "docs/PROJECT_MAP.md")
        for path in _backticked_paths(text):
            if not (Path(ctx.repo) / path).exists():
                out.append(F.error(
                    "24", f"code map names `{path}`, which does not exist",
                    path="docs/PROJECT_MAP.md"))
    return out


def _backticked_paths(text):
    out = []
    for m in re.finditer(r"`([A-Za-z0-9_./-]+/[A-Za-z0-9_./-]*)`", text or ""):
        cand = m.group(1)
        if cand.startswith(("http", "//")) or " " in cand:
            continue
        out.append(cand.rstrip("/"))
    return sorted(set(out))


def _links(ctx, tracked, required):
    """Broken links error inside required docs, warn everywhere else."""
    out = []
    tracked_set = set(tracked)
    for rel in markdown_files(tracked):
        if excluded(rel):
            continue
        text = _read(ctx, rel)
        base = Path(rel).parent
        for m in MD_LINK.finditer(text):
            target = m.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#")[0].strip()
            if not target:
                continue
            resolved = str(Path(*(base / target).parts)).replace("\\", "/")
            try:
                resolved = str((base / target).resolve().relative_to(
                    Path(ctx.repo).resolve()))
            except (ValueError, OSError):
                pass
            exists = resolved in tracked_set or (Path(ctx.repo) / resolved).exists()
            if exists:
                continue
            line = text[:m.start()].count("\n") + 1
            if rel in required:
                out.append(F.error("4", f"broken link to `{target}`",
                                   path=rel, line=line))
            else:
                out.append(F.warn("19", f"broken link to `{target}`",
                                  path=rel, line=line))
    return out


def _duplicates(ctx, tracked):
    out = []
    live = [f for f in markdown_files(tracked) if not excluded(f)]

    backlogs = [f for f in live if Path(f).name in BACKLOG_NAMES]
    others = [f for f in backlogs if f != CANONICAL_BACKLOG]
    if CANONICAL_BACKLOG in backlogs and others:
        for f in others:
            out.append(F.error(
                "26", f"second backlog beside `{CANONICAL_BACKLOG}` — merge it in; "
                      f"two roadmaps disagreeing is worse than none", path=f))
    elif len(others) > 1:
        for f in others[1:]:
            out.append(F.error(
                "26", "more than one backlog document and no canonical "
                      "`docs/NEXT_STEPS.md`", path=f))

    truth = [f for f in live if Path(f).name in PRODUCT_TRUTH]
    if len(truth) > 1:
        out.append(F.warn(
            "18", "more than one document asserts product truth: "
                  + ", ".join(f"`{t}`" for t in sorted(truth))))

    if CANONICAL_BACKLOG in tracked:
        text = _read(ctx, CANONICAL_BACKLOG)
        hits = len(DONE_MARKERS.findall(text))
        if hits:
            out.append(F.warn(
                "28", f"{hits} line(s) look like completed items — the roadmap is "
                      f"future-only; done rows are deleted, not kept "
                      f"(pattern matching, needs a human eye)",
                path=CANONICAL_BACKLOG))

    prds = [f for f in tracked if f.startswith("docs/prds/") and f.endswith(".md")]
    for rel in prds:
        if Path(rel).name in ("README.md",):
            continue
        text = _read(ctx, rel)
        if not re.search(r"\*\*Status:\*\*", text, re.I):
            out.append(F.error("33", "PRD carries no `Status:` header", path=rel))
        if re.search(r"implementation[-_ ]status|current state", Path(rel).name,
                     re.I):
            out.append(F.warn(
                "36", "a state-asserting document inside docs/prds/ will be read "
                      "as current and will drift — it belongs in FEATURE_MAP.md",
                path=rel))

    stray = [f for f in tracked
             if re.search(r"(^|/)PRDs?[-_./]", f, re.I)
             and not f.startswith("docs/prds/") and not excluded(f)
             and f.endswith(".md")]
    for f in stray:
        out.append(F.error(
            "32", "PRD lives outside `docs/prds/`", path=f))
    return out


def _claude_dir(ctx, tracked):
    out = []
    repo = Path(ctx.repo)
    for d in (".claude/agents", ".claude/skills"):
        if (repo / d).is_dir() and not any(f.startswith(d + "/") for f in tracked):
            out.append(F.warn(
                "22", f"`{d}/` exists but nothing in it is tracked — project "
                      f"agents and skills are project knowledge"))
    return out


def _older(a, b):
    def parts(v):
        return tuple(int(x) for x in re.findall(r"\d+", v)[:3] or [0])
    return parts(a) < parts(b)
