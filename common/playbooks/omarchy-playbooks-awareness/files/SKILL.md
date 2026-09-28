---
name: machine-playbooks
description: Restore known Omarchy machine fixes and record newly proven system workarounds in the user's playbooks repository. Use for machine restoration or display, GPU, Hyprland, udev, and boot configuration work that may have a recorded solution.
---

# Machine playbooks

Locate the selected repository with:

```bash
python3 ~/.agents/skills/machine-playbooks/awareness.py resolve
```

Resolution uses explicit `MACHINE_PLAYBOOKS`, then the saved absolute path in
`~/.config/machine-playbooks/repo-path`, then a unique conventional checkout.
If an explicit or saved path is invalid, repair that selection; do not silently
switch repositories. Before awareness is installed, ask where the user's copy
lives if the active workspace is not that repository.

Read its `AGENTS.md`, `common/INDEX.md`, and the matching machine's documentation.
Start with the recorded solution, checking hardware, dependencies, and version
assumptions. Examples and retired recipes are not restore candidates.

Before applying **any** playbook, including one marked verified or named by the
user, follow `AGENTS.md`'s fresh restore preflight. Check whether current
Omarchy/upstream behavior makes the fix obsolete or incompatible, and whether
its changes could break the current system. Recheck the provenance and current
trust of external projects before installing or running them. If a kit could
cause harm, explain the concrete conflict to the user and stop that kit. If
the source cannot be verified, defer the affected external step. Report why a
kit is applied, skipped, or stopped; do not blindly replay old instructions.

Use existing user authorization; clarify only unresolved choices. After a proven
new fix, propose a machine-specific or common record. Saving locally and pushing
to GitHub are separate actions; follow the scope the user authorized.

Never write through packaged skill symlinks or modify `/usr/share/omarchy/` or
`~/.grok/bundled/skills/`.
