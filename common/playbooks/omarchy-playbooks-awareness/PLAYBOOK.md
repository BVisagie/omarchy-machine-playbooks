---
id: omarchy-playbooks-awareness
scope: common
host: all
depends_on: none
agnostic: true
status: verified
last_verified: 2026-09-15
needs_reboot: false
---

# Omarchy playbooks awareness

## Symptoms

Agents rediscover recorded fixes or lose the selected repository after an update.

## Root cause

Discovery relied on conventional paths without recording the selected checkout.

## Apply

Run `./apply.sh` as your normal user with Python 3 installed. It installs a
standalone skill and post-update hook, and records the source repository in
`~/.config/machine-playbooks/repo-path`. It does not modify the Omarchy skill.

Resolution uses explicit `MACHINE_PLAYBOOKS`, then the saved path, then a unique
conventional checkout. Invalid explicit or saved paths fail clearly. If a
repository moves, run the installer from its new location. Installation itself
intentionally selects the source checkout; environment selection controls
discovery and the update hook.

Original bytes and permissions are stored in
`~/.local/state/machine-playbooks/awareness/files.json` (mode 0600).
Repeat installation retains the original backup. Later edits cause a conflict
requiring review. New files are written atomically; an interrupted run leaves
a journal for retry or rollback.

## Verify

Run `./check.sh` (0 verified, 1 incomplete/error). It checks the selected repo,
installed content and permissions, and journal without writing files.
Start a new agent session and confirm the machine-playbooks skill is discoverable;
file checks alone cannot prove a particular agent loaded it.

## Rollback

Run `./rollback.sh`. It restores original files and removes files newly created
by this installer. It checks all journal entries for later edits before restoring
any. Empty directories and the lock file remain. Keep the journal until recovery
is complete; it is local state, not repository content.

### Existing installations

On the first upgrade, existing awareness files become the rollback baseline.
Old installers did not save originals. They may also have left
`playbooks.md` in the user skill and a marked section between
`<!-- machine-playbooks:awareness -->` and
`<!-- /machine-playbooks:awareness -->` in a writable Omarchy skill.

Review those files, remove only that exact legacy block and an unmodified
legacy fragment if present, and preserve other content. Never follow a packaged
skill symlink. Do not delete whole skill directories as a migration shortcut.
Rolling back the upgrade restores the previous awareness files; it cannot
reconstruct content that the old installer overwrote without a backup.

## Tested environment and evidence

Historical installation verification: 2026-09-15. The revised installer is
covered by isolated repository tests for selection, repeat application, conflicts,
symlinks, and rollback. Hardware and agent discovery after an Omarchy update
require a separate manual check; no new live-system verification is claimed.

## What not to change

Do not patch packaged skills, install this user-level kit as root, or add
automatic Git fetch/pull/push behavior to the update hook.
