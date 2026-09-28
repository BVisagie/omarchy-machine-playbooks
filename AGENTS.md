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
   Complete the fresh restore preflight below for every candidate, including
   recipes marked `verified`, before running its installer or Apply steps.
3. Summarize applicable kits, affected files, privileges, and reboot needs.
   Respect authorization already given. Ask only for unresolved choices.
4. Use the playbook's installer or documented steps. Run `check.sh` when
   provided. Distinguish installed files from verified live state and pending
   reboot. Do not switch to a known-broken display mode merely to test.
5. Never modify `/usr/share/omarchy/` or `~/.grok/bundled/skills/`, including
   through symlinks. Keep user configuration in `~/.config/`.

## Fresh restore preflight

A past successful restore proves only that a recipe worked in its recorded
environment. Before each restore, compare the current machine and installed
Omarchy, kernel, compositor, packages, and relevant app/plugin versions with
the playbook's assumptions. Check whether the symptom still exists, whether
Omarchy or another upstream component now fixes it, and whether the proposed
changes would conflict with current defaults, APIs, packages, or user settings.
Use current upstream documentation, release notes, and issue status where
available; do not infer current safety from `last_verified` alone.

Before fetching, installing, or executing a third-party project, verify its
current source and package origin, maintainership, release or commit being
installed, and relevant security advisories or compromise reports. Check
published signatures or checksums when provided. A historical URL or pinned
version is a starting point, not proof that the project is still safe. If
current trust cannot be established, defer the affected external step. A
network failure is not a clean security result.

Decide and report for each candidate: apply it; skip it because it is already
fixed or unnecessary; or stop because it is incompatible, harmful, or cannot
be verified. If a recipe could break Omarchy or cause another issue, tell the
user the specific conflict and likely effect **before making changes**.
Offer a current safe alternative or a playbook revision when possible. Do not
run the affected installer merely because the user asked to restore the old
recipe. Keep read-only diagnosis and unaffected kits moving where safe.

## Recording a fix

Propose the correct machine or `common/` destination and whether this updates
an existing playbook. Record app/plugin dependencies and a supported fallback
(or explicitly explain why none exists). Ask only if these choices are unresolved.

Saving locally, committing, and publishing are separate actions. Follow the
user's authorized scope; do not repeatedly ask for permission already granted.
Do not publish experiments as verified fixes or leave an authorized record only in chat.

## GitHub Actions versions

When creating or updating workflows, verify each action's latest stable upstream
release and use that release. Do not select versions from memory or use prereleases.
Check compatibility and run CI after updating action versions.

## Playbook format

One problem per folder: `PLAYBOOK.md`, optional `apply.sh`, read-only
`check.sh`, `rollback.sh`, and `files/`.
See [the writing guide](docs/writing-a-playbook.md) for metadata, evidence, and
compatibility requirements. Recipe maturity is `draft`, `verified`,
`example`, or `retired`; local installation state comes from checks.

Copy `machines/_template/` for a new host, fill its actual static hostname and
match keys, and add proven kits. Teaching material lives in `examples/`.
