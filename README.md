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
python bust_cache.py workflow
```

This script updates the plugin version and reinstalls it. Codex needs this step to load the new version.
Claude and other tools may not need it.

Use `--cachebuster <token>` for a repeatable version, or `--no-install` to update the manifest only.

## Plugins

### `workflow`

Skills for planning, clarification, implementation, review, refactoring, and ticket writing.
