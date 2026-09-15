# Writing a playbook

One folder per problem under `common/playbooks/` or
`machines/<hostname>/playbooks/`. Required: `PLAYBOOK.md`.
Optional: `apply.sh`, read-only `check.sh`, `rollback.sh`, and `files/`.

## Front matter

```yaml
id: short-kebab-id
scope: machine
host: my-hostname
depends_on: none
agnostic: true
status: draft
last_verified: null
needs_reboot: false
```

Use `scope: common` with `host: all`. Dependencies may be `none`,
`plugin:<id>`, or `app:<name>`. Describe a supported agnostic path when a
dependency is absent, or explicitly state that no fallback exists.

Statuses describe recipe maturity, never current machine state:

- `draft`: not yet proven on its intended hardware.
- `verified`: supported by recorded successful checks.
- `example`: teaching material outside the restore inventory.
- `retired`: retained for history; do not automatically apply.

`last_verified` is the date of actual verification, or null. Updating scripts
does not reset it. Explain which version was tested and which changes remain
unverified on hardware.

## Body

Include Symptoms, Root cause, Apply, Verify, Rollback, and What not to change.
A working workaround does not establish its mechanism: distinguish a confirmed
cause from a hypothesis. Link supporting upstream issues or primary documentation.

Under Tested environment and evidence, record Omarchy, kernel, compositor,
relevant plugin versions, hardware, commands/results, and any unknowns.
Document cold boot, suspend/resume, and physical symptoms separately from
file installation and mocked tests. Record power/performance tradeoffs where relevant.

## Script behavior

Check target hardware and dependencies before mutations. Avoid broad device
globs and full config replacements. Preserve original content, retain that
backup on repeat application, and refuse rollback over later edits. Use
argument arrays for privilege escalation, not interpolated shell code.

`check.sh` must not change files, devices, profiles, or caches. Explain exit
codes and pending reboot. An installer must report incomplete steps honestly.
Keep examples no-ops. See [the example](../examples/example-desktop/playbooks/example-high-hz-black-frames/PLAYBOOK.md).

After a successful fix, follow AGENTS.md to record it locally or publish it
within the user's existing authorization.
