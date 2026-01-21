#!/usr/bin/env python3
"""
QuickBooks OAuth2 Helper Script

Usage:
    1. Run: python quickbooks_oauth.py
    2. Open the authorization URL in browser
    3. Authorize and copy the redirect URL
    4. Paste the redirect URL when prompted
    5. Tokens will be saved to .credentials file
"""

import base64
import json
import urllib.parse
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import threading

# QuickBooks OAuth2 endpoints
AUTHORIZATION_URL = "https://appcenter.intuit.com/connect/oauth2"
TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
# Use localhost for local OAuth flow, or Dify callback for production
LOCAL_REDIRECT_URI = "http://localhost:8765/callback"
DIFY_REDIRECT_URI = "https://dify.greeep.com/console/api/oauth/plugin/b03855dd-de51-486a-b6d6-37fd9478358d/quickbooks/quickbooks/tool/callback"
REDIRECT_URI = LOCAL_REDIRECT_URI  # Default to local for testing
SCOPES = "com.intuit.quickbooks.accounting"

# Load credentials
CREDENTIALS_FILE = Path(__file__).parent.parent / "quickbooks_plugin" / ".credentials"


def load_credentials():
    if CREDENTIALS_FILE.exists():
        with open(CREDENTIALS_FILE) as f:
            return json.load(f)
    return {}


def save_credentials(creds):
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(creds, f, indent=2)
    print(f"\nCredentials saved to {CREDENTIALS_FILE}")


def get_authorization_url(client_id: str) -> str:
    """Generate the OAuth2 authorization URL."""
    params = {
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "state": "security_token",
    }
    return f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"


def exchange_code_for_tokens(client_id: str, client_secret: str, code: str, realm_id: str) -> dict:
    """Exchange authorization code for access and refresh tokens."""
    import httpx

    # Create Basic Auth header
    auth_string = f"{client_id}:{client_secret}"
    auth_header = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    response = httpx.post(TOKEN_URL, headers=headers, data=data, timeout=30)

    if response.status_code == 200:
        tokens = response.json()
        return {
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
            "realm_id": realm_id,
            "expires_in": tokens.get("expires_in"),
            "x_refresh_token_expires_in": tokens.get("x_refresh_token_expires_in"),
        }
    else:
        raise Exception(f"Token exchange failed: {response.status_code} - {response.text}")


