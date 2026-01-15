# Mercury API Documentation

> **Source**: Compiled from https://docs.mercury.com and search results (2025-12-26)

## Overview

Mercury offers a programmatic API for financial operations enabling access to accounts, transaction histories, and payment processing.

## Authentication

### OAuth 2.0 Flow

Mercury uses OAuth 2.0 with Authorization Code Grant Type and PKCE support.

**Prerequisites**: OAuth access requires prior approval from Mercury. This is intended for companies building integrations for Mercury customers.

**Key Endpoints**:
- Authorization URL: `https://app.mercury.com/oauth/authorize` (requires approval)
- Token URL: `https://oauth2.mercury.com/oauth2/token`

**Required Scopes**:
- `read:accounts` - Access account information
- `read:transactions` - Access transaction data
- `offline_access` - Obtain refresh tokens for persistent access

**Authentication Flow**:
1. Redirect user to Mercury authorization endpoint
2. User verifies identity and authorizes request
3. Mercury redirects back with authorization code
4. Exchange code for access token

**Token Usage**:
```
Authorization: Bearer <access_token>
```

**Important Notes**:
- Access tokens expire in 1 hour
- Refresh tokens can only be used once
- For persistent access, include `offline_access` scope

## Base URL

```
https://api.mercury.com/api/v1
```

## Core Endpoints

### Accounts

#### Get All Accounts
```
GET /api/v1/accounts
```

Returns all accounts associated with the authenticated user.

**Response Fields** (typical):
- `id` - Account ID
- `name` - Account name
- `type` - Account type (checking, savings, treasury)
- `status` - Account status
- `availableBalance` - Available balance
- `currentBalance` - Current balance
- `currency` - Currency code (USD)

---

### Transactions

#### Get Transactions for Account
```
GET /api/v1/account/:id/transactions
```

Returns transaction data for a specific account.

**Path Parameters**:
- `id` - Account ID

**Query Parameters** (typical):
- `postedAtStart` - Start date for filtering (ISO 8601)
- `postedAtEnd` - End date for filtering (ISO 8601)
- `limit` - Number of results (pagination)
- `offset` - Pagination offset

**Response Fields**:
- `id` / `transaction_id` - Unique transaction identifier
- `amount` - Transaction amount (negative for debits, positive for credits)
- `postedAt` / `date` - Transaction posting date
- `status` - Transaction status (pending, posted, etc.)
- `description` / `note` - Transaction description
- `counterpartyName` / `merchant` - Merchant/counterparty name
- `counterpartyAccountNumber` - Account number
- `counterpartyRoutingNumber` - Routing number
- `bankDescription` - Bank-provided description
- `category` - Transaction category (if set)
- `type` - Transaction type (debit, credit, wire, ach, etc.)
- `trackingNumber` - Optional tracking number (added 2025)

**Example Response**:
```json
{
  "transactions": [
    {
      "id": "txn_123abc",
      "amount": -150.00,
      "postedAt": "2025-12-19T10:30:00Z",
      "status": "posted",
      "counterpartyName": "Staples",
      "bankDescription": "DEBIT CARD PURCHASE - STAPLES",
      "category": "",
      "type": "debit"
    }
  ],
  "total": 1,
  "hasMore": false
}
```

#### Get Single Transaction
```
GET /api/v1/transactions/:transactionId
```

Retrieves a single transaction without requiring accountId.

**Path Parameters**:
- `transactionId` - Transaction ID

---

#### Update Transaction Metadata
```
PATCH /api/v1/transaction/:transactionId
```

Updates or clears notes/category attached to a transaction.

**Request Body**:
```json
{
  "note": "Office supplies for Q4",
  "category": "Office Expenses"
}
```

---

#### Create Transaction (Send Payment)
```
POST /api/v1/account/:id/transactions
```

Creates a new transaction to send money from an account.

**Required Headers**:
- `Idempotency-Key` - Unique identifier for the transaction

**Request Body** (typical):
```json
{
  "amount": 1000.00,
  "recipientId": "rec_xyz",
  "description": "Invoice payment",
  "idempotencyKey": "unique-key-123"
}
```

**Note**: Transaction may require approval depending on account settings.

---

### Attachments

#### Get Transaction Attachment
```
GET /api/v1/attachment/:attachmentId
```

Retrieves attachments (receipts, invoices) associated with transactions.

---

### Users

#### Get User by ID
```
GET /api/v1/user/:userId
```

Retrieves user information.

---

## API Features

### Versioning

Mercury supports multiple API versions:
- `v1` (current)
- `v1-prev1` (previous version)
- `v2` (beta/upcoming)

### Sandbox Environment

Mercury provides a sandbox environment for testing integrations. See official documentation for sandbox setup.

### Rate Limits

**Not officially documented in search results**. Typical financial APIs enforce:
- Rate limits per minute/hour
- 429 status codes when exceeded
- Exponential backoff recommended

Best practices:
- Implement exponential backoff for retries
- Cache data when possible
- Use polling intervals of 1-5 minutes for transaction monitoring

---

## Webhooks API

Mercury supports real-time webhooks for receiving notifications when resources change.

> **Note**: Webhooks are currently not available in the sandbox environment.

### Webhook Endpoints

#### Create Webhook
```
POST /api/v1/webhooks
```

**Request Body**:
```json
{
  "url": "https://your-endpoint.com/webhook",
  "eventTypes": ["transaction.created", "transaction.updated"],
  "filterPaths": ["status", "amount"]
}
```

