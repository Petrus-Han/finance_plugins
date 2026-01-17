# QuickBooks OAuth 2.0 Authentication

> Guide for authenticating with QuickBooks Online API

## Overview

QuickBooks uses OAuth 2.0 for authentication. Your app must be registered on the [Intuit Developer Portal](https://developer.intuit.com/).

## OAuth 2.0 Flow

```
┌──────────┐      ┌─────────────┐      ┌─────────────┐
│  User    │      │  Your App   │      │  QuickBooks │
└────┬─────┘      └──────┬──────┘      └──────┬──────┘
     │                   │                    │
     │ 1. Connect        │                    │
     ├──────────────────>│                    │
     │                   │                    │
     │ 2. Redirect to QB │                    │
     │<──────────────────│                    │
     │                   │                    │
     │ 3. Authorize      │                    │
     ├───────────────────┼───────────────────>│
     │                   │                    │
     │ 4. Callback w/code│                    │
     │<───────────────────────────────────────│
     │                   │                    │
     │ 5. Exchange code  │                    │
     │                   ├───────────────────>│
     │                   │                    │
     │                   │ 6. Access token    │
     │                   │<───────────────────│
     │                   │                    │
     │                   │ 7. API calls       │
     │                   ├───────────────────>│
     │                   │                    │
```

## Configuration

### Required Values

| Value | Description |
|-------|-------------|
| `client_id` | From Intuit Developer Portal |
| `client_secret` | From Intuit Developer Portal |
| `redirect_uri` | Your callback URL (must be registered) |
| `scope` | `com.intuit.quickbooks.accounting` |

### Endpoints

| Environment | Authorization | Token |
|-------------|---------------|-------|
| Production | `https://appcenter.intuit.com/connect/oauth2` | `https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer` |
| Sandbox | Same | Same |

## Step-by-Step Implementation

### Step 1: Generate Authorization URL

```python
import urllib.parse
import secrets

def get_authorization_url(client_id, redirect_uri, state=None):
    """Generate QuickBooks OAuth authorization URL."""
    if state is None:
        state = secrets.token_urlsafe(32)
    
    params = {
        "client_id": client_id,
        "response_type": "code",
        "scope": "com.intuit.quickbooks.accounting",
        "redirect_uri": redirect_uri,
        "state": state
    }
    
    base_url = "https://appcenter.intuit.com/connect/oauth2"
    return f"{base_url}?{urllib.parse.urlencode(params)}", state
```

### Step 2: Handle Callback

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/callback")
def oauth_callback():
    # Verify state matches
    state = request.args.get("state")
    if state != stored_state:
        return "Invalid state", 400
    
    # Get authorization code
    code = request.args.get("code")
    realm_id = request.args.get("realmId")  # Company ID
    
    # Exchange for tokens
    tokens = exchange_code_for_tokens(code)
    
    # Store tokens securely
    save_tokens(realm_id, tokens)
    
    return "Connected successfully!"
```

### Step 3: Exchange Code for Tokens

```python
import requests
import base64

def exchange_code_for_tokens(code, client_id, client_secret, redirect_uri):
    """Exchange authorization code for access and refresh tokens."""
    
    token_url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    
    # Basic auth header
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }
    
    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    
    return response.json()
```

### Token Response

```json
{
  "token_type": "bearer",
  "access_token": "eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxn...",
  "refresh_token": "AB11234567890...",
  "expires_in": 3600,
  "x_refresh_token_expires_in": 8726400
}
```

| Token | Expires | Description |
|-------|---------|-------------|
| `access_token` | 1 hour | Used for API calls |
| `refresh_token` | 100 days | Used to get new access tokens |

### Step 4: Refresh Access Token

```python
def refresh_access_token(refresh_token, client_id, client_secret):
    """Refresh expired access token."""
    
    token_url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    
    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    
    return response.json()
```

### Step 5: Make API Calls

```python
def make_qb_request(method, endpoint, realm_id, access_token, data=None):
    """Make authenticated request to QuickBooks API."""
    
    base_url = "https://quickbooks.api.intuit.com"  # or sandbox-quickbooks.api.intuit.com
    url = f"{base_url}/v3/company/{realm_id}/{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    
    response.raise_for_status()
    return response.json()
```

## Token Management

### Best Practices

1. **Store securely**: Encrypt tokens at rest
2. **Refresh proactively**: Refresh before expiry (e.g., at 50 minutes)
3. **Handle failures**: Implement retry logic for token refresh
4. **Track realm_id**: Store realm_id (company ID) with tokens

### Token Refresh Strategy

```python
import time

class QuickBooksClient:
    def __init__(self, realm_id, tokens, client_id, client_secret):
        self.realm_id = realm_id
        self.tokens = tokens
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_expiry = time.time() + tokens.get("expires_in", 3600)
    
    def get_access_token(self):
        """Get valid access token, refreshing if needed."""
        # Refresh 5 minutes before expiry
        if time.time() > self.token_expiry - 300:
            self._refresh_token()
        return self.tokens["access_token"]
    
    def _refresh_token(self):
        """Refresh the access token."""
        new_tokens = refresh_access_token(
            self.tokens["refresh_token"],
            self.client_id,
            self.client_secret
        )
        self.tokens = new_tokens
        self.token_expiry = time.time() + new_tokens.get("expires_in", 3600)
        # Save updated tokens to storage
        save_tokens(self.realm_id, new_tokens)
```

## Scopes

| Scope | Description |
|-------|-------------|
| `com.intuit.quickbooks.accounting` | Full access to accounting data |
| `com.intuit.quickbooks.payment` | Access to payment data |
| `openid` | OpenID Connect |
| `profile` | User profile info |
| `email` | User email |
| `phone` | User phone |
| `address` | User address |

For Mercury-QuickBooks sync, you only need: `com.intuit.quickbooks.accounting`

## Error Handling

### Common OAuth Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `invalid_grant` | Code expired or already used | Restart authorization flow |
| `invalid_client` | Wrong client_id/secret | Check credentials |
| `access_denied` | User denied access | User must approve |
| `invalid_token` | Token expired | Refresh token |

### API Error Response

```json
{
  "Fault": {
    "Error": [
      {
        "Message": "message=AuthenticationFailed; errorCode=003200; statusCode=401",
        "Detail": "Token expired",
        "code": "3200"
      }
    ],
    "type": "AUTHENTICATION"
  }
}
```

## Revoke Token

```python
def revoke_token(token, client_id, client_secret):
    """Revoke access or refresh token."""
    
    revoke_url = "https://developer.api.intuit.com/v2/oauth2/tokens/revoke"
    
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    data = {"token": token}
    
    response = requests.post(revoke_url, headers=headers, json=data)
    return response.status_code == 200
```

## Disconnect

When user disconnects, revoke tokens and delete stored credentials:

```python
def disconnect_company(realm_id, tokens, client_id, client_secret):
    """Disconnect company and clean up."""
    
    # Revoke tokens
    revoke_token(tokens["access_token"], client_id, client_secret)
    revoke_token(tokens["refresh_token"], client_id, client_secret)
    
    # Delete stored tokens
    delete_tokens(realm_id)
```

## Sandbox vs Production

| Environment | Base API URL | Same OAuth Endpoints |
|-------------|--------------|----------------------|
| Sandbox | `https://sandbox-quickbooks.api.intuit.com` | Yes |
| Production | `https://quickbooks.api.intuit.com` | Yes |

Use sandbox for development and testing. Sandbox has sample company data.

## References

- [Intuit Developer Portal](https://developer.intuit.com/)
- [OAuth 2.0 Documentation](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization)
- [API Explorer](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account)
