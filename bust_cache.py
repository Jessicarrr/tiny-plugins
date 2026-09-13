#!/usr/bin/env python3
"""Bump a local Codex plugin's version and reinstall it from this marketplace."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable


IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*$")
VERSION_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
BUMP_TYPES = ("patch", "minor", "major")


def find_codex() -> str:
    """Return the launchable Codex command, including Windows script extensions."""
    codex_path = shutil.which("codex")
    if codex_path is None:
        raise FileNotFoundError("Could not find 'codex' on PATH")
    return codex_path


def read_json(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as manifest_file:
            value = json.load(manifest_file)
    except FileNotFoundError as exc:
        raise ValueError(f"Could not find JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def marketplace_name(marketplace_path: Path) -> str:
    marketplace = read_json(marketplace_path)
    name = marketplace.get("name")
    if not isinstance(name, str) or not IDENTIFIER_RE.fullmatch(name):
        raise ValueError(
            f"Marketplace name must match {IDENTIFIER_RE.pattern}: {marketplace_path}"
        )
    return name


def bump_version(version: str, bump: str) -> str:
    """Return the next version after applying a SemVer major/minor/patch bump."""
    if bump not in BUMP_TYPES:
        valid_bumps = ", ".join(BUMP_TYPES)
        raise ValueError(f"Version bump must be one of: {valid_bumps}")

    match = VERSION_RE.fullmatch(version)
    if match is None:
        raise ValueError(f"Plugin version must be a valid SemVer version: {version}")

    major, minor, patch = (int(value) for value in match.groups()[:3])

    if bump == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1

    return f"{major}.{minor}.{patch}"


def update_manifest(manifest_path: Path, bump: str) -> tuple[str, str]:
    manifest = read_json(manifest_path)

    plugin_name = manifest.get("name")
    if not isinstance(plugin_name, str) or not IDENTIFIER_RE.fullmatch(plugin_name):
        raise ValueError(
            f"Plugin manifest name must match {IDENTIFIER_RE.pattern}: {manifest_path}"
        )

    version = manifest.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError(f"Plugin manifest does not contain a valid version: {manifest_path}")

    new_version = bump_version(version, bump)
    manifest["version"] = new_version

    with manifest_path.open("w", encoding="utf-8", newline="\n") as manifest_file:
        json.dump(manifest, manifest_file, indent=2, ensure_ascii=False)
        manifest_file.write("\n")

    return plugin_name, new_version


def refresh_plugin(
    plugin_name: str,
    repo_root: Path,
    marketplace_path: Path,
    bump: str,
    install: bool = True,
    run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> str:
    if not IDENTIFIER_RE.fullmatch(plugin_name):
        raise ValueError(f"Plugin name must match {IDENTIFIER_RE.pattern}: {plugin_name}")

    plugin_path = repo_root / "plugins" / plugin_name
    manifest_path = plugin_path / ".codex-plugin" / "plugin.json"
    if not manifest_path.is_file():
        raise ValueError(f"Could not find plugin manifest: {manifest_path}")

    manifest = read_json(manifest_path)
    actual_name = manifest.get("name")
    if not isinstance(actual_name, str) or not IDENTIFIER_RE.fullmatch(actual_name):
        raise ValueError(
            f"Plugin manifest name must match {IDENTIFIER_RE.pattern}: {manifest_path}"
        )
    if actual_name != plugin_name:
        raise ValueError(
            f"Plugin name mismatch: requested {plugin_name!r}, manifest contains {actual_name!r}"
        )

    selected_marketplace = marketplace_name(marketplace_path)
    actual_name, new_version = update_manifest(manifest_path, bump)
    print(f"Updated {actual_name} to version {new_version}")

    if install:
        codex_path = find_codex()
        result = run(
            [codex_path, "plugin", "add", f"{actual_name}@{selected_marketplace}"],
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(f"codex plugin add failed with exit code {result.returncode}")
        print("\nPlugin refreshed successfully.")
        print("Start a new Codex thread to pick up the changes.")

    return new_version


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bump a local Codex plugin version and reinstall the plugin."
    )
    parser.add_argument("plugin_name", help="Plugin name, for example: workflow")
    parser.add_argument(
        "bump",
        choices=BUMP_TYPES,
        help="Version component to bump: patch (bug fix), minor (new feature), or major (breaking change).",
    )
    parser.add_argument(
        "--marketplace-path",
        type=Path,
        help="Path to marketplace.json (default: .agents/plugins/marketplace.json)",
    )
    parser.add_argument(
        "--no-install",
        action="store_true",
        help="Update plugin.json without running codex plugin add (useful for testing).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    marketplace_path = args.marketplace_path or repo_root / ".agents" / "plugins" / "marketplace.json"

    try:
        refresh_plugin(
            args.plugin_name,
            repo_root,
            marketplace_path,
            bump=args.bump,
            install=not args.no_install,
        )
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
