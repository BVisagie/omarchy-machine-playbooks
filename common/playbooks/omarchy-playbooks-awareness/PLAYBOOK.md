---
id: omarchy-playbooks-awareness
scope: common
host: all
depends_on: none
agnostic: true
status: applied
last_verified: 2026-09-15
needs_reboot: false
---

# Omarchy playbooks awareness

Makes agents on this box look up **this** playbooks repo and ask to save system fixes there.

Does **not** edit `/usr/share/omarchy/` or bundled skills. Those are overwritten on update.

## Symptoms

- After a format, models re-solve already-known host issues
- A system workaround lives only in chat

## Root cause

The packaged Omarchy skill has no pointer at a private playbooks repo. Stock `~/.agents/skills/omarchy` is a symlink into `/usr/share/omarchy`. Awareness has to live in a **user** skill and a `post-update` hook.

## Apply

Run `apply.sh` from this folder.

It:

1. Installs `~/.agents/skills/machine-playbooks/SKILL.md`
2. Copies the fragment next to that skill
3. If `~/.agents/skills/omarchy` is a **writable real directory** (not the stock symlink), appends a pointer there
4. Installs a `post-update` hook so `omarchy update` re-applies this playbook

## Verify

```bash
test -f ~/.agents/skills/machine-playbooks/SKILL.md
test -f ~/.config/omarchy/hooks/post-update.d/50-machine-playbooks-awareness
```

## Rollback

Delete `~/.agents/skills/machine-playbooks/` and `~/.config/omarchy/hooks/post-update.d/50-machine-playbooks-awareness`.

## What not to change

Do not patch `/usr/share/omarchy/` or `~/.grok/bundled/skills/omarchy/`.
