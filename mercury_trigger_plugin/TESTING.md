# Mercury Trigger Plugin - Testing Guide

## Overview

This document describes how to test the Mercury Trigger Plugin with the mock Mercury server and Dify platform.

## Prerequisites

- Python 3.12+
- Access to Dify platform (dify.greeep.com)
- Mock Mercury Server running locally

## Quick Start

### 1. Start Mock Mercury Server

```bash
cd /home/ubuntu/playground/finance_plugins
python3 scripts/mock_mercury_server.py
```

Server will start on `http://localhost:8765` with:
- **API Token**: `mock_token_12345`

### 2. Run Tests

```bash
# Unit tests (15 tests)
.venv/bin/pytest mercury_trigger_plugin/tests/unit/ -v

# Integration tests (14 tests) - requires mock server running
.venv/bin/pytest mercury_trigger_plugin/tests/integration/ -v

# All tests
.venv/bin/pytest mercury_trigger_plugin/tests/ -v
```

## Mock Mercury Server API

### Mercury API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/accounts` | List all accounts |
| GET | `/api/v1/account/{id}` | Get account details |
| GET | `/api/v1/account/{id}/transactions` | Get account transactions |
| GET | `/api/v1/recipients` | List recipients |
| GET | `/api/v1/recipient/{id}` | Get recipient details |
| POST | `/api/v1/recipients` | Create recipient |
| GET | `/api/v1/categories` | List categories |
| GET | `/api/v1/webhooks` | List webhooks |
| POST | `/api/v1/webhooks` | Create webhook (returns secret) |
| GET | `/api/v1/webhook/{id}` | Get webhook details |
| DELETE | `/api/v1/webhook/{id}` | Delete webhook |

### Simulation Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/simulate/transaction` | Simulate transaction.created event |
| POST | `/simulate/transaction/update` | Simulate transaction.updated event |
| POST | `/simulate/custom` | Send custom webhook event |

### Utility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/status` | Server status and info |
| GET | `/webhooks/list` | List all webhooks (no auth) |
| POST | `/webhooks/clear` | Clear all webhooks |

## Testing Workflow

### Step 1: Create a Webhook

```bash
curl -X POST http://localhost:8765/api/v1/webhooks \
  -H "Authorization: Bearer mock_token_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "http://your-callback-url/webhook",
    "eventTypes": ["transaction.created", "transaction.updated"]
  }'
```

Response:
```json
{
  "id": "wh_xxxx",
  "url": "http://your-callback-url/webhook",
  "secret": "base64-encoded-secret",
  "status": "active",
  "eventTypes": ["transaction.created", "transaction.updated"]
}
```

### Step 2: Simulate Transaction Event

```bash
# Simulate transaction.created
curl -X POST http://localhost:8765/simulate/transaction \
  -H "Content-Type: application/json" \
  -d '{
    "amount": -500.00,
    "counterparty": "Test Vendor",
    "status": "pending"
  }'

# Simulate transaction.updated
curl -X POST http://localhost:8765/simulate/transaction/update \
  -H "Content-Type: application/json" \
  -d '{
    "amount": -500.00,
    "status": "sent"
  }'
```

### Step 3: View Registered Webhooks

```bash
curl http://localhost:8765/webhooks/list
```

## Remote Debugging with Dify

### Configuration

Create `.env` file in `mercury_trigger_plugin/`:

```env
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=dify.greeep.com
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=<your-debugging-key>
PLUGIN_DEBUG=true
```

### Get Debugging Key

1. Login to Dify console: https://dify.greeep.com
2. Go to **Plugins** page
3. Click **Debug** button to get the debugging key

### Start Plugin in Debug Mode

```bash
cd mercury_trigger_plugin
dify plugin run .
```

Or manually:
```bash
python3 -m dify_plugin
```

## Webhook Signature Validation

Mercury webhooks include a signature header for validation:

```
Mercury-Signature: t=1234567890,v1=sha256-signature
```

The signature is computed as:
```python
import hmac
import hashlib
import base64

# Decode base64 secret
secret_bytes = base64.b64decode(webhook_secret)

# Create signed payload
signed_payload = f"{timestamp}.{request_body}"

# Compute HMAC-SHA256
signature = hmac.new(
    secret_bytes,
    signed_payload.encode(),
    hashlib.sha256
).hexdigest()
```

## Trigger Event Variables

When a transaction event is received, the trigger outputs these variables:

| Variable | Type | Description |
|----------|------|-------------|
| `event_id` | string | Mercury event ID |
| `transaction_id` | string | Transaction ID |
| `operation_type` | string | "created" or "updated" |
| `account_id` | string | Mercury account ID |
| `amount` | number | Transaction amount (negative for debits) |
| `status` | string | Transaction status |
| `posted_at` | string | ISO timestamp |
| `counterparty_name` | string | Counterparty name |
| `bank_description` | string | Bank description |
| `note` | string | Transaction note |
| `category` | string | Mercury category |
| `transaction_type` | string | Transaction type |

## Troubleshooting

### Mock Server Not Starting
```bash
# Check if port 8765 is in use
lsof -i :8765

# Kill existing process
kill -9 <pid>
```

### Plugin Connection Issues
```bash
# Test port connectivity
nc -zv dify.greeep.com 5003

# Check plugin logs
tail -f /tmp/mercury_trigger.log
```

### Webhook Delivery Failures
```bash
# Check mock server output for delivery results
# The server logs all webhook deliveries with status
```

## Test Coverage

| Test Suite | Tests | Coverage |
|------------|-------|----------|
| Unit Tests | 15 | Trigger logic, signature validation, event parsing |
| Integration Tests | 14 | API endpoints, webhook lifecycle, event simulation |
| **Total** | **29** | Full plugin functionality |
