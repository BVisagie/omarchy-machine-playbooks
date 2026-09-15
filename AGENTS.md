# Agent instructions

This repository stores **Omarchy restore kits**: per-machine and all-machine deltas, plus the reasoning needed to re-apply them after a format.

Omarchy is the OS. Do not dump whole home directories here. Canonical file for models. `CLAUDE.md` and `.github/copilot-instructions.md` point here — do not duplicate these rules there.

## Locate the repo

Try, in order:

1. Current workspace if it contains `machines/` and `common/`
2. `$MACHINE_PLAYBOOKS`
3. `~/Work/machine-playbooks`
4. `~/machine-playbooks`
5. `~/Work/omarchy-machine-playbooks`

If missing, ask where the user’s copy of this template lives. Do not assume a GitHub user or clone URL.

## Workflow

1. Identify the host: `hostnamectl`, GPU `lspci -nn | grep -E 'VGA|3D'`, monitor `hyprctl monitors` (or EDID under `/sys/class/drm/`).
2. Read `common/INDEX.md`, then `machines/<hostname>/MACHINE.md` and `INDEX.md`. If hostname misses, match motherboard / GPU PCI ID / monitor EDID in `MACHINE.md`. Ignore `example-desktop` unless the hostname really is that.
3. Use only playbooks whose symptoms match. Do not re-research a solved issue. Do not run `example-*` playbooks as if they were real fixes.
4. Ask the questions below before applying or saving. Do not skip them.
5. Prefer that playbook’s `apply.sh` when it exists. Otherwise follow `PLAYBOOK.md` exactly.
6. Verify with the playbook’s checks. Do not switch the user into a known-broken mode “to test” unless the playbook says to.
7. Never edit `/usr/share/omarchy/` or `~/.grok/bundled/skills/`. Stock `~/.agents/skills/omarchy` is a **symlink** into `/usr/share/omarchy` — do not write through it. User config stays in `~/.config/`. Privileged files: `sudo` in a terminal, `pkexec` from an agent.

## Questions — before applying a playbook

1. **Host** — “This looks like **&lt;title&gt;** (`<hostname>`). Apply here?”
2. **Scope** — if `scope: common`: “This is in the all-machines kit. Apply it on this box too?”
3. **App/plugin** — if `depends_on` is not `none`, confirm that plugin/app is installed. If it is missing, use the playbook’s **agnostic** path.
4. **Reboot / root** — say so before Limine, udev, or kernel cmdline.

## Questions — after a new system fix (save)

Always ask, even if the fix feels small:

1. **Scope** — “Is this **this machine only**, or **all machines** (`common/`)?”
2. **Agnostic vs tied** — “Is this independent of a specific app/plugin, or does it only work with one (theme, Screens, a bar widget, Steam, …)?” If tied, set `depends_on: plugin:<id>` or `app:<name>` and write a fallback.
3. **Push** — “Shall we write this into the playbooks repo and push?” Destination follows (1): `machines/<hostname>/playbooks/` vs `common/playbooks/`.
4. **New vs update** — new folder vs an existing playbook.

Do not file one-off experiments unless the user says yes. Do not leave a working fix only in chat.

## Playbook front matter

```yaml
id: short-kebab-id
scope: machine | common
host: example-desktop | all
depends_on: none | plugin:<id> | app:<name>
agnostic: true | false
status: applied | stub | example
last_verified: YYYY-MM-DD
needs_reboot: true | false
```

One folder per problem: `PLAYBOOK.md`, optional `apply.sh`, optional `files/`. See [docs/writing-a-playbook.md](docs/writing-a-playbook.md).

## Adding a machine

Copy `machines/_template/`, name the folder after `hostnamectl`’s Static hostname, fill `MACHINE.md` (title, match keys, hardware), add playbooks as they are proven. Delete or rename `machines/example-desktop/` so agents do not match the sample.
