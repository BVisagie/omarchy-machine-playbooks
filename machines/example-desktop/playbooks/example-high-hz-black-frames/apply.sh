#!/bin/bash
# Teaching example. Does not change the system unless EXAMPLE_APPLY=1.
set -euo pipefail

if [[ "${EXAMPLE_APPLY:-}" != "1" ]]; then
  cat <<'EOF'
example-high-hz-black-frames: this is a teaching playbook.

It does not install udev rules, kernel parameters, or GPU clocks.

Rename machines/example-desktop/ to this host's hostname, replace
PLAYBOOK.md / files/ with a real kit, and drop status: example.

To see this script's placeholder install path: EXAMPLE_APPLY=1 ./apply.sh
EOF
  exit 0
fi

echo "EXAMPLE_APPLY=1: still a no-op. Put real install steps here after you replace files/."
exit 0
