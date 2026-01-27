#!/usr/bin/env python3
"""
Build Mode Manager for Finance Plugins

Usage:
    python scripts/build_mode.py debug    - Switch to debug mode (add [DEBUG] labels)
    python scripts/build_mode.py release  - Switch to release mode (remove [DEBUG] labels)
    python scripts/build_mode.py status   - Show current build mode for all plugins
    python scripts/build_mode.py package  - Package all plugins
    python scripts/build_mode.py package --release  - Switch to release and package
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Plugin directories
PLUGINS = [
    "mercury_tools_plugin",
    "mercury_trigger_plugin",
    "quickbooks_plugin",
    "quickbooks_payments_plugin",
]

DEBUG_SUFFIX = " [DEBUG]"

# Regex pattern to match label lines in YAML
# Matches lines like: "  en_US: Some Label" or "  en_US: Some Label [DEBUG]"
LABEL_PATTERN = re.compile(
    r"^(\s+)(en_US|zh_Hans|ja_JP|fr_FR|es_ES|pt_BR|ko_KR):\s*(.+?)(\s*\[DEBUG\])?\s*$"
)


def process_file(file_path: Path, mode: str) -> tuple[bool, str]:
    """
    Process a YAML file to add/remove [DEBUG] suffix from labels.
    Uses regex replacement to preserve original formatting.

    Returns (changed, message) tuple.
    """
    if not file_path.exists():
        return False, "file not found"

    with open(file_path, encoding="utf-8") as f:
        original_content = f.read()

    lines = original_content.split("\n")
    new_lines = []
    changed = False
    in_label_block = False

    for line in lines:
        # Detect if we're entering a label block
        stripped = line.strip()
        if stripped.startswith("label:"):
            in_label_block = True
            new_lines.append(line)
            continue

        # Detect if we're exiting a label block (non-indented line after label:)
        if in_label_block and stripped and not line.startswith(" ") and not line.startswith("\t"):
            in_label_block = False

        # Process label lines
        if in_label_block:
            match = LABEL_PATTERN.match(line)
            if match:
                indent = match.group(1)
                lang = match.group(2)
                label_text = match.group(3).strip()
                has_debug = match.group(4) is not None

                # Remove existing [DEBUG] from label text if present
                if label_text.endswith("[DEBUG]"):
                    label_text = label_text[:-7].strip()

                if mode == "debug" and not has_debug:
                    # Add [DEBUG]
                    new_line = f"{indent}{lang}: {label_text} [DEBUG]"
                    if new_line != line:
                        changed = True
                    new_lines.append(new_line)
                elif mode == "release" and has_debug:
                    # Remove [DEBUG]
                    new_line = f"{indent}{lang}: {label_text}"
                    if new_line != line:
                        changed = True
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
                continue

        new_lines.append(line)

    if changed:
        new_content = "\n".join(new_lines)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True, "labels updated"

    return False, "no changes needed"


def get_provider_yaml_path(plugin_dir: Path) -> Path | None:
    """Find the provider YAML file for a plugin."""
    provider_dir = plugin_dir / "provider"
    if not provider_dir.exists():
        return None

    for yaml_file in provider_dir.glob("*.yaml"):
        content = yaml_file.read_text()
        # Check if it's a provider file (has identity section with label)
        if "identity:" in content and "label:" in content:
            return yaml_file

    return None


def check_plugin_mode(plugin_name: str) -> str:
    """Check if a plugin is in debug or release mode."""
    plugin_dir = PROJECT_ROOT / plugin_name
    manifest_path = plugin_dir / "manifest.yaml"

    if not manifest_path.exists():
        return "unknown"

    content = manifest_path.read_text()

    # Look for en_US label with [DEBUG]
    for line in content.split("\n"):
        if "en_US:" in line and "[DEBUG]" in line:
            return "debug"

    return "release"


def set_plugin_mode(plugin_name: str, mode: str) -> tuple[bool, list[str]]:
    """
    Set plugin mode (debug or release).
    Returns (changed, messages) tuple.
    """
    plugin_dir = PROJECT_ROOT / plugin_name
    manifest_path = plugin_dir / "manifest.yaml"
    messages = []
    any_changed = False

    # Process manifest.yaml
    changed, msg = process_file(manifest_path, mode)
    messages.append(f"  manifest.yaml: {msg}")
    if changed:
        any_changed = True

    # Process provider/*.yaml
    provider_path = get_provider_yaml_path(plugin_dir)
    if provider_path:
        changed, msg = process_file(provider_path, mode)
        rel_path = provider_path.relative_to(plugin_dir)
        messages.append(f"  {rel_path}: {msg}")
        if changed:
            any_changed = True

    return any_changed, messages


def cmd_status() -> None:
    """Show current build mode for all plugins."""
    print("Plugin Build Mode Status:")
    print("-" * 50)

    for plugin in PLUGINS:
        mode = check_plugin_mode(plugin)
        mode_display = "[DEBUG]" if mode == "debug" else "RELEASE"
        color = "\033[33m" if mode == "debug" else "\033[32m"
        reset = "\033[0m"
        print(f"  {plugin:<35} {color}{mode_display}{reset}")

    print("-" * 50)


def cmd_set_mode(mode: str) -> None:
    """Set mode for all plugins."""
    mode_display = "DEBUG" if mode == "debug" else "RELEASE"
    print(f"Switching all plugins to {mode_display} mode...")
    print("-" * 50)

    total_changed = 0
    for plugin in PLUGINS:
        print(f"\n{plugin}:")
        changed, messages = set_plugin_mode(plugin, mode)
        for msg in messages:
            print(msg)
        if changed:
            total_changed += 1

    print("-" * 50)
    if total_changed > 0:
        print(f"Updated {total_changed} plugin(s) to {mode_display} mode")
    else:
        print(f"All plugins already in {mode_display} mode")


def cmd_package(release_mode: bool = False) -> None:
    """Package all plugins."""
    if release_mode:
        print("Switching to RELEASE mode before packaging...")
        cmd_set_mode("release")
        print()

    print("Packaging all plugins...")
    print("-" * 50)

    for plugin in PLUGINS:
        plugin_dir = PROJECT_ROOT / plugin
        if not plugin_dir.exists():
            print(f"  {plugin}: directory not found, skipping")
            continue

        print(f"  Packaging {plugin}...", end=" ", flush=True)
        try:
            result = subprocess.run(
                ["dify", "plugin", "package", str(plugin_dir)],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
            print("OK")
        except subprocess.CalledProcessError as e:
            print(f"FAILED")
            print(f"    Error: {e.stderr.strip()}")
        except FileNotFoundError:
            print("FAILED")
            print("    Error: 'dify' command not found")
            print("    Install with: pip install dify-plugin-daemon")
            return

    print("-" * 50)
    print("Packaging complete. Check the project root for .difypkg files.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build mode manager for Finance Plugins",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/build_mode.py status             # Check current mode
  python scripts/build_mode.py debug              # Switch to debug mode
  python scripts/build_mode.py release            # Switch to release mode
  python scripts/build_mode.py package            # Package all plugins
  python scripts/build_mode.py package --release  # Release and package
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # status command
    subparsers.add_parser("status", help="Show current build mode")

    # debug command
    subparsers.add_parser("debug", help="Switch to debug mode (add [DEBUG] labels)")

    # release command
    subparsers.add_parser(
        "release", help="Switch to release mode (remove [DEBUG] labels)"
    )

    # package command
    package_parser = subparsers.add_parser("package", help="Package all plugins")
    package_parser.add_argument(
        "--release",
        action="store_true",
        help="Switch to release mode before packaging",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "status":
        cmd_status()
    elif args.command == "debug":
        cmd_set_mode("debug")
    elif args.command == "release":
        cmd_set_mode("release")
    elif args.command == "package":
        cmd_package(release_mode=args.release)


if __name__ == "__main__":
    main()
