#!/usr/bin/env bash
# Symlink each skill directory in this repo into ~/.claude/skills/
# Re-running is safe: existing symlinks pointing at this repo are refreshed,
# real directories of the same name are reported and skipped.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="$HOME/.claude/skills"

mkdir -p "$TARGET_DIR"

linked=0
skipped=0

for skill_dir in "$REPO_DIR"/*/; do
  name=$(basename "$skill_dir")
  # Skip non-skill dirs (no SKILL.md inside)
  [[ -f "$skill_dir/SKILL.md" ]] || continue

  target="$TARGET_DIR/$name"

  if [[ -L "$target" ]]; then
    # Existing symlink — refresh
    rm "$target"
    ln -s "$skill_dir" "$target"
    echo "refreshed: $name"
    linked=$((linked + 1))
  elif [[ -e "$target" ]]; then
    echo "skipped: $name (real directory exists at $target — remove it manually if you want to switch to this version)"
    skipped=$((skipped + 1))
  else
    ln -s "$skill_dir" "$target"
    echo "linked: $name"
    linked=$((linked + 1))
  fi
done

echo
echo "$linked skill(s) linked into $TARGET_DIR"
[[ $skipped -gt 0 ]] && echo "$skipped skipped (collision with real dirs)"
echo
echo "Skills are now invokable in any Claude Code session. Run 'git pull' here to update."
