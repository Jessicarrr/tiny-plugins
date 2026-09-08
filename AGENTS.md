# Tiny Plugins

Tiny Plugins is a small, repo-local marketplace for Codex plugins. The marketplace definition is
in `.agents/plugins/marketplace.json`, and plugin source lives under `plugins/`. The repository
currently contains the `workflow` plugin, which provides reusable planning, review, refactoring,
clarification, and ticket-writing skills. `README.md` documents marketplace registration and
installation. `bust_cache.py` updates a plugin version with a UTC cachebuster and reinstalls it
from the configured marketplace. Tests for that helper are in `test_bust_cache.py`.

## Instructions

After making any change, run the cache-busting script for the changed plugin yourself.
`workflow` below is the plugin name; replace it with the relevant plugin's name:

```powershell
python bust_cache.py <plugin-name>
```

For example, for this repository's `workflow` plugin:

```powershell
python bust_cache.py workflow
```

The script automatically adds a UTC timestamp cachebuster. Use `--cachebuster` when a
repeatable token is useful:

```powershell
python bust_cache.py workflow --cachebuster local-test
```

`local-test` is only an example label. It becomes part of the plugin version, such as
`0.1.0+codex.local-test`, so Codex sees a changed version during local development.

Start a new Codex thread after reinstalling so the updated plugin is loaded.
