# Omarchy machine playbooks

A GitHub **template** for [Omarchy](https://omarchy.org/) boxes: small restore kits that humans and coding agents can re-apply after a format, instead of rediscovering the same display, GPU, or Hyprland workaround.

Omarchy stays the OS. This repo only stores **your deltas** (udev, Limine drop-ins, Hyprland snippets) and the **why**.

Use this template → create a repo (keep it **private** if it will hold host-specific quirks) → clone it onto the machine → tell an agent **restore this machine**.

## First day

```bash
# after "Use this template" on GitHub
git clone git@github.com:<you>/<your-playbooks>.git ~/Work/machine-playbooks
cd ~/Work/machine-playbooks
./common/playbooks/omarchy-playbooks-awareness/apply.sh
```

Then:

1. Rename `machines/example-desktop/` to this box’s static hostname (`hostnamectl`).
2. Fill `MACHINE.md` (motherboard, GPU PCI ID, monitor).
3. Replace the example playbook with a real one, or delete it.
4. After the next system fix, the agent should ask: this machine vs all machines, plugin-specific vs agnostic, **shall we push?**

Agents read [AGENTS.md](AGENTS.md). Copilot and Claude load the same file via short pointers. How to write a kit: [docs/writing-a-playbook.md](docs/writing-a-playbook.md).

## Layout

| Path | What |
|---|---|
| `common/` | All-machines solutions (start with awareness so agents know this repo exists) |
| `machines/<hostname>/` | Host-only kits. Folder name is `hostnamectl`’s Static hostname |
| `machines/_template/` | Copy this for a new box |
| `machines/example-desktop/` | **Sample only** — rename or delete |

Matching also uses motherboard, GPU PCI ID, and monitor EDID, so a renamed host can still hit the right kit.

## What this is not

- Not chezmoi / Ansible / a full dotfiles tree
- Not an Omarchy fork — never commit `/usr/share/omarchy/`
- Not a drop-in GPU fix. The example playbook teaches **shape**, and does not install clocks or kernel flags

## What not to commit

- Secrets, LUKS passphrases, tokens
- Full `~/.config` dumps (Hyprland: small deltas only)
- Anything under `/usr/share/omarchy/` (stock `~/.agents/skills/omarchy` is a symlink there)

## License

MIT. See [LICENSE](LICENSE).
