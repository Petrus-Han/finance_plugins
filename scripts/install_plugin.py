#!/usr/bin/env python3
"""
Install Dify plugins via API.

Usage:
    uv run python scripts/install_plugin.py dist/*.difypkg
    uv run python scripts/install_plugin.py dist/quickbooks_plugin.difypkg
"""

import base64
import json
import sys
from pathlib import Path

import httpx

CREDENTIAL_FILE = ".credential"


def load_credentials() -> dict:
    """Load credentials from .credential file."""
    cred_path = Path(__file__).resolve().parent.parent / CREDENTIAL_FILE
    if not cred_path.exists():
        raise Exception(f"Credential file not found: {cred_path}")

    with open(cred_path) as f:
        return json.load(f)


def login(host: str, email: str, password: str) -> tuple[dict, str]:
    """Login to Dify and get cookies."""
    url = f"{host.rstrip('/')}/console/api/login"
    encoded_password = base64.b64encode(password.encode()).decode()

    response = httpx.post(
        url,
        json={"email": email, "password": encoded_password, "remember_me": True},
        timeout=30,
    )

    if response.status_code != 200:
        raise Exception(f"Login failed: {response.status_code} - {response.text}")

    cookies = dict(response.cookies)
    csrf_token = cookies.get("csrf_token") or cookies.get("__Host-csrf_token")

    if not csrf_token:
        raise Exception(f"No csrf_token in cookies. Cookies: {list(cookies.keys())}")

    return cookies, csrf_token


def upload_plugin(host: str, cookies: dict, csrf_token: str, pkg_path: Path) -> dict:
    """Upload plugin package to Dify."""
    url = f"{host.rstrip('/')}/console/api/workspaces/current/plugin/upload/pkg"

    with open(pkg_path, "rb") as f:
        files = {"pkg": (pkg_path.name, f, "application/octet-stream")}
        response = httpx.post(
            url,
            cookies=cookies,
            headers={"X-CSRF-Token": csrf_token},
            files=files,
            timeout=60,
        )

    if response.status_code != 200:
        raise Exception(f"Upload failed: {response.status_code} - {response.text}")

    return response.json()


def list_installed_plugins(host: str, cookies: dict, csrf_token: str, plugin_ids: list[str]) -> dict:
    """Check which plugins are already installed."""
    url = f"{host.rstrip('/')}/console/api/workspaces/current/plugin/list/installations/ids"

    response = httpx.post(
        url,
        cookies=cookies,
        headers={"X-CSRF-Token": csrf_token, "Content-Type": "application/json"},
        json={"plugin_ids": plugin_ids},
        timeout=30,
    )

    if response.status_code != 200:
        raise Exception(f"List installations failed: {response.status_code} - {response.text}")

    return response.json()


def uninstall_plugin(host: str, cookies: dict, csrf_token: str, installation_id: str) -> dict:
    """Uninstall an installed plugin."""
    url = f"{host.rstrip('/')}/console/api/workspaces/current/plugin/uninstall"

    response = httpx.post(
        url,
        cookies=cookies,
        headers={"X-CSRF-Token": csrf_token, "Content-Type": "application/json"},
        json={"plugin_installation_id": installation_id},
        timeout=60,
    )

    if response.status_code != 200:
        raise Exception(f"Uninstall failed: {response.status_code} - {response.text}")

    return response.json()


def install_plugin(host: str, cookies: dict, csrf_token: str, plugin_unique_identifier: str) -> dict:
    """Install uploaded plugin."""
    url = f"{host.rstrip('/')}/console/api/workspaces/current/plugin/install/pkg"

    response = httpx.post(
        url,
        cookies=cookies,
        headers={"X-CSRF-Token": csrf_token, "Content-Type": "application/json"},
        json={"plugin_unique_identifiers": [plugin_unique_identifier]},
        timeout=60,
    )

    if response.status_code != 200:
        raise Exception(f"Install failed: {response.status_code} - {response.text}")

    return response.json()


def extract_plugin_name(unique_identifier: str) -> str:
    """Extract plugin name from unique identifier."""
    return unique_identifier.split(":")[0]


def install_single_plugin(host: str, cookies: dict, csrf_token: str, pkg_path: Path) -> bool:
    """Upload, uninstall old version, and install a single plugin. Returns True on success."""
    print(f"\n{'='*50}")
    print(f"  {pkg_path.name}")
    print(f"{'='*50}")

    # Upload
    print(f"  Uploading...")
    upload_result = upload_plugin(host, cookies, csrf_token, pkg_path)
    plugin_id = upload_result.get("unique_identifier") or upload_result.get("plugin_unique_identifier")

    if not plugin_id:
        print(f"  Upload response: {json.dumps(upload_result, indent=2)}")
        raise Exception("No unique_identifier in upload response")

    print(f"  Uploaded: {plugin_id}")

    # Check if already installed
    plugin_name = extract_plugin_name(plugin_id)
    installations = list_installed_plugins(host, cookies, csrf_token, [plugin_name])
    installed_list = (
        installations.get("plugins")
        or installations.get("installations")
        or installations.get("data")
        or []
    )

    # Uninstall old version if exists
    for installed in installed_list:
        installation_id = installed.get("id") or installed.get("installation_id")
        if installation_id:
            print(f"  Uninstalling old version (id: {installation_id})...")
            uninstall_plugin(host, cookies, csrf_token, installation_id)
            print(f"  Old version uninstalled.")

    # Install new version
    print(f"  Installing new version...")
    install_plugin(host, cookies, csrf_token, plugin_id)
    print(f"  Installed successfully!")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/install_plugin.py <plugin.difypkg> [plugin2.difypkg ...]", file=sys.stderr)
        sys.exit(1)

    pkg_paths = [Path(p) for p in sys.argv[1:]]
    for p in pkg_paths:
        if not p.exists():
            print(f"Package not found: {p}", file=sys.stderr)
            sys.exit(1)

    try:
        creds = load_credentials()
        host = creds["host"]

        print(f"Logging in to {host}...")
        cookies, csrf_token = login(host, creds["email"], creds["password"])
        print("Login successful.\n")

        results = {}
        for pkg_path in pkg_paths:
            try:
                install_single_plugin(host, cookies, csrf_token, pkg_path)
                results[pkg_path.name] = "OK"
            except Exception as e:
                print(f"  FAILED: {e}", file=sys.stderr)
                results[pkg_path.name] = f"FAILED: {e}"

        print(f"\n{'='*50}")
        print("  Summary")
        print(f"{'='*50}")
        for name, status in results.items():
            print(f"  {name}: {status}")

        if any("FAILED" in s for s in results.values()):
            sys.exit(1)

    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
