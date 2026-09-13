# Tiny Plugins

Tiny Plugins is a local marketplace for Codex plugins. It provides small, reusable skills for
software development.

## Install

From the repository root, add the marketplace:

```powershell
codex plugin marketplace add .
```

Install the `workflow` plugin:

```powershell
codex plugin add workflow@tiny-plugins
```

Start a new Codex thread after installation.

## Update a plugin in Codex

If you're running ChatGPT Codex and you change a plugin, you need to run the cache-busting script:

```powershell
python bust_cache.py workflow patch
```

The final argument is required and chooses the version component to bump:

- `patch`: bug fixes and small backward-compatible changes (`0.1.0` -> `0.1.1`)
- `minor`: new backward-compatible features (`0.1.1` -> `0.2.0`)
- `major`: breaking changes or major overhauls (`0.2.0` -> `1.0.0`)

The script updates the plugin version and reinstalls it. Codex needs this step to load the new version.
Claude and other tools may not need it.

Use `--no-install` to update the manifest only.

## Plugins

### `workflow`

Skills for planning, clarification, implementation, review, refactoring, and ticket writing.
