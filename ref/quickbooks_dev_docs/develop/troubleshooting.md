# Troubleshooting and Errors

> QuickBooks Online API - Error Handling Guide

Learn how to fix common problems for the QuickBooks Online Accounting API.

---

## Quick Reference

| Issue Type | Guide |
|------------|-------|
| API Status | [Check API statuses](https://developer.intuit.com/app/developer/qbo/docs/develop/troubleshooting/api-status) |
| Common API Errors | [Fix common errors](#common-api-errors) |
| Error Codes | [Error code reference](#error-codes) |
| OAuth 2.0 Issues | [Fix OAuth errors](#oauth-20-errors) |
| Subscription Status | [Subscription states](#subscription-states) |

---

## Common API Errors

### HTTP Status Codes

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 400 | Bad Request | Malformed request, invalid parameters |
| 401 | Unauthorized | Invalid or expired access token |
| 403 | Forbidden | App doesn't have permission for this scope |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Intuit server error |
| 503 | Service Unavailable | Service temporarily down |

### Common Error Patterns

| Error | Cause | Solution |
|-------|-------|----------|
| `AuthenticationFailed` | Invalid access token | Refresh the token |
| `InvalidGrantException` | Authorization code expired | Get new authorization code |
| `StaleObjectError` | Concurrent update conflict | Re-fetch and retry |
| `ValidationError` | Invalid field values | Check field requirements |
| `DuplicateEntityError` | Entity already exists | Query existing entity first |

---

## Error Codes

### Business Validation Errors (2000-2999)

| Code | Message | Description |
|------|---------|-------------|
| 2000 | Invalid Reference | Referenced entity doesn't exist |
| 2010 | Required Field Missing | A required field was not provided |
| 2020 | Invalid Field Format | Field value doesn't match expected format |
| 2030 | Duplicate Name | An entity with this name already exists |
| 2500 | Stale Object | Entity was modified by another request |

### Authorization Errors (3000-3999)

| Code | Message | Description |
|------|---------|-------------|
| 3000 | Authentication Failed | Invalid or expired token |
| 3100 | Permission Denied | App lacks required scope |
| 3200 | Company Unavailable | QuickBooks company is not accessible |

### System Errors (5000-5999)

| Code | Message | Description |
|------|---------|-------------|
| 5000 | Internal Error | Unexpected server error |
| 5010 | Service Unavailable | Service temporarily down |

---

## OAuth 2.0 Errors

### Authorization Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `access_denied` | User declined authorization | User must authorize again |
| `invalid_scope` | Invalid scope requested | Check app configuration |
| `invalid_request` | Missing required parameter | Review request parameters |
| `server_error` | Intuit server issue | Retry later |

### Token Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `invalid_grant` | Authorization code expired or used | Get new authorization code |
| `invalid_client` | Wrong client credentials | Check Client ID and Secret |
| `expired_token` | Access token expired | Use refresh token |
| `invalid_token` | Token is malformed | Re-authorize |

### Refresh Token Issues

| Scenario | Solution |
|----------|----------|
| Refresh token expired (100 days) | User must re-authorize |
| Multiple refresh attempts | Only one refresh at a time |
| Token already refreshed | Use the new token |

---

## Rate Limits

### API Throttling

| Limit Type | Value |
|------------|-------|
| Requests per minute (per app, per company) | 500 |
| Concurrent connections | 10 |

### Handling Rate Limits

```python
import time

def make_api_call_with_retry(func, max_retries=3):
    """Make API call with exponential backoff for rate limits."""
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt * 60  # 1, 2, 4 minutes
                time.sleep(wait_time)
            else:
                raise
```

---

## Subscription States

QuickBooks Online companies can have different subscription states:

| State | API Access | Description |
|-------|------------|-------------|
| `SUBSCRIBED` | Full access | Active subscription |
| `TRIAL` | Full access | Free trial period |
| `CANCELLED` | Read-only | Subscription cancelled |
| `SUSPENDED` | No access | Account suspended |
| `EXPIRED` | No access | Trial or subscription expired |

### Handling Subscription States

```python
def check_company_status(company_info):
    """Check if company is in a valid state for API operations."""
    status = company_info.get('subscriptionStatus')
    
    if status in ['SUBSCRIBED', 'TRIAL']:
        return True, "Full access"
    elif status == 'CANCELLED':
        return True, "Read-only access"
    else:
        return False, f"No access: {status}"
```

---

## Debugging Tips

### 1. Check Request Headers

Ensure all required headers are present:

```
Authorization: Bearer {access_token}
Accept: application/json
Content-Type: application/json
```

### 2. Validate Request Body

- Check JSON formatting
- Verify required fields
- Validate field types and formats

### 3. Use Intuit-RequestId

Add a unique request ID for tracking:

```
Intuit-RequestId: {unique-uuid}
```

### 4. Review Error Response

API errors include helpful details:

```json
{
  "Fault": {
    "Error": [
      {
        "Message": "Error description",
        "Detail": "Detailed error information",
        "code": "2020"
      }
    ],
    "type": "ValidationFault"
  }
}
```

### 5. Check API Status

Visit [Intuit Status Page](https://status.intuit.com/) for service health.

---

## Getting Help

1. **Developer Forum**: [developer.intuit.com/hub](https://developer.intuit.com/hub)
2. **Bug Tracker**: [Known Issues](https://help.developer.intuit.com/s/bug-tracker-page)
3. **Developer Support**: [Contact Support](https://help.developer.intuit.com/s/contactsupport)

---

## Related Documentation

- [OAuth 2.0 Setup](./authentication-and-authorization/oauth-2.0.md)
- [API Reference](../api-reference/README.md)
- [Sandbox Testing](./sandboxes.md)
