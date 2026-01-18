# Set Up OAuth 2.0

> QuickBooks Online API - OAuth 2.0 Implementation Guide

Use the OAuth 2.0 protocol to implement authentication and authorization. Authorization is essential for both testing via sandbox companies and production apps.

---

## Overview

The OAuth 2.0 flow enables users to authorize your app and give it permission to access their QuickBooks Online company data.

**Flow Summary:**
1. Your app sends an authorization request
2. User grants permission on the authorization page
3. Intuit OAuth 2.0 Server sends an authorization code back
4. Your app exchanges the code for access and refresh tokens
5. Use access tokens to make API calls

---

## Step 1: Create Your App on the Intuit Developer Portal

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account
2. Create an app on the Intuit Developer Portal
3. Select the **QuickBooks Online Accounting** scope

This app provides the credentials you'll need for authorization requests.

---

## Step 2: Practice Authorization in the OAuth Playground

Check out the [OAuth Playground](./oauth-2.0-playground.md) to preview each step of the authorization flow. We've provided sample data, like the redirect URI, so you can focus on the overall flow.

---

## Step 3: Start Developing with an SDK

Our SDKs come with a built-in OAuth 2.0 Client Library and handle many parts of the authorization implementation.

**Available OAuth 2.0 Client Libraries:**
- [.NET](https://www.nuget.org/packages/IppDotNetSdkForQuickBooksApiV3)
- [Java](https://search.maven.org/artifact/com.intuit.quickbooks-online/oauth2-platform-api)
- [PHP](https://packagist.org/packages/intuit/intuit-oauth)
- [Node.js](https://www.npmjs.com/package/intuit-oauth)
- [Python](https://pypi.org/project/intuit-oauth)
- [Ruby](https://rubygems.org/gems/intuit-oauth)

### Python Installation

```bash
pip install intuit-oauth
```

> **Note**: SDKs are only for OAuth 2.0 and QuickBooks Online. SDKs aren't required but are strongly encouraged given the importance of OAuth implementation.

---

## Step 4: Understand the End-to-End Authorization Flow

### Creating Authorization Requests
1. Review the scopes your app uses
2. Configure your app with correct credentials (Client ID and Client Secret)
3. Set up redirect URIs
4. Review base URLs in discovery documents
5. Create authorization requests

### Managing the Authorization Flow
1. When a user connects, your app sends an authorization request
2. User is redirected to the authorization page ("user consent" step)
3. If user authorizes, server sends an authorization code back

### Getting Access and Refresh Tokens
1. Your app exchanges the authorization code for tokens
2. Extract access and refresh tokens from the response

### Making API Calls
1. Use access tokens to call APIs
2. Refresh access tokens when they expire
3. If refresh token expires, user must re-authorize

---

## Step 5: Get Your App's Credentials

1. Sign in to your [Intuit Developer account](https://developer.intuit.com/dashboard)
2. Go to your app's **Keys & OAuth** section
3. For **production**: Use credentials from the Production section
4. For **sandbox testing**: Use credentials from the Development section

---

## Step 6: Discovery Documents

OAuth 2.0 requires multiple URLs for authentication and token requests. Use discovery documents to simplify implementation.

**Discovery Document URLs:**
- **Sandbox**: `https://developer.intuit.com/.well-known/openid_sandbox_configuration`
- **Production**: `https://developer.intuit.com/.well-known/openid_configuration`

**Key Endpoints from Discovery Documents:**

| Endpoint | Sandbox URL | Production URL |
|----------|-------------|----------------|
| Authorization | `https://appcenter.intuit.com/connect/oauth2` | `https://appcenter.intuit.com/connect/oauth2` |
| Token | `https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer` | `https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer` |
| Revocation | `https://developer.api.intuit.com/v2/oauth2/tokens/revoke` | `https://developer.api.intuit.com/v2/oauth2/tokens/revoke` |
| UserInfo | `https://accounts.platform.intuit.com/v1/openid_connect/userinfo` | `https://accounts.platform.intuit.com/v1/openid_connect/userinfo` |

---

## Step 7: Add Your App's Redirect URIs

Add at least one redirect URI for your app. URIs handle responses from the OAuth 2.0 Server during authorization.

**Best Practice**: Design endpoints so they don't expose authorization codes to other resources on the page.

---

## Step 8: Create an Authorization Request

### Authorization Request Parameters

| Field | Description | Required |
|-------|-------------|----------|
| `client_id` | Identifies your app (from Step 5) | Yes |
| `scope` | Space-delimited list of scopes | Yes |
| `redirect_uri` | Where server redirects after authorization | Yes |
| `response_type` | Always set to `code` | Yes |
| `state` | For validation and CSRF prevention | Yes |
| `claims` | Optional JSON for OpenID Connect claims | No |

### Available Scopes

| Scope | Description |
|-------|-------------|
| `com.intuit.quickbooks.accounting` | QuickBooks Online Accounting API |
| `com.intuit.quickbooks.payment` | QuickBooks Payments API |
| `openid` | OpenID Connect |
| `profile` | User profile information |
| `email` | User email address |
| `phone` | User phone number |
| `address` | User address |

### Python Example

```python
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes

# Initialize the auth client
auth_client = AuthClient(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    redirect_uri='YOUR_REDIRECT_URI',
    environment='sandbox'  # or 'production'
)

# Prepare scopes
scopes = [Scopes.ACCOUNTING]

# Get the authorization URL
authorize_url = auth_client.get_authorization_url(scopes)
```

### Manual HTTPS Request

```
https://appcenter.intuit.com/connect/oauth2?
    client_id=YOUR_CLIENT_ID&
    response_type=code&
    scope=com.intuit.quickbooks.accounting&
    redirect_uri=https://www.yourapp.com/oauth-redirect&
    state=YOUR_ANTI_CSRF_TOKEN
```

> **Important**: Create authorization requests in a browser modal. If your app doesn't have browser support, use the OAuth Playground or Postman.

---

## Step 9: Redirect Users to the Authorization Page

When users connect, redirect them to start the "user consent" step.

### Python Example

```python
# Redirect user to the authorization URL
# In a web framework like Flask:
return redirect(authorize_url)
```

---

## Step 10: Create the UI for Connection

Options:
- Add a "Connect to QuickBooks" button in your app
- Set up Intuit Single Sign-on from QuickBooks App Store
- Link to your app's website

The UI needs to redirect users to the Intuit OAuth 2.0 Server and open the authorization page.

---

## Step 11: Get the Authorization Code from Server Response

If users authorize, the server sends a response to your redirect URI containing:

```
https://www.yourapp.com/oauth-redirect?
    code=AUTHORIZATION_CODE&
    state=YOUR_ANTI_CSRF_TOKEN&
    realmId=COMPANY_ID
```

### Response Parameters

| Parameter | Description |
|-----------|-------------|
| `code` | Authorization code (max 512 characters) |
| `realmId` | Unique ID of the QuickBooks Online company (also called "company ID") |
| `state` | Should match the state sent in original request |

### Error Responses

| Error | Cause |
|-------|-------|
| `access_denied` | User didn't authorize your app |
| `invalid_scope` | Authorization request has scope issue |

---

## Step 12: Exchange Authorization Code for Access Tokens

### Python Example

```python
# Exchange authorization code for tokens
auth_client.get_bearer_token(auth_code, realm_id=realm_id)

# Access tokens are now available
access_token = auth_client.access_token
refresh_token = auth_client.refresh_token
realm_id = auth_client.realm_id
```

### Manual POST Request

**Endpoint:** `https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer`

**Headers:**
```
Accept: application/json
Authorization: Basic BASE64_ENCODED(client_id:client_secret)
Content-Type: application/x-www-form-urlencoded
```

**Body Parameters:**

| Field | Description | Required |
|-------|-------------|----------|
| `code` | Authorization code from response | Yes |
| `redirect_uri` | Same redirect URI from Step 7 | Yes |
| `grant_type` | Must be `authorization_code` | Yes |

**Example cURL:**
```bash
curl -X POST 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer' \
  -H 'Accept: application/json' \
  -H 'Authorization: Basic BASE64_ENCODED_CREDENTIALS' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=authorization_code&code=AUTH_CODE&redirect_uri=YOUR_REDIRECT_URI'
```

> **Important**: Only send one request to exchange the authorization code. Multiple requests may invalidate tokens.

---

## Step 13: Extract Access and Refresh Tokens

### Token Response

```json
{
  "token_type": "bearer",
  "access_token": "eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0...",
  "refresh_token": "AB11570127472xkApQcsuqTXgmXTmslIuWq7qhxlcMWHfC",
  "expires_in": 3600,
  "x_refresh_token_expires_in": 8726400,
  "id_token": "eyJraWQiOiJyMX..."
}
```

### Token Lifetimes

| Token Type | Lifetime |
|------------|----------|
| Access Token | 60 minutes (3600 seconds) |
| Refresh Token | 100 days (8,640,000 seconds) |

---

## Step 14: Refresh Access Tokens

Access tokens expire after 60 minutes. Use the refresh token to get new access tokens.

### Python Example

```python
# Refresh the access token
auth_client.refresh()

# New tokens are available
new_access_token = auth_client.access_token
```

### Manual POST Request

**Endpoint:** `https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer`

**Body Parameters:**

| Field | Description | Required |
|-------|-------------|----------|
| `refresh_token` | Current refresh token | Yes |
| `grant_type` | Must be `refresh_token` | Yes |

**Example cURL:**
```bash
curl -X POST 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer' \
  -H 'Accept: application/json' \
  -H 'Authorization: Basic BASE64_ENCODED_CREDENTIALS' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=refresh_token&refresh_token=YOUR_REFRESH_TOKEN'
```

---

## Step 15: Make API Calls

Use the access token in the Authorization header for API calls.

### Python Example

```python
import requests

base_url = "https://sandbox-quickbooks.api.intuit.com/v3"
company_id = realm_id

headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Query company info
response = requests.get(
    f"{base_url}/company/{company_id}/companyinfo/{company_id}",
    headers=headers
)
```

---

## Token Storage Best Practices

1. **Securely store tokens** - Use encryption at rest
2. **Store per-company** - Associate tokens with `realmId`
3. **Track expiration** - Store `expires_in` and refresh proactively
4. **Handle token refresh** - Implement automatic refresh before expiration
5. **Handle refresh token expiration** - Prompt user to re-authorize

---

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `invalid_grant` | Authorization code expired or already used | Get new authorization code |
| `invalid_client` | Wrong client credentials | Check Client ID and Secret |
| `invalid_request` | Missing required parameter | Review request parameters |
| `unauthorized_client` | App not authorized for scope | Check app configuration |

---

## Related Documentation

- [OAuth 2.0 Playground](./oauth-2.0-playground.md)
- [OpenID Connect](./openid-connect.md)
- [Authorization FAQ](./faq.md)
- [Discovery Documents](./oauth-openid-discovery-doc.md)
