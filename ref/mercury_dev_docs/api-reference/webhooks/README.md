# Webhooks API

Base URL: `https://api.mercury.com/api/v1`

Webhooks allow you to receive real-time HTTP notifications when resources in your Mercury account change (e.g., transaction updates) instead of polling the API.

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/webhooks` | Get all webhook endpoints |
| GET | `/webhook/{webhookId}` | Get webhook endpoint by ID |
| POST | `/webhooks` | Create a new webhook endpoint |
| POST | `/webhook/{webhookId}` | Update webhook endpoint |
| POST | `/webhook/{webhookId}/verify` | Verify webhook endpoint |
| DELETE | `/webhook/{webhookId}` | Delete webhook endpoint |

---

## Webhook Events

Mercury webhooks support the following event types:

| Event | Description |
|-------|-------------|
| `transaction.created` | New transaction created |
| `transaction.updated` | Transaction status or details changed |
| `transaction.deleted` | Transaction was deleted/cancelled |

Webhook payloads use the same event structure as the [Events API](../events/) and follow the JSON Merge Patch standard.

---

## GET /webhooks

Get all webhook endpoints for your organization.

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/webhooks" \
  -H "Authorization: Bearer <token>"
```

### Response

```json
{
  "webhooks": [
    {
      "id": "webhook_123",
      "url": "https://your-server.com/webhook",
      "events": ["transaction.created", "transaction.updated"],
      "status": "active",
      "secret": "whsec_...",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique webhook ID |
| url | string | Endpoint URL |
| events | array | Subscribed event types |
| status | string | `active`, `inactive`, `pending_verification` |
| secret | string | Signing secret for verification |
| createdAt | string | ISO 8601 timestamp |

---

## GET /webhook/{webhookId}

Get details for a specific webhook endpoint.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| webhookId | string | Yes | Webhook ID |

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/webhook/{webhookId}" \
  -H "Authorization: Bearer <token>"
```

---

## POST /webhooks

Create a new webhook endpoint.

### Request Body

```json
{
  "url": "https://your-server.com/webhook",
  "events": ["transaction.created", "transaction.updated"]
}
```

### Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| url | string | Yes | HTTPS endpoint URL |
| events | array | Yes | Event types to subscribe |

### Request

```bash
curl -X POST "https://api.mercury.com/api/v1/webhooks" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.com/webhook",
    "events": ["transaction.created", "transaction.updated"]
  }'
```

### Response

```json
{
  "id": "webhook_123",
  "url": "https://your-server.com/webhook",
  "events": ["transaction.created", "transaction.updated"],
  "status": "pending_verification",
  "secret": "whsec_abc123...",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

### Notes

- URL must use HTTPS
- Save the `secret` - it's only shown once
- Webhook starts in `pending_verification` status

---

## POST /webhook/{webhookId}

Update an existing webhook endpoint.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| webhookId | string | Yes | Webhook ID |

### Request Body

```json
{
  "url": "https://your-server.com/new-webhook",
  "events": ["transaction.created"]
}
```

---

## POST /webhook/{webhookId}/verify

Verify a webhook endpoint. Mercury will send a test event to confirm the endpoint is reachable.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| webhookId | string | Yes | Webhook ID |

### Request

```bash
curl -X POST "https://api.mercury.com/api/v1/webhook/{webhookId}/verify" \
  -H "Authorization: Bearer <token>"
```

---

## DELETE /webhook/{webhookId}

Delete a webhook endpoint.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| webhookId | string | Yes | Webhook ID |

### Request

```bash
curl -X DELETE "https://api.mercury.com/api/v1/webhook/{webhookId}" \
  -H "Authorization: Bearer <token>"
```

---

## Webhook Payload Format

When an event occurs, Mercury sends a POST request to your endpoint:

### Headers

```http
Content-Type: application/json
X-Mercury-Signature: sha256=abc123...
X-Mercury-Timestamp: 1705320600
X-Mercury-Webhook-Id: webhook_123
X-Mercury-Event-Id: evt_456
```

### Body

```json
{
  "id": "evt_456",
  "type": "transaction.created",
  "createdAt": "2024-01-15T10:30:00Z",
  "data": {
    "id": "txn_789",
    "accountId": "account_123",
    "amount": -1500.00,
    "status": "pending",
    "counterpartyName": "Acme Corp"
  }
}
```

---

## Verifying Webhook Signatures

Always verify webhook signatures to ensure requests come from Mercury.

### Python Example

```python
import hmac
import hashlib

def verify_webhook(payload: bytes, signature: str, timestamp: str, secret: str) -> bool:
    # Construct signed payload
    signed_payload = f"{timestamp}.{payload.decode()}"
    
    # Calculate expected signature
    expected = hmac.new(
        secret.encode(),
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures
    expected_signature = f"sha256={expected}"
    return hmac.compare_digest(signature, expected_signature)
```

### Best Practices

1. **Always verify signatures** - Reject requests with invalid signatures
2. **Check timestamps** - Reject requests older than 5 minutes
3. **Respond quickly** - Return 2xx within 30 seconds
4. **Handle retries** - Mercury retries failed deliveries with exponential backoff
5. **Idempotency** - Handle duplicate events gracefully using event ID

---

## Retry Policy

If your endpoint doesn't respond with a 2xx status:

| Attempt | Delay |
|---------|-------|
| 1 | Immediate |
| 2 | 1 minute |
| 3 | 5 minutes |
| 4 | 30 minutes |
| 5 | 2 hours |
| 6 | 12 hours |
| 7 | 24 hours |

After 7 failed attempts, the webhook is marked as failed and requires manual re-verification.
