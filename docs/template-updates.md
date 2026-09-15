# Maintaining a personal copy

The public omarchy-machine-playbooks repository owns shared awareness tooling,
validation, tests, agent workflow, and documentation. Personal repositories own
their machine identities and proven hardware fixes.

Record the public source commit in `TEMPLATE_REVISION`. A GitHub template copy
does not automatically receive later changes.

To update, compare that commit with a reviewed upstream commit. Selectively
port shared changes, keeping personal README details and machine data. Bring
across supporting files and tests together; review metadata migrations and run
validation before committing the new source revision. Do not overwrite the
entire personal tree or publish private data upstream.

Shared code and workflow improvements belong in the public template first.
Machine-specific fixes remain private unless separately prepared for publication.