**Parameters**:
- `url` (required): HTTPS URL where webhook events will be delivered
- `eventTypes` (optional): Array of event types to subscribe to. If omitted, receives all events
- `filterPaths` (optional): Array of field paths to filter by. Only sends webhooks when these fields change

**Response** (200):
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "url": "https://your-endpoint.com/webhook",
  "secret": "base64-encoded-secret",
  "status": "active",
  "eventTypes": ["transaction.created", "transaction.updated"],
  "filterPaths": ["status", "amount"],
  "createdAt": "2025-01-01T00:00:00Z",
  "updatedAt": "2025-01-01T00:00:00Z"
}
```

> **Important**: The `secret` is only returned on creation. Store it securely for signature verification.

#### Delete Webhook
```
DELETE /api/v1/webhooks/{id}
```

Returns `204 No Content` on success.

#### Get Webhooks
```
GET /api/v1/webhooks
GET /api/v1/webhooks/{id}
```

### Supported Event Types

- `transaction.created` - New transaction created
- `transaction.updated` - Existing transaction modified

### Webhook Payload Format

Webhooks follow the JSON Merge Patch standard (RFC 7396):

```json
{
  "id": "bfa85eaa-afab-11f0-8fea-17d650f2306e",
  "resourceType": "transaction",
  "resourceId": "1d3042b6-af63-11f0-89d2-3503f2fcfef7",
  "operationType": "update",
  "resourceVersion": 2,
  "occurredAt": "2025-01-01T00:00:00.000000Z",
  "changedPaths": ["status", "postedAt"],
  "mergePatch": {
    "postedAt": "2025-01-01T00:00:00.000000+00:00",
    "status": "sent"
  },
  "previousValues": {
    "postedAt": null,
    "status": "pending"
  }
}
```

### Signature Verification

Every webhook includes a `Mercury-Signature` header for verification.

**Header Format**: `t=<timestamp>,v1=<signature>`

**Verification Steps**:
1. Extract timestamp (`t`) and signature (`v1`) from header
2. Construct signed payload: `<timestamp>.<request_body>`
3. Compute HMAC-SHA256 using your webhook secret (base64 decoded)
4. Compare signatures using constant-time comparison

**Python Example**:
```python
import hmac
import hashlib
import base64

def verify_signature(request_body: str, header: str, secret: str) -> bool:
    parts = dict(p.split("=", 1) for p in header.split(","))
    timestamp = parts.get("t")
    signature = parts.get("v1")
    
    signed_payload = f"{timestamp}.{request_body}"
    secret_bytes = base64.b64decode(secret)
    
    expected = hmac.new(
        secret_bytes,
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected)
```

### Best Practices

- Respond with `2xx` within 5 seconds
- Mercury retries up to 10 times with exponential backoff (~1 day)
- Use event `id` for idempotency (at-least-once delivery)
- Use `eventTypes` and `filterPaths` to reduce noise

---

## Error Handling

**Expected HTTP Status Codes**:
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `401` - Unauthorized (invalid or expired token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error
- `503` - Service Unavailable

**Best Practices**:
- Implement retry logic with exponential backoff
- Handle 401 by refreshing OAuth token
- Handle 429 by respecting rate limits
- Log errors for debugging

---

## Data Normalization Example

When building integrations, normalize Mercury data:

```python
def normalize_transaction(raw_txn):
    """Normalize Mercury transaction to standard format"""
    return {
        "transaction_id": raw_txn.get("id"),
        "account_id": raw_txn.get("accountId"),
        "amount": raw_txn.get("amount"),
        "type": "debit" if raw_txn.get("amount", 0) < 0 else "credit",
        "date": raw_txn.get("postedAt", "").split("T")[0],
        "merchant": raw_txn.get("counterpartyName", ""),
        "description": raw_txn.get("bankDescription", ""),
        "category": raw_txn.get("category", ""),
        "status": raw_txn.get("status", ""),
        "counterparty": {
            "name": raw_txn.get("counterpartyName"),
            "account": raw_txn.get("counterpartyAccountNumber"),
            "routing": raw_txn.get("counterpartyRoutingNumber")
        }
    }
```

---

## Additional Resources

- **Official Documentation**: https://docs.mercury.com/reference/welcome-to-mercury-api
- **OAuth2 Guide**: https://docs.mercury.com/docs/integrations-with-oauth2
- **Changelog**: https://docs.mercury.com/changelog
- **Support**: [email protected]
- **Developer Portal**: https://mercury.com/api

---

## Notes for Plugin Development

### For Dify Trigger Plugin:

1. **Polling Implementation**:
   - Poll every 60-300 seconds (1-5 minutes)
   - Use `postedAtStart` with last check timestamp
   - Store state using `self.get_state()` and `self.set_state()`

2. **OAuth Integration**:
   - Dify v1.7.0+ handles refresh tokens automatically
   - Configure OAuth provider in `provider/mercury.yaml`
   - Define scopes: `read:accounts`, `read:transactions`, `offline_access`

3. **Event Structure**:
   - Event name: `transaction.created`
   - Payload: Normalized transaction object
   - Emit event for each new transaction found

4. **Error Handling**:
   - Retry on 429 with exponential backoff
   - Refresh token on 401
   - Log errors and continue polling
   - Don't crash on network failures

---

*Last Updated: 2025-12-26*
*Note: Some endpoint details may require Mercury API approval to access complete documentation*
