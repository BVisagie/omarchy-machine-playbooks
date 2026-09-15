#!/bin/bash
# Idempotent install of user-level playbooks awareness.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
FILES="$HERE/files"
SKILL_DIR="${HOME}/.agents/skills/machine-playbooks"
OMARCHY_SKILL_DIR="${HOME}/.agents/skills/omarchy"
MARKER_BEGIN="<!-- machine-playbooks:awareness -->"
MARKER_END="<!-- /machine-playbooks:awareness -->"

mkdir -p "$SKILL_DIR"
install -m 0644 "$FILES/SKILL.md" "$SKILL_DIR/SKILL.md"
install -m 0644 "$FILES/omarchy-skill-fragment.md" "$SKILL_DIR/playbooks.md"

# Packaged Omarchy skill is a symlink to /usr/share/omarchy — never write there.
if [[ -d "$OMARCHY_SKILL_DIR" && ! -L "$OMARCHY_SKILL_DIR" && -w "$OMARCHY_SKILL_DIR" ]]; then
  install -m 0644 "$FILES/omarchy-skill-fragment.md" "$OMARCHY_SKILL_DIR/playbooks.md"
  USER_OMARCHY_SKILL="$OMARCHY_SKILL_DIR/SKILL.md"
  if [[ -f "$USER_OMARCHY_SKILL" && -w "$USER_OMARCHY_SKILL" ]] && ! grep -q 'machine-playbooks:awareness' "$USER_OMARCHY_SKILL"; then
    {
      printf '\n%s\n' "$MARKER_BEGIN"
      printf '%s\n' "## Machine playbooks"
      printf '\n%s\n' "If \`playbooks.md\` exists in this directory, read it before applying a system fix."
      printf '%s\n' "$MARKER_END"
    } >> "$USER_OMARCHY_SKILL"
  fi
fi

HOOK_SRC="$FILES/50-machine-playbooks-awareness"
HOOK_DIR="${HOME}/.config/omarchy/hooks/post-update.d"
mkdir -p "$HOOK_DIR"
if command -v omarchy >/dev/null 2>&1; then
  omarchy hook install post-update "$HOOK_SRC"
else
  install -m 0755 "$HOOK_SRC" "$HOOK_DIR/50-machine-playbooks-awareness"
fi

echo "machine-playbooks awareness installed"
