#!/usr/bin/env python3
"""
Get a new debug key from Dify for remote plugin debugging.
Usage: python get_debug_key.py [--output-env]
"""

import httpx
import sys
import json
import base64
from pathlib import Path

# Find credential file
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CREDENTIAL_FILE = PROJECT_ROOT / ".credential"


def load_credentials() -> dict:
    """Load credentials from .credential file."""
    if not CREDENTIAL_FILE.exists():
        print(f"Error: Credential file not found: {CREDENTIAL_FILE}")
        print("\nCreate a .credential file with:")
        print(json.dumps({
            "host": "https://your-dify.com",
            "email": "your-email@example.com",
            "password": "your-password"
        }, indent=2))
        sys.exit(1)

    with open(CREDENTIAL_FILE) as f:
        return json.load(f)


def login(host: str, email: str, password: str, verbose: bool = True) -> httpx.Cookies:
    """Login to Dify and return the cookies containing access token."""
    url = f"{host}/console/api/login"
    # Dify expects password to be Base64 encoded
    encoded_password = base64.b64encode(password.encode()).decode()
    payload = {
        "email": email,
        "password": encoded_password,
        "remember_me": True
    }

    # Use a client to capture cookies
    with httpx.Client(timeout=30) as client:
        response = client.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()
            if data.get("result") == "success":
                if verbose:
                    print("Login successful!")
                return response.cookies
            else:
                print(f"Login failed: {data}")
                sys.exit(1)
        else:
            print(f"Login failed: {response.status_code}")
            print(response.text)
            sys.exit(1)


def get_debug_key(host: str, cookies: httpx.Cookies) -> dict:
    """Get a new debug key from Dify."""
    url = f"{host}/console/api/workspaces/current/plugin/debugging-key"

    # Extract CSRF token from cookies
    csrf_token = None
    for name, value in cookies.items():
        if "csrf" in name.lower():
            csrf_token = value
            break

    headers = {}
    if csrf_token:
        headers["X-Csrf-Token"] = csrf_token

    with httpx.Client(timeout=30, cookies=cookies) as client:
        response = client.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error getting debug key: {response.status_code}")
            print(response.text)
            return None


def main():
    output_env = "--output-env" in sys.argv
    verbose = not output_env

    # Load credentials
    creds = load_credentials()
    host = creds["host"]
    email = creds["email"]
    password = creds["password"]

    # Login
    if verbose:
        print(f"Logging in to {host}...")
    cookies = login(host, email, password, verbose)

    # Get debug key
    result = get_debug_key(host, cookies)
    if result:
        key = result.get("key")
        if output_env:
            # Output as .env format
            print(f"INSTALL_METHOD=remote")
            print(f"REMOTE_INSTALL_HOST={host}")
            print(f"REMOTE_INSTALL_PORT=5003")
            print(f"REMOTE_INSTALL_KEY={key}")
        else:
            print(f"\nDebug Key: {key}")
            print(f"\nUpdate your .env files with:")
            print(f"REMOTE_INSTALL_KEY={key}")


if __name__ == "__main__":
    main()
