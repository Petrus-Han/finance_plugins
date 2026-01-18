# SDKs and Sample Code

> QuickBooks Online API - SDK Reference

Intuit provides official OAuth clients and community-contributed SDKs for integrating with the QuickBooks Online API.

---

## Available SDKs by Language

| Language | OAuth Client | SDK | Type |
|----------|-------------|-----|------|
| **Python** | [intuit-oauth](https://pypi.org/project/intuit-oauth) | [python-quickbooks](https://pypi.python.org/pypi/python-quickbooks) | Community |
| **.NET** | Official | Official | Official |
| **Java** | Official | Official | Official |
| **PHP** | [intuit-oauth](https://packagist.org/packages/intuit/intuit-oauth) | Community | Mixed |
| **Node.js** | [intuit-oauth](https://www.npmjs.com/package/intuit-oauth) | Community | Mixed |
| **Ruby** | Community | Community | Community |

---

## Python

### Intuit OAuth2 Python Client (Official)

The official OAuth 2.0 client provides methods for working with Intuit's OAuth and OpenID implementation.

**Installation:**
```bash
pip install intuit-oauth
```

**PyPI:** https://pypi.org/project/intuit-oauth

**Features:**
- OAuth 2.0 authorization flow
- Token management (refresh, revoke)
- OpenID Connect support
- Token validation

### Python SDK (Community Contributed)

> **Note**: Intuit is not affiliated with community-contributed SDKs and assumes no liability for them. Evaluate such tools and their associated terms and conditions to make your own assessments.

**Installation:**
```bash
pip install python-quickbooks
```

**PyPI:** https://pypi.python.org/pypi/python-quickbooks

**GitHub:** https://github.com/eddiejessup/python-quickbooks

**Features:**
- CRUD operations for all QuickBooks entities
- Query builder for complex queries
- Batch operations
- Report generation

---

## .NET

### Official .NET SDK

**NuGet:** https://www.nuget.org/packages/IppDotNetSdkForQuickBooksApiV3

**Installation:**
```bash
Install-Package IppDotNetSdkForQuickBooksApiV3
```

---

## Java

### Official Java SDK

**Maven Repository:** Available on Maven Central

**Installation (Maven):**
```xml
<dependency>
    <groupId>com.intuit.quickbooks-online</groupId>
    <artifactId>ipp-v3-java-devkit</artifactId>
    <version>LATEST</version>
</dependency>
```

---

## PHP

### Intuit OAuth2 PHP Client

**Installation:**
```bash
composer require intuit/intuit-oauth
```

**Packagist:** https://packagist.org/packages/intuit/intuit-oauth

---

## Node.js

### Intuit OAuth2 Node.js Client

**Installation:**
```bash
npm install intuit-oauth
```

**NPM:** https://www.npmjs.com/package/intuit-oauth

---

## OAuth 2.0 Scopes

All SDKs use OAuth 2.0 for authentication. Available scopes:

| Scope | Description |
|-------|-------------|
| `com.intuit.quickbooks.accounting` | QuickBooks Online Accounting API |
| `com.intuit.quickbooks.payment` | QuickBooks Payments API |
| `openid` | OpenID Connect |
| `profile` | User profile information |
| `email` | User email address |
| `phone` | User phone number |
| `address` | User address |

---

## Python OAuth Client Usage Example

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

# Get authorization URL
scopes = [Scopes.ACCOUNTING]
auth_url = auth_client.get_authorization_url(scopes)

# After user authorizes, exchange code for tokens
auth_client.get_bearer_token(auth_code, realm_id)

# Access token is now available
access_token = auth_client.access_token
refresh_token = auth_client.refresh_token
realm_id = auth_client.realm_id

# Refresh token when needed
auth_client.refresh()
```

---

## Python QuickBooks SDK Usage Example

```python
from quickbooks import QuickBooks
from quickbooks.objects.customer import Customer

# Initialize client with tokens
client = QuickBooks(
    auth_client=auth_client,
    refresh_token=refresh_token,
    company_id=realm_id
)

# Query customers
customers = Customer.all(qb=client)

# Get specific customer
customer = Customer.get(1, qb=client)

# Create new customer
new_customer = Customer()
new_customer.DisplayName = "New Customer"
new_customer.save(qb=client)

# Query with filter
from quickbooks.objects.account import Account
accounts = Account.filter(
    AccountType="Bank",
    qb=client
)
```

---

## Making Direct API Calls (Without SDK)

If not using an SDK, you can make direct HTTP requests:

```python
import requests

base_url = "https://sandbox-quickbooks.api.intuit.com/v3"
company_id = "YOUR_COMPANY_ID"

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

# Create a purchase
purchase_data = {
    "AccountRef": {"value": "123"},
    "PaymentType": "Cash",
    "Line": [
        {
            "Amount": 100.00,
            "DetailType": "AccountBasedExpenseLineDetail",
            "AccountBasedExpenseLineDetail": {
                "AccountRef": {"value": "456"}
            }
        }
    ]
}

response = requests.post(
    f"{base_url}/company/{company_id}/purchase",
    headers=headers,
    json=purchase_data
)
```

---

## SDK Selection Guidelines

| Use Case | Recommendation |
|----------|----------------|
| Quick prototyping | Community SDK (higher level abstraction) |
| Production app | Community SDK + Official OAuth Client |
| Custom integration | Direct API calls with Official OAuth Client |
| Enterprise app | Official SDKs (.NET, Java) |

---

## Related Documentation

- [OAuth 2.0 Authentication](./authentication-and-authorization/oauth-2.0.md)
- [Postman Testing](./postman.md)
- [API Reference](../api-reference/README.md)
- [Troubleshooting](./troubleshooting.md)
