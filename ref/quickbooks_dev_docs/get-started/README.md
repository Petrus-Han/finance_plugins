# Getting Started with QuickBooks Online API

> Set up your Intuit Developer Account and start building

## Overview

The QuickBooks Online Accounting API uses REST architecture to integrate your app with QuickBooks Online and the Intuit Financial Ecosystem.

## Pages in This Section

| Page | Description | Mercury Relevance |
|------|-------------|-------------------|
| [Intuit App Partner Program FAQ](partner-faq.md) | FAQ about becoming an Intuit partner, certification, security requirements | Understanding partnership requirements for production deployment |
| [Start Developing Your App](start-developing-your-app.md) | Create an Intuit Developer account and register your app | **★ Essential** - First step for any integration |
| [Build Your First App](build-your-first-app.md) | Demo app tutorials for .NET, Java, and PHP | Reference implementations and patterns |
| [Get Started with API Explorer](get-started-with-the-api-explorer.md) | Interactive API testing tool | Testing QuickBooks API calls before coding |
| [Create a Request](create-a-request.md) | Basic request structure, headers, and response handling | **★ Essential** - Core API communication patterns |
| [Get Client ID and Secret](get-client-id-and-client-secret.md) | Managing OAuth credentials | **★ Essential** - Required for OAuth flow |
| [App Settings](app-settings.md) | Configuring redirect URIs, scopes, and app details | OAuth configuration for the sync plugin |
| [Developer Account Settings](developer-account-settings.md) | Managing developer profile and notifications | Account maintenance |
| [Share Workspace](share-workspace.md) | Team collaboration on developer portal | Team development workflow |

---

## Quick Start Steps

### 1. Create an Intuit Developer Account

1. Go to [developer.intuit.com](https://developer.intuit.com/)
2. Click **Sign Up** and create an account
3. Verify your email

### 2. Create an App

1. Go to **My Apps** → **Create an App**
2. Select **QuickBooks Online and Payments**
3. Fill in app details:
   - App name
   - Scopes: Select `com.intuit.quickbooks.accounting`
   - Redirect URIs: Your OAuth callback URLs

### 3. Get Credentials

From your app's dashboard, copy:

| Credential | Where to find |
|------------|---------------|
| **Client ID** | Keys & OAuth section |
| **Client Secret** | Keys & OAuth section |

⚠️ Keep these secure! Never expose in client-side code.

### 4. Create a Sandbox

1. Go to **Sandbox** section in developer portal
2. Create a new sandbox company
3. Use for testing without affecting real data

**Sandbox Base URL**: `https://sandbox-quickbooks.api.intuit.com`

### 5. Implement OAuth 2.0

See [Authentication Guide](../develop/authentication.md) for detailed OAuth implementation.

Quick flow:
```
1. Redirect user → Intuit authorization page
2. User approves → Callback with code + realmId
3. Exchange code → Access token + Refresh token
4. Use access token → API calls
```

### 6. Make Your First API Call

```python
import requests

access_token = "your_access_token"
realm_id = "your_realm_id"

url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{realm_id}/companyinfo/{realm_id}"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)
print(response.json())
```

---

## Development Checklist

- [ ] Intuit Developer account created
- [ ] App registered on developer portal
- [ ] Client ID and Secret obtained
- [ ] Redirect URIs configured
- [ ] Sandbox company created
- [ ] OAuth 2.0 flow implemented
- [ ] Access token obtained
- [ ] First API call successful

---

## Key Resources

| Resource | URL |
|----------|-----|
| Developer Portal | https://developer.intuit.com/ |
| API Explorer | https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account |
| Sandbox Setup | https://developer.intuit.com/app/developer/qbo/docs/develop/sandboxes |
| OAuth 2.0 Guide | https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization |
| SDKs | https://developer.intuit.com/app/developer/qbo/docs/develop/sdks-and-samples |

---

## Available SDKs

| Language | Package |
|----------|---------|
| Python | `intuit-oauth`, `python-quickbooks` |
| .NET | `Intuit.Ipp.Data`, `Intuit.Ipp.OAuth2PlatformClient` |
| Java | `ipp-v3-java-devkit` |
| PHP | `quickbooks-php` |

---

## Environments

| Environment | Base URL | Use Case |
|-------------|----------|----------|
| **Sandbox** | `https://sandbox-quickbooks.api.intuit.com` | Development & testing |
| **Production** | `https://quickbooks.api.intuit.com` | Live data |

Always develop against sandbox first, then switch to production for deployment.

---

## Common First Steps for Mercury Integration

1. **Set up OAuth** to connect user's QuickBooks company
2. **Query Accounts** to find/create Mercury bank account mapping
3. **Query Vendors** to cache existing vendors for matching
4. **Query Customers** to cache existing customers for matching
5. **Test Purchase creation** with a sandbox transaction
6. **Test Deposit creation** with a sandbox transaction
7. **Test Transfer creation** for internal transfers

See [API Reference](../api-reference/) for detailed entity documentation.
