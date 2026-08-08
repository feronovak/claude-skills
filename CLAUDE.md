# claude-skills

A collection of Claude Code skills, each a self-contained directory holding a
`SKILL.md` plus whatever references, templates or tooling that skill needs.
Skills are symlinked into `~/.claude/skills/` rather than copied, so the working
copy and the installed one are the same file.

## Running it

There is no build. Each skill is markdown plus, in some cases, a stdlib-only
Python tool with its own suite:

```bash
# install every skill in this repo into ~/.claude/skills
bash setup.sh

# the one skill that ships code
cd project-standard/tool
PYTHONPATH=.:tests python3 -m unittest discover -s tests -t .
```

## Conventions

- One directory per skill; the directory name is the skill name.
- `SKILL.md` carries YAML frontmatter with `name` and a `description` written to
  trigger on what a user would actually say.
- Long reference material goes in `references/`, not in `SKILL.md` — the skill
  body is loaded every time it triggers, the references only when read.
- Skills that ship code keep it under `<skill>/tool/` with tests beside it, and
  take no third-party dependencies.
- Design documents and implementation plans live under `docs/superpowers/`.

## Git hygiene

No AI assistant is recorded as a contributor: no `Co-Authored-By` trailer, no
session reference, no generation notice in a pull request body, and no commit
authored under an assistant identity. This overrides the default behaviour of
the tooling, which appends several of those unless told otherwise.

Install the guards that enforce it:

```bash
./project-standard/bin/project-standard install-hooks --global
```

Local-only paths stay untracked; see `.gitignore`.

## Where things are

Every document in this repository is indexed in
[`docs/DOCMAP.md`](docs/DOCMAP.md). Start there.

## project-standard

```yaml
adopted: f97c337c280e83f3c5c323b177d63dfbfc068806
profile: docs
  reason: a collection of skills, not a shipped application
critical-paths:
```
