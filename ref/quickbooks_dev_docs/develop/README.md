# Develop - QuickBooks Online API

> Development documentation for QuickBooks Online API integration

This section covers everything you need to develop and integrate with the QuickBooks Online API.

---

## Documentation Index

### Testing & Development Environment

| Document | Description |
|----------|-------------|
| [Sandbox Testing](./sandboxes.md) | Create and manage sandbox companies for testing |
| [Sandbox FAQ](./sandbox-faqs.md) | Common questions about sandbox environments |
| [Postman Setup](./postman.md) | Set up Postman for API testing |

### SDKs & Libraries

| Document | Description |
|----------|-------------|
| [SDKs and Sample Code](./sdks-and-samples.md) | Official and community SDKs for all languages |

### Authentication & Authorization

| Document | Description |
|----------|-------------|
| [OAuth 2.0 Setup](./authentication-and-authorization/oauth-2.0.md) | Complete OAuth 2.0 implementation guide |
| [Authentication Overview](./authentication.md) | Basic authentication concepts |

### Real-time Notifications

| Document | Description |
|----------|-------------|
| [Webhooks](./webhooks.md) | Set up webhooks for real-time data change notifications |

### Error Handling

| Document | Description |
|----------|-------------|
| [Troubleshooting](./troubleshooting.md) | Common errors and solutions |

---

## Quick Start

### 1. Set Up Your Development Environment

1. Create a [developer account](https://developer.intuit.com/)
2. Create an app in the Developer Portal
3. Get your [sandbox credentials](./sandboxes.md)

### 2. Implement Authentication

1. Set up [OAuth 2.0](./authentication-and-authorization/oauth-2.0.md)
2. Store tokens securely
3. Implement token refresh

### 3. Make API Calls

```python
import requests

base_url = "https://sandbox-quickbooks.api.intuit.com/v3"
company_id = "YOUR_COMPANY_ID"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json"
}

# Query company info
response = requests.get(
    f"{base_url}/company/{company_id}/companyinfo/{company_id}",
    headers=headers
)
```

### 4. Set Up Webhooks (Optional)

1. Configure [webhook endpoints](./webhooks.md)
2. Validate webhook signatures
3. Process notifications asynchronously

---

## Key Endpoints

### Base URLs

| Environment | URL |
|-------------|-----|
| Sandbox | `https://sandbox-quickbooks.api.intuit.com/v3` |
| Production | `https://quickbooks.api.intuit.com/v3` |

### OAuth URLs

| Purpose | URL |
|---------|-----|
| Authorization | `https://appcenter.intuit.com/connect/oauth2` |
| Token Exchange | `https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer` |
| Token Revocation | `https://developer.api.intuit.com/v2/oauth2/tokens/revoke` |

---

## Token Lifetimes

| Token | Lifetime |
|-------|----------|
| Access Token | 60 minutes |
| Refresh Token | 100 days |

---

## Rate Limits

| Limit | Value |
|-------|-------|
| Requests per minute (per app, per company) | 500 |
| Sandbox requests per minute | 500 |

---

## Scopes

| Scope | Description |
|-------|-------------|
| `com.intuit.quickbooks.accounting` | QuickBooks Online Accounting API |
| `com.intuit.quickbooks.payment` | QuickBooks Payments API |
| `openid` | OpenID Connect |
| `profile` | User profile information |
| `email` | User email address |

---

## Development Workflow

```
┌─────────────────┐
│  1. Create App  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Get Sandbox  │
│   Credentials   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. Implement    │
│   OAuth 2.0     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Test with    │
│   Sandbox       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. Set Up       │
│   Webhooks      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 6. Go Live      │
│   (Production)  │
└─────────────────┘
```

---

## Related Documentation

- [Get Started](../get-started/README.md) - Initial setup and account creation
- [Learn](../learn/rest-api-features.md) - API concepts and features
- [API Reference](../api-reference/) - Entity-specific documentation
- [Use Cases](../use-cases/README.md) - Common integration patterns
