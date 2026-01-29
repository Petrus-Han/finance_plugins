# QuickBooks OAuth Token Refresh Analysis

## Problem Description

QuickBooks refresh token becomes invalid after a few hours with error:
```
"error":"invalid_grant","error_description":"Incorrect or invalid refresh token"
```

## OAuth Token Lifecycle

### QuickBooks Token Specifications

| Token Type | Validity | Notes |
|------------|----------|-------|
| Access Token | 1 hour (3600s) | Used for API calls |
| Refresh Token | 100 days | **Rotates on each refresh** |

**Critical**: QuickBooks implements **refresh token rotation** - each time you use a refresh token, the old one is invalidated and a new one is returned.

## Dify OAuth Refresh Mechanism

### Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Dify OAuth Refresh Flow                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. Tool Invocation                                                         │
│     └── tool_manager.py:get_builtin_tool()                                  │
│                                                                             │
│  2. Check Token Expiration (line 272)                                       │
│     └── if expires_at - 60 < current_time:                                  │
│         ├── Call plugin._oauth_refresh_credentials()                        │
│         └── Save new credentials to database                                │
│                                                                             │
│  3. Plugin Refresh (quickbooks.py:_oauth_refresh_credentials)               │
│     ├── POST to QuickBooks token endpoint                                   │
│     ├── Get new access_token + refresh_token                                │
│     └── Return ToolOAuthCredentials(credentials, expires_at)                │
│                                                                             │
│  4. Dify Saves Credentials (line 295-299)                                   │
│     ├── Encrypt new credentials                                             │
│     ├── Update database: encrypted_credentials, expires_at                  │
│     └── db.session.commit()                                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Code Locations

**Dify Backend** (`/home/ubuntu/playground/dify/api`):
- `core/tools/tool_manager.py:272-300` - Token expiration check and refresh
- `core/plugin/impl/oauth.py:87-120` - OAuth handler calling plugin

**QuickBooks Plugin** (`quickbooks_plugin/provider/quickbooks.py`):
- `_oauth_refresh_credentials():111-179` - Refresh implementation

## Root Cause Analysis

### Potential Issue: Refresh Token Not Being Saved

Looking at the plugin code (line 149):
```python
new_refresh_token = response_json.get("refresh_token", refresh_token)
```

If QuickBooks returns a response **without** `refresh_token` field, the old token is reused. But since QuickBooks already invalidated the old token, the next refresh will fail.

### QuickBooks API Behavior

According to QuickBooks OAuth documentation:
1. When you refresh, QuickBooks **always** returns a new refresh_token
2. The old refresh_token is immediately invalidated
3. If the new refresh_token is not saved, subsequent refreshes fail

### Debugging Steps

1. **Check QuickBooks API Response**: Add logging to see what QuickBooks actually returns:
```python
def _oauth_refresh_credentials(self, ...):
    ...
    response_json = response.json()
    logger.info(f"QuickBooks refresh response keys: {response_json.keys()}")
    logger.info(f"Has refresh_token: {'refresh_token' in response_json}")
```

2. **Check Database Storage**: Verify the credentials are being saved:
```sql
SELECT id, provider, expires_at,
       LENGTH(encrypted_credentials) as cred_length,
       updated_at
FROM tool_builtin_providers
WHERE provider LIKE '%quickbooks%';
```

3. **Check Dify Logs**: Look for refresh errors in Dify API logs.

## Proposed Fix

### Fix 1: Add Logging for Debugging

Add temporary logging to understand the issue:

```python
# In quickbooks.py _oauth_refresh_credentials
import logging
logger = logging.getLogger(__name__)

def _oauth_refresh_credentials(self, ...):
    ...
    response_json = response.json()

    # Debug logging (remove after fixing)
    logger.warning(f"[QBO_REFRESH] Response keys: {list(response_json.keys())}")
    logger.warning(f"[QBO_REFRESH] Has new refresh_token: {'refresh_token' in response_json}")

    access_token = response_json.get("access_token")
    new_refresh_token = response_json.get("refresh_token")

    if not new_refresh_token:
        logger.error("[QBO_REFRESH] No new refresh_token in response!")
        # Fallback to old token (will likely fail next time)
        new_refresh_token = refresh_token
    else:
        logger.warning(f"[QBO_REFRESH] Got new refresh_token: {new_refresh_token[:10]}...")
```

### Fix 2: Validate Refresh Token in Response

Ensure we always get a new refresh token:

```python
def _oauth_refresh_credentials(self, ...):
    ...
    response_json = response.json()

    access_token = response_json.get("access_token")
    new_refresh_token = response_json.get("refresh_token")

    if not access_token:
        raise ToolProviderOAuthError(f"No access_token in response: {response_json}")

    if not new_refresh_token:
        raise ToolProviderOAuthError(
            "QuickBooks did not return a new refresh_token. "
            "This is unexpected - please re-authorize the connection."
        )

    # ... rest of the code
```

### Fix 3: Add Refresh Token Expiration Tracking (Long-term)

QuickBooks refresh tokens expire after 100 days. Consider tracking this:

```python
# Calculate refresh token expiration (100 days from now)
REFRESH_TOKEN_VALIDITY_DAYS = 100
refresh_token_expires_at = int(time.time()) + (REFRESH_TOKEN_VALIDITY_DAYS * 24 * 60 * 60)

new_credentials = {
    "access_token": access_token,
    "refresh_token": new_refresh_token,
    "refresh_token_expires_at": refresh_token_expires_at,  # Track this
}
```

## Testing the Fix

1. Re-authorize QuickBooks connection
2. Wait for access token to expire (1 hour) or manually trigger refresh
3. Check logs to see if new refresh_token is received
4. Verify database has updated credentials
5. Wait for another expiration cycle and verify it still works

## References

- [QuickBooks OAuth 2.0 Documentation](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0)
- [QuickBooks Token Refresh](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0#refresh-the-access-token)
- Dify Plugin Daemon: `/home/ubuntu/playground/dify-plugin-daemon`
- Dify API: `/home/ubuntu/playground/dify/api`
