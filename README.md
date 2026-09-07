# Tiny Plugins

A small, repo-local marketplace for Codex plugins. Clone the repository, register the marketplace, and install only the plugins you want.

## Installation

From the repository root:

```powershell
codex plugin marketplace add .
```

Check that the marketplace is registered:

```powershell
codex plugin marketplace list
```

Install a specific plugin:

```powershell
codex plugin add workflow@tiny-plugins
```

Registering the marketplace does not install every plugin. Install each plugin individually as needed. Start a new Codex thread after installing a plugin so its skills are available.

## Plugins

### `workflow`

For implementation, code review, planning, and related software-development workflows. It currently includes a small `hello` skill for verifying that the plugin is installed correctly.

## Repository layout

```text
.
├── .agents/plugins/marketplace.json
└── plugins/
    └── workflow/
```
