# OAuth2 API

OAuth2 Base URL: `https://oauth2.mercury.com`

Sandbox OAuth2 URL: `https://oauth2-sandbox.mercury.com`

The OAuth2 API allows third-party applications to access Mercury accounts on behalf of users.

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/authorize` | Start OAuth2 web flow |
| POST | `/token` | Obtain/refresh access token |

---

## GET /authorize

Redirect users to this endpoint to start the OAuth2 authorization flow.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| client_id | string | Yes | Your OAuth2 client ID |
| redirect_uri | string | Yes | Registered callback URL |
| response_type | string | Yes | Must be `code` |
| scope | string | Yes | Space-separated scopes |
| state | string | Yes | Random string (min 8 chars) |
| code_challenge | string | PKCE | SHA256 hash of code_verifier |
| code_challenge_method | string | PKCE | Must be `S256` |

### Scopes

| Scope | Description |
|-------|-------------|
| read | Access accounts and transactions |
| offline_access | Obtain refresh tokens |

### Example URL

```
https://oauth2.mercury.com/authorize?
  client_id=your_client_id&
  redirect_uri=https://yourapp.com/callback&
  response_type=code&
  scope=read%20offline_access&
  state=abc12345xyz
```

### PKCE Flow (Recommended)

For public clients, use PKCE:

```python
import secrets
import hashlib
import base64

# Generate code_verifier
code_verifier = secrets.token_urlsafe(32)

# Create code_challenge
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).decode().rstrip('=')
```

Then add to authorization URL:
```
&code_challenge=<code_challenge>&code_challenge_method=S256
```

---

## POST /token

Exchange authorization code for access token, or refresh an existing token.

### Exchange Authorization Code

#### Request

```bash
curl -X POST "https://oauth2.mercury.com/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=<authorization_code>" \
  -d "redirect_uri=https://yourapp.com/callback" \
  -d "client_id=<client_id>" \
  -d "client_secret=<client_secret>"
```

#### With PKCE

```bash
curl -X POST "https://oauth2.mercury.com/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=<authorization_code>" \
  -d "redirect_uri=https://yourapp.com/callback" \
  -d "client_id=<client_id>" \
  -d "code_verifier=<code_verifier>"
```

#### Response

```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "dGhpcyBpcyBhIHJl...",
  "scope": "read offline_access"
}
```

### Refresh Token

#### Request

```bash
curl -X POST "https://oauth2.mercury.com/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=<refresh_token>" \
  -d "client_id=<client_id>" \
  -d "client_secret=<client_secret>"
```

#### Response

Same structure as authorization code exchange.

---

## Token Lifetimes

| Token | Lifetime | Notes |
|-------|----------|-------|
| Access Token | 1 hour | Use for API calls |
| Refresh Token | 720 hours (30 days) | One-time use, returns new refresh token |

---

## Using Access Tokens

Include the access token in API requests:

```bash
curl -X GET "https://api.mercury.com/api/v1/accounts" \
  -H "Authorization: Bearer <access_token>"
```

---

## Error Responses

### Authorization Errors

| Error | Description |
|-------|-------------|
| invalid_request | Missing or invalid parameter |
| unauthorized_client | Client not authorized |
| access_denied | User denied authorization |
| invalid_scope | Invalid scope requested |

### Token Errors

| Error | Description |
|-------|-------------|
| invalid_grant | Invalid or expired code/token |
| invalid_client | Client authentication failed |
| unsupported_grant_type | Grant type not supported |

---

## Complete Flow Example

### 1. Redirect User to Authorization

```python
import secrets

state = secrets.token_urlsafe(16)
# Store state in session

auth_url = (
    "https://oauth2.mercury.com/authorize?"
    f"client_id={CLIENT_ID}&"
    f"redirect_uri={REDIRECT_URI}&"
    "response_type=code&"
    "scope=read%20offline_access&"
    f"state={state}"
)
# Redirect user to auth_url
```

### 2. Handle Callback

```python
# User redirected to: https://yourapp.com/callback?code=xxx&state=yyy

def handle_callback(code, state):
    # Verify state matches stored value
    
    # Exchange code for tokens
    response = requests.post(
        "https://oauth2.mercury.com/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )
    
    tokens = response.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    
    # Store tokens securely
    return access_token, refresh_token
```

### 3. Make API Calls

```python
def get_accounts(access_token):
    response = requests.get(
        "https://api.mercury.com/api/v1/accounts",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    return response.json()
```

### 4. Refresh When Needed

```python
def refresh_access_token(refresh_token):
    response = requests.post(
        "https://oauth2.mercury.com/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )
    
    tokens = response.json()
    # Store new tokens
    return tokens["access_token"], tokens["refresh_token"]
```
