# Machine playbooks (user overlay)

This file sits next to the user `machine-playbooks` skill. Packaged Omarchy is not patched (`~/.agents/skills/omarchy` is usually a symlink into `/usr/share/omarchy`).

After **any** system-level solution (Hyprland, display, GPU, udev, kernel cmdline, Omarchy config):

1. Open the playbooks repo (`$MACHINE_PLAYBOOKS`, `~/Work/machine-playbooks`, or `~/machine-playbooks`).
2. Follow `AGENTS.md`.
3. Ask whether the fix is **this machine only** or **all machines** (`common/`).
4. Ask whether it depends on a specific app/plugin or is agnostic.
5. Ask: **Shall we push this to the playbooks repo?**
