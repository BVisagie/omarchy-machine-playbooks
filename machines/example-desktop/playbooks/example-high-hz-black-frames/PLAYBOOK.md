---
id: example-high-hz-black-frames
scope: machine
host: example-desktop
depends_on: plugin:example.screens
agnostic: false
status: example
last_verified: 2026-09-15
needs_reboot: true
---

# Example: 4K high-refresh black frames

**Teaching example.** Do not run this as a real fix. `apply.sh` exits without changing the system unless `EXAMPLE_APPLY=1`.

A real kit of this kind belongs in *your* private fleet repo, with files that match **your** GPU and panel.

## Symptoms

- 4K at the panel’s max refresh (e.g. 240 Hz) over DisplayPort: full black frame every few seconds, then the image returns
- Lower refresh (e.g. 120 Hz) is stable
- Same cable and panel are fine on another OS or another GPU

## Root cause

(Fill in for a real playbook. Pattern: the link needs more bandwidth than the idle GPU clocks / colour depth / VRR path can hold — for example DP 1.4 + DSC on `amdgpu` while VRAM P-states drop. One paragraph, so the next agent does not re-investigate.)

## Apply

Real playbook: run `apply.sh`, which copies `files/` to the paths listed there (udev, Limine drop-in, helper script) and records Hyprland **deltas** (not a full `monitors.lua` dump).

This example: `apply.sh` only prints instructions.

`depends_on: plugin:example.screens` is the sample “a bar plugin owns monitors.lua” case. If that plugin is missing, use the agnostic path.

## Verify

```bash
# Real kit: show the clocks / connector / Hyprland flags you care about.
# Example:
#   cat /sys/class/drm/card1/device/pp_dpm_mclk
#   hyprctl monitors
```

## Rollback

List the files to remove and any `limine-update` / reboot.

## What not to change

- Do not disable a compression or link feature the mode actually requires
- Do not pin GPU **core** clocks if you only needed a **memory** floor
- Do not re-enable a compositor feature (e.g. VRR) that was part of the failure mode

## Agnostic path (no Screens-like plugin)

Edit `~/.config/hypr/monitors.lua` directly: set the flags the playbook needs (`vrr = 0`, bit depth, and so on). Do not force a refresh rate the user did not ask for.
