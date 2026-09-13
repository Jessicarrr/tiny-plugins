# Tiny Plugins

Tiny Plugins is a small, repo-local marketplace for Codex plugins. The marketplace definition is
in `.agents/plugins/marketplace.json`, and plugin source lives under `plugins/`. The repository
currently contains the `workflow` plugin, which provides reusable planning, review, refactoring,
clarification, and ticket-writing skills. `README.md` documents marketplace registration and
installation. `bust_cache.py` bumps a plugin's SemVer version and reinstalls it from the
configured marketplace. Tests for that helper are in `test_bust_cache.py`.

## Instructions

After making any change, run the cache-busting script for the changed plugin yourself.
`workflow` below is the plugin name; replace it with the relevant plugin's name:

```powershell
python bust_cache.py <plugin-name> <patch|minor|major>
```

For example, for this repository's `workflow` plugin:

```powershell
python bust_cache.py workflow patch
```

Use `patch` for bug fixes, `minor` for backward-compatible features, and `major` for breaking
changes or major overhauls. The bump argument is required so every version change is explicit.

Start a new Codex thread after reinstalling so the updated plugin is loaded.
