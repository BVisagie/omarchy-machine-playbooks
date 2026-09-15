---
id: example-desktop
title: Example desktop (rename or delete)
hostname: example-desktop
match:
  motherboard: REPLACE-MOTHERBOARD
  gpu_pci: REPLACE-GPU-PCI
  gpu: REPLACE-GPU-NAME
  monitor: REPLACE-MONITOR
  monitor_desc: REPLACE-MONITOR-DESC
---

# Example desktop (rename or delete)

Sample host for the template. **Rename this folder** to `hostnamectl`’s Static hostname, or delete it and copy `machines/_template/`.

Agents must not treat this as a real machine unless the hostname is actually `example-desktop`.

## Hardware

- Board: `REPLACE-MOTHERBOARD`
- GPU: `REPLACE-GPU-NAME` (`REPLACE-GPU-PCI`)
- Display: `REPLACE-MONITOR`

## Notes

The playbook under `playbooks/` is a **teaching example**. It does not install GPU clocks or kernel parameters.
