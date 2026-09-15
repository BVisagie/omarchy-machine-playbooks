# Omarchy on these machines

Read the packaged Omarchy skill (`~/.agents/skills/omarchy/SKILL.md`) for live commands. On stock Omarchy that path is a **symlink** into `/usr/share/omarchy` — never write through it.

Hard rules:

- Never edit `/usr/share/omarchy/` or `~/.grok/bundled/skills/`. Package updates overwrite both.
- User config: `~/.config/hypr/`, `~/.config/omarchy/`.
- `omarchy hook install <type> <script>` for hooks.
- Privileged: `sudo` in a terminal, `pkexec` from an agent.
- `omarchy debug` always with `--no-sudo --print`.

Awareness lives in `~/.agents/skills/machine-playbooks/`. After any system fix, follow AGENTS.md: ask scope, plugin-agnostic vs tied, and whether to push to this repo.
