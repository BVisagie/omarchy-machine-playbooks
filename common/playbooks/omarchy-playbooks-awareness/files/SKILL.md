---
name: machine-playbooks
description: >
  Restore and record Omarchy machine-specific and all-machine system fixes
  from a machine-playbooks repo (this template or a private copy). Use when
  customizing Hyprland, ~/.config/omarchy/, displays, GPU, kernel cmdline,
  udev, after a format, restoring a machine, or when a system workaround
  just landed. Triggers: restore this machine, format, playbooks, system
  fix, push to common, /machine-playbooks.
---

# Machine playbooks

Before solving a desktop/GPU/display/Omarchy config problem from scratch, open the playbooks repo and match a kit.

## Find the repo

1. `$MACHINE_PLAYBOOKS`
2. `~/Work/machine-playbooks`
3. `~/machine-playbooks`
4. `~/Work/omarchy-machine-playbooks`

If it is missing, ask where the user’s copy of this template lives. Then read `AGENTS.md` there and follow it. Do not invent a second process.

## Order

1. Identify host (`hostnamectl`, GPU, monitor).
2. Read `common/INDEX.md`, then `machines/<hostname>/`. Skip `example-desktop` unless that is the real hostname.
3. Ask the apply/save questions in `AGENTS.md`. Always ask **“Shall we push this to the playbooks repo?”** after a new system fix (`common/` vs this machine).
4. Apply matching playbooks; do not re-research a solved issue.

Never edit `/usr/share/omarchy/` or `~/.grok/bundled/skills/`.
