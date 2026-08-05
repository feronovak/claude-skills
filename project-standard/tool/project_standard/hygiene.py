"""Local-only paths, attribution, and hook reachability.

Attribution has four markers, not one. The harness appends several
independently, so guarding the trailer alone leaves the rule half-enforced —
a message stripped of `Co-Authored-By` but keeping a session URL still names
Claude, and that is the one that was actually getting through.

The pull-request body is a fifth marker with no git-side guard at all. Git
hooks never see PR bodies. That is stated, not papered over.
"""

import re
from fnmatch import fnmatch
from pathlib import Path

from . import defaults, findings as F

# Kept as a module attribute for callers and tests; the effective set for a
# given repo comes from defaults.local_only_paths(contract), which lets a repo
# extend or replace it. A standard that hardcodes one team's tooling
# directories smuggles that team's habits in as best practice.
LOCAL_ONLY = tuple(defaults.LOCAL_ONLY_COMMON) + tuple(defaults.LOCAL_ONLY_HOUSE)

# Exact paths catch the convention; a summary written outside it needs a
# pattern, and a filename is a hint rather than proof.
LOCAL_ONLY_PATTERNS = defaults.LOCAL_ONLY_PATTERNS

ATTRIBUTION = (
    ("8a", re.compile(r"^\s*co-authored-by:.*claude", re.I | re.M),
     "Co-Authored-By trailer naming Claude"),
    ("8b", re.compile(r"^\s*claude-session:|claude\.ai/code/session", re.I | re.M),
     "Claude session reference"),
    ("8c", re.compile(r"^\s*signed-off-by:.*(claude|anthropic)", re.I | re.M),
     "Signed-off-by naming Claude or Anthropic"),
    ("8e", re.compile(r"generated with \[?claude code|🤖 generated with", re.I),
     "Claude Code generation notice"),
)

IDENTITY = re.compile(r"claude|anthropic", re.I)

MARKER_LINE = "# project-standard: local-only"


def opted_in(ctx):
    """The local-only rule binds only repos that joined.

    Blocking logs/ everywhere would stop a legitimate commit in employer work,
    and a guard that does that gets disabled wholesale — taking the attribution
    rule with it.
    """
    repo = Path(ctx.repo)
    if (repo / "scripts" / "project-standard").is_dir():
        return True
    gi = repo / ".gitignore"
    if gi.is_file() and MARKER_LINE in gi.read_text(errors="ignore"):
        return True
    return False


def check(ctx):
    out = []
    out += _tracked_local_only(ctx)
    out += _gitignore(ctx)
    out += _attribution(ctx)
    out += _hooks(ctx)
    return out


def _tracked_local_only(ctx):
    out = []
    local_only = defaults.local_only_paths(ctx.contract)
    for rel in ctx.tracked:
        if any(rel.startswith(keep) for keep in defaults.ALWAYS_TRACKED):
            continue
        for path in local_only:
            bare = path.rstrip("/")
            if rel == bare or rel.startswith(path):
                out.append(F.error(
                    "7", f"local-only path is tracked — un-track it "
                         f"(history is not rewritten)", path=rel))
                break
        else:
            name = Path(rel).name
            if any(fnmatch(name.upper(), pat.upper())
                   for pat in LOCAL_ONLY_PATTERNS):
                out.append(F.warn(
                    "7", "looks like a local-only artifact but matches no exact "
                         "path — move it under docs/exec-summaries/ or confirm "
                         "it belongs in git", path=rel))
    return out


def _gitignore(ctx):
    out = []
    if not opted_in(ctx):
        return out
    gi = Path(ctx.repo) / ".gitignore"
    text = gi.read_text(errors="ignore") if gi.is_file() else ""
    local_only = defaults.local_only_paths(ctx.contract)
    missing = [p for p in local_only if p.rstrip("/") not in text]
    if missing:
        out.append(F.error(
            "9", f"gitignore is missing {len(missing)} of {len(local_only)} "
                 f"local-only entries: " + ", ".join(missing[:4])
                 + (" …" if len(missing) > 4 else ""), path=".gitignore"))
    return out


def _attribution(ctx):
    out = []
    if defaults.attribution_policy(ctx.contract) == "allow":
        return out  # the repo has declared it wants the attribution
    adopted = ctx.contract.adopted
    adopted_ok = bool(adopted) and ctx.git.commit_exists(adopted)

    after = ctx.git.commits(since=adopted) if adopted_ok else []
    before = ctx.git.commits() if not adopted_ok else \
        [c for c in ctx.git.commits() if c not in after]

    for check_id, pattern, label in ATTRIBUTION:
        hits = [c for c in after if pattern.search(c["body"] or "")]
        if hits:
            out.append(F.error(
                check_id, f"{len(hits)} commit(s) after the adoption baseline "
                          f"carry a {label} — newest {hits[0]['hash'][:8]}"))
        old = [c for c in before if pattern.search(c["body"] or "")]
        if old:
            out.append(F.warn(
                "14", f"{len(old)} commit(s) before the baseline carry a "
                      f"{label}; history is not rewritten for tidiness"))

    bad_ident = [c for c in after
                 if IDENTITY.search(c["author"] + c["author_email"]
                                    + c["committer"] + c["committer_email"])]
    if bad_ident:
        out.append(F.error(
            "8d", f"{len(bad_ident)} commit(s) after the baseline are authored "
                  f"or committed as Claude — newest {bad_ident[0]['hash'][:8]}"))

    if not adopted_ok:
        out.append(F.warn(
            "14", "no usable `adopted` baseline, so every attribution marker in "
                  "history is reported as pre-existing rather than as a breach"))
    return out


def _hooks(ctx):
    """Checks 11 / 11b — the guards are reachable.

    A hook vendored into a repo's own .git/hooks never fires when
    core.hooksPath is set, and it is set globally here. The check asks whether
    the resolved directory actually holds both guards.
    """
    out = []
    resolved = ctx.git.config("core.hooksPath")
    local = ctx.git.config("core.hooksPath", local_only=True)

    if not resolved:
        out.append(F.error(
            "11", "core.hooksPath is unset, so the git-hygiene guards are not "
                  "installed anywhere"))
        return out

    hooks_dir = Path(resolved).expanduser()
    if not hooks_dir.is_absolute():
        hooks_dir = Path(ctx.repo) / hooks_dir

    missing = [n for n in ("pre-commit", "commit-msg")
               if not (hooks_dir / n).is_file()]
    if missing:
        finding = F.error(
            "11b" if local else "11",
            f"core.hooksPath resolves to `{hooks_dir}`, which is missing "
            + ", ".join(missing)
            + (" — a local override pointing at a directory without the guards "
               "silently disables every hook" if local else ""))
        out.append(finding)
    return out
