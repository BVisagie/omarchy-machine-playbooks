# files/

In a real playbook, put the exact artifacts here, for example:

- `amdgpu-lock-display-clocks` → `/usr/local/sbin/`
- `99-something.rules` → `/etc/udev/rules.d/`
- `something.conf` → `/etc/limine-entry-tool.d/`

This example ships **no** installable GPU or boot files. Copying a udev rule from someone else’s box is how you break a different GPU.
