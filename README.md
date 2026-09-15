# Omarchy machine playbooks

Small restore kits for [Omarchy](https://omarchy.org/), written for humans and
coding agents. Keep your configuration deltas together with their symptoms,
reasoning, verification, and rollback so the next restore starts from evidence.

## First day

Use this GitHub template to create your own repository. A private repository is
recommended for personal machine information. Then:

```bash
git clone git@github.com:<you>/<your-playbooks>.git ~/Work/machine-playbooks
cd ~/Work/machine-playbooks
./common/playbooks/omarchy-playbooks-awareness/apply.sh
./common/playbooks/omarchy-playbooks-awareness/check.sh
```

Requires Bash and Python 3. Install as your normal user, without sudo. Custom
clone locations work: the installer records the absolute repository path.
Start a new agent session so it can discover the installed skill.

Copy `machines/_template/` to a directory named after your static hostname.
Fill the identity and hardware in `MACHINE.md`; add real playbooks as fixes
are proven. Then ask an agent to restore this machine.

## Layout

| Path | Purpose |
|---|---|
| `common/` | Reusable kits; check applicability before applying |
| `machines/<hostname>/` | Machine-specific kits and hardware identity |
| `machines/_template/` | Starting point for a new host |
| `examples/` | Teaching material, never restore candidates |
| `tests/` | Isolated regression tests |
| `scripts/validate.py` | Repository structure and script validation |

Agents follow [AGENTS.md](AGENTS.md). See [writing a playbook](docs/writing-a-playbook.md)
and [maintaining a personal copy](docs/template-updates.md).

## Recovery and boundaries

Each installer documents its checks and rollback. Awareness preserves original
files in a local journal and refuses to overwrite later edits during rollback.
See its [playbook](common/playbooks/omarchy-playbooks-awareness/PLAYBOOK.md).

This repository stores small deltas, not full home directories or an Omarchy
fork. Do not commit secrets, tokens, full configuration dumps, local backup
journals, or files from `/usr/share/omarchy/`. Review changes before publishing.

## Development

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Install ShellCheck separately through your OS package manager; validation
requires it. Tests use temporary directories and mocked system interfaces.

## License

MIT. See [LICENSE](LICENSE).