def refresh_access_token(client_id: str, client_secret: str, refresh_token: str) -> dict:
    """Refresh the access token using refresh token."""
    import httpx

    auth_string = f"{client_id}:{client_secret}"
    auth_header = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    response = httpx.post(TOKEN_URL, headers=headers, data=data, timeout=30)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Token refresh failed: {response.status_code} - {response.text}")


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for OAuth callback."""

    code = None
    realm_id = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        OAuthCallbackHandler.code = params.get("code", [None])[0]
        OAuthCallbackHandler.realm_id = params.get("realmId", [None])[0]

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if OAuthCallbackHandler.code:
            self.wfile.write(b"""
            <html><body>
            <h1>Authorization Successful!</h1>
            <p>You can close this window and return to the terminal.</p>
            </body></html>
            """)
        else:
            error = params.get("error", ["Unknown error"])[0]
            self.wfile.write(f"""
            <html><body>
            <h1>Authorization Failed</h1>
            <p>Error: {error}</p>
            </body></html>
            """.encode())

    def log_message(self, format, *args):
        pass  # Suppress logging


def main():
    creds = load_credentials()

    client_id = creds.get("client_id")
    client_secret = creds.get("client_secret")

    if not client_id or not client_secret:
        print("Error: client_id and client_secret not found in .credentials")
        print("Please add them first.")
        return

    # Check if we already have tokens
    if creds.get("access_token") and creds.get("refresh_token"):
        print("Existing tokens found. Options:")
        print("1. Use existing tokens")
        print("2. Refresh access token")
        print("3. Get new tokens (local OAuth flow)")
        print("4. Manually enter tokens")
        print("5. Exchange authorization code for tokens")
        choice = input("\nChoice [1/2/3/4/5]: ").strip()

        if choice == "1":
            print(f"\nAccess Token: {creds['access_token'][:50]}...")
            print(f"Realm ID: {creds.get('realm_id')}")
            return
        elif choice == "2":
            try:
                new_tokens = refresh_access_token(
                    client_id, client_secret, creds["refresh_token"]
                )
                creds["access_token"] = new_tokens["access_token"]
                creds["refresh_token"] = new_tokens.get("refresh_token", creds["refresh_token"])
                save_credentials(creds)
                print(f"\nNew Access Token: {creds['access_token'][:50]}...")
                return
            except Exception as e:
                print(f"Refresh failed: {e}")
                print("Proceeding with full OAuth flow...")
        elif choice == "4":
            manual_token_entry(creds)
            return
        elif choice == "5":
            exchange_code_manually(creds, client_id, client_secret)
            return
    else:
        print("Options:")
        print("1. Start local OAuth flow (localhost callback)")
        print("2. Manually enter tokens")
        print("3. Exchange authorization code for tokens")
        choice = input("\nChoice [1/2/3]: ").strip()

        if choice == "2":
            manual_token_entry(creds)
            return
        elif choice == "3":
            exchange_code_manually(creds, client_id, client_secret)
            return

    # Start local OAuth flow
    run_local_oauth_flow(creds, client_id, client_secret)


def run_local_oauth_flow(creds: dict, client_id: str, client_secret: str):
    """Run OAuth flow with local callback server."""
    print("\nStarting local OAuth2 flow...")
    print(f"Listening for callback on {LOCAL_REDIRECT_URI}")

    server = HTTPServer(("localhost", 8765), OAuthCallbackHandler)
    server_thread = threading.Thread(target=server.handle_request)
    server_thread.start()

    # Generate authorization URL with local callback
    auth_url = get_authorization_url(client_id)
    print(f"\n{'='*60}")
    print("QuickBooks OAuth2 Authorization")
    print(f"{'='*60}")
    print(f"\nAuthorization URL:\n{auth_url}\n")

    try:
        webbrowser.open(auth_url)
        print("Browser opened automatically.")
    except:
        print("Couldn't open browser. Please copy the URL manually.")

    print("\nWaiting for authorization callback...")
    server_thread.join(timeout=300)  # Wait up to 5 minutes

    if OAuthCallbackHandler.code:
        print(f"\nReceived authorization code!")
        realm_id = OAuthCallbackHandler.realm_id or creds.get("realm_id")
        print(f"Realm ID: {realm_id}")

        # Exchange code for tokens
        try:
            tokens = exchange_code_for_tokens(
                client_id, client_secret,
                OAuthCallbackHandler.code,
                realm_id
            )

            creds.update(tokens)
            save_credentials(creds)

            print(f"\n✓ OAuth2 complete!")
            print(f"Access Token: {tokens['access_token'][:50]}...")
            print(f"Realm ID: {tokens['realm_id']}")
            print(f"Token expires in: {tokens['expires_in']} seconds")

        except Exception as e:
            print(f"\nError exchanging code for tokens: {e}")
    else:
        print("\nNo authorization code received. Please try again.")


def exchange_code_manually(creds: dict, client_id: str, client_secret: str):
    """Manually exchange an authorization code for tokens."""
    print("\n" + "="*60)
    print("Exchange Authorization Code for Tokens")
    print("="*60)
    print("\nIf you captured the authorization code from a failed callback,")
    print("enter it here to exchange it for access tokens.\n")

    code = input("Authorization Code: ").strip()
    if not code:
        print("No code entered.")
        return

    realm_id = creds.get("realm_id")
    if not realm_id:
        realm_id = input("Realm ID (Company ID): ").strip()

    if not realm_id:
        print("Realm ID is required.")
        return

    try:
        tokens = exchange_code_for_tokens(client_id, client_secret, code, realm_id)
        creds.update(tokens)
        save_credentials(creds)

        print(f"\n✓ Token exchange successful!")
        print(f"Access Token: {tokens['access_token'][:50]}...")
        print(f"Realm ID: {tokens['realm_id']}")
        print(f"Token expires in: {tokens['expires_in']} seconds")

    except Exception as e:
        print(f"\nError exchanging code: {e}")


def manual_token_entry(creds):
    """Allow manual entry of tokens (e.g., copied from Dify)."""
    print("\n" + "="*60)
    print("Manual Token Entry")
    print("="*60)
    print("\nEnter the tokens from Dify (or press Enter to skip):\n")

    access_token = input("Access Token: ").strip()
    if access_token:
        creds["access_token"] = access_token

    refresh_token = input("Refresh Token: ").strip()
    if refresh_token:
        creds["refresh_token"] = refresh_token

    realm_id = input("Realm ID (Company ID): ").strip()
    if realm_id:
        creds["realm_id"] = realm_id

    if access_token or refresh_token or realm_id:
        save_credentials(creds)
        print("\n✓ Tokens saved successfully!")
        if creds.get("access_token"):
            print(f"Access Token: {creds['access_token'][:50]}...")
        if creds.get("realm_id"):
            print(f"Realm ID: {creds['realm_id']}")
    else:
        print("\nNo tokens entered.")


if __name__ == "__main__":
    main()
