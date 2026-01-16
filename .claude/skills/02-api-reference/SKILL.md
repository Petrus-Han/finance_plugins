---
name: api-reference
description: Guide for collecting and organizing API documentation for plugin development. Use when researching target APIs, understanding authentication, or documenting endpoints.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# API Reference Collection

Collect and organize API documentation to prepare for plugin development.

## When to Use This Skill

- Researching target API authentication methods
- Organizing API endpoints and parameters
- Documenting API limitations and considerations
- Creating API documentation references

## API Documentation Structure

### Standard API Documentation Template

```markdown
# [Service Name] API Documentation

## Overview
- Base URL: `https://api.example.com/v1`
- Authentication: OAuth 2.0 / API Key
- Rate Limits: 100 requests/minute

## Authentication

### OAuth 2.0 Flow
1. Authorization URL: `https://auth.example.com/authorize`
2. Token URL: `https://auth.example.com/token`
3. Scopes: `read`, `write`

### Headers
```http
Authorization: Bearer {access_token}
Content-Type: application/json
Accept: application/json
```

## Endpoints

### Get Resources
```http
GET /resources
```

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| limit | integer | No | Max results (default: 50) |
| offset | integer | No | Pagination offset |

**Response:**
```json
{
  "data": [...],
  "meta": {"total": 100}
}
```

## Error Codes
| Code | Meaning | Action |
|------|---------|--------|
| 400 | Bad Request | Check parameters |
| 401 | Unauthorized | Refresh token |
| 429 | Rate Limited | Retry with backoff |
```

## Existing API References

API documentation available in this project:

### Mercury Bank API
- Location: `archive/Mercury_API_Documentation.md`
- Used by: `mercury_tools_plugin`, `mercury_trigger_plugin`

### QuickBooks Online API
- Location: `archive/QuickBooks_API_Documentation.md`
- Used by: `quickbooks_plugin`

### QuickBooks Payments API
- Location: `QuickBooks_Payments_API_Documentation.md`
- Used by: `quickbooks_payments_plugin`

## How to Research New APIs

### Step 1: Get Official Documentation

1. Visit the service provider's developer portal
2. Register a developer account
3. Create an application to get credentials
4. Download or read API documentation

### Step 2: Identify Key Information

```yaml
api_research_checklist:
  authentication:
    - type: "OAuth 2.0 / API Key / Token"
    - authorization_url: ""
    - token_url: ""
    - scopes: []
    
  base_urls:
    sandbox: ""
    production: ""
    
  rate_limits:
    requests_per_minute: 100
    requests_per_day: 10000
    
  required_headers:
    - "Authorization"
    - "Content-Type"
    
  common_endpoints:
    - "GET /resources"
    - "POST /resources"
    - "GET /resources/{id}"
```

### Step 3: Write Diagnostic Script

```python
# test_api.py - Test API connectivity
import httpx

API_KEY = "your_api_key"
BASE_URL = "https://api.example.com/v1"

def test_connection():
    """Test basic API connectivity."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = httpx.get(f"{BASE_URL}/ping", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ API connection successful!")
    else:
        print("❌ API connection failed!")

if __name__ == "__main__":
    test_connection()
```

### Step 4: Document Endpoint Details

For each required endpoint, document:

```yaml
endpoint:
  name: "Get Accounts"
  method: GET
  path: "/accounts"
  
  request:
    headers:
      Authorization: "Bearer {token}"
    query_params:
      - name: limit
        type: integer
        required: false
        default: 50
        
  response:
    success:
      status: 200
      body:
        accounts:
          - id: "string"
            name: "string"
            balance: "number"
    errors:
      - status: 401
        meaning: "Unauthorized"
      - status: 404
        meaning: "Not found"
```

## API Authentication Patterns

### Pattern 1: API Key

```python
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
```

### Pattern 2: OAuth 2.0

```python
class OAuthProvider(ToolProvider):
    def _oauth_get_authorization_url(self, system_credentials):
        return {
            "url": f"{AUTH_URL}?client_id={client_id}&redirect_uri={redirect_uri}&scope={scopes}"
        }
    
    def _oauth_get_credentials(self, system_credentials, code):
        # Exchange code for token
        response = httpx.post(TOKEN_URL, data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret
        })
        return response.json()
    
    def _oauth_refresh_credentials(self, system_credentials, credentials):
        # Refresh expired token
        response = httpx.post(TOKEN_URL, data={
            "grant_type": "refresh_token",
            "refresh_token": credentials["refresh_token"],
            "client_id": client_id,
            "client_secret": client_secret
        })
        return response.json()
```

### Pattern 3: Signature-based (Webhook)

```python
import hmac
import hashlib

def verify_signature(payload, signature, secret):
    """Verify webhook signature."""
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

## Common API Conventions

### RESTful Endpoints

```
GET    /resources          # List all
GET    /resources/{id}     # Get one
POST   /resources          # Create
PUT    /resources/{id}     # Update
DELETE /resources/{id}     # Delete
```

### Pagination

```python
# Offset-based
GET /resources?offset=0&limit=50

# Cursor-based
GET /resources?cursor=abc123&limit=50
```

### Date Formats

```python
# ISO 8601
"2025-01-16T12:00:00Z"

# Unix timestamp
1705406400
```

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "The request was invalid",
    "details": [
      {"field": "amount", "issue": "must be positive"}
    ]
  }
}
```

## Related Skills

- **01-design**: Design phase
- **03-development**: Development implementation (uses these APIs)
- **04-testing**: Testing API calls
- **05-packaging**: Packaging and release

## Quick Reference

### Common HTTP Status Codes

| Code | Meaning | Plugin Handling |
|------|---------|-----------------|
| 200 | Success | Return data |
| 201 | Created | Return created resource |
| 400 | Bad Request | Return validation error |
| 401 | Unauthorized | Refresh token / re-auth |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Return not found message |
| 429 | Rate Limited | Retry with backoff |
| 500 | Server Error | Retry or fail gracefully |

### httpx Best Practices

```python
import httpx

# Recommended configuration
client = httpx.Client(
    timeout=30.0,
    headers={"User-Agent": "DifyPlugin/1.0"}
)

# Error handling
try:
    response = client.get(url)
    response.raise_for_status()
except httpx.HTTPError as e:
    # Handle error
    pass
```
