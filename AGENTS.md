# Agent instructions

This repository stores small Omarchy restore kits and the evidence needed to
reuse them. This is the canonical instruction file for all agents.

## Repository selection

When awareness is installed, run
`python3 ~/.agents/skills/machine-playbooks/awareness.py resolve`.
Resolution uses explicit `MACHINE_PLAYBOOKS`, then
`~/.config/machine-playbooks/repo-path`, then a unique conventional checkout
(`~/Work/machine-playbooks`, `~/machine-playbooks`, or
`~/Work/omarchy-machine-playbooks`). Invalid explicit or saved paths are errors.
Before installation, use the workspace the user selected, or ask where their copy lives.

## Restore workflow

1. Identify hardware with `hostnamectl`, `lspci -nn`, and `hyprctl monitors`
   or DRM/EDID. Read `common/INDEX.md` and the candidate machine's `MACHINE.md`
   and `INDEX.md`. A hostname alone is insufficient for hardware workarounds.
   Empty match keys are unknown, not wildcards; ambiguous matches need clarification.
2. Start with recorded solutions and check symptoms, hardware, dependencies,
   and tested versions. Do not apply examples, drafts, or retired recipes as
   proven fixes. `common/` means reusable, not automatically applicable.
3. Summarize applicable kits, affected files, privileges, and reboot needs.
   Respect authorization already given. Ask only for unresolved choices.
4. Use the playbook's installer or documented steps. Run `check.sh` when
   provided. Distinguish installed files from verified live state and pending
   reboot. Do not switch to a known-broken display mode merely to test.
5. Never modify `/usr/share/omarchy/` or `~/.grok/bundled/skills/`, including
   through symlinks. Keep user configuration in `~/.config/`.

## Recording a fix

Propose the correct machine or `common/` destination and whether this updates
an existing playbook. Record app/plugin dependencies and a supported fallback
(or explicitly explain why none exists). Ask only if these choices are unresolved.

Saving locally, committing, and publishing are separate actions. Follow the
user's authorized scope; do not repeatedly ask for permission already granted.
Do not publish experiments as verified fixes or leave an authorized record only in chat.

## Format

One problem per folder: `PLAYBOOK.md`, optional `apply.sh`, read-only
`check.sh`, `rollback.sh`, and `files/`.
See [the writing guide](docs/writing-a-playbook.md) for metadata, evidence, and
compatibility requirements. Recipe maturity is `draft`, `verified`,
`example`, or `retired`; local installation state comes from checks.

Copy `machines/_template/` for a new host, fill its actual static hostname and
match keys, and add proven kits. Teaching material lives in `examples/`.
