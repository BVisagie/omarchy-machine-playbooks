# Writing a playbook

One folder, one problem, under `common/playbooks/` or `machines/<hostname>/playbooks/`.

```
my-fix/
├── PLAYBOOK.md    # required — what, why, apply, verify, rollback
├── apply.sh       # optional — idempotent install
└── files/         # optional — the actual udev rule, script, snippet
```

## Front matter

```yaml
id: short-kebab-id
scope: machine          # or common
host: my-hostname       # or all
depends_on: none        # or plugin:im0001gt.screens or app:steam
agnostic: true          # false if it only works with that plugin/app
status: applied         # stub | example
last_verified: 2026-09-15
needs_reboot: false
```

If `depends_on` is not `none`, `PLAYBOOK.md` must include an **agnostic path** (what to do when that plugin is missing).

## Body

Keep it short enough that a model will follow it instead of re-investigating:

1. **Symptoms** — what the user sees
2. **Root cause** — one paragraph
3. **Apply** — `apply.sh` or exact steps
4. **Verify** — commands and expected output
5. **Rollback**
6. **What not to change**

See `machines/example-desktop/playbooks/example-high-hz-black-frames/` for a filled-in sample. That sample does **not** change the system unless `EXAMPLE_APPLY=1`.

## After it works

Ask (see AGENTS.md): this machine vs `common/`, plugin-tied vs agnostic, then **shall we push?**
