# Mercury Webhook Debugging Scripts

Scripts for testing and debugging the mercury_trigger_plugin webhook flow.

## Quick Start

```bash
# Terminal 1: Start Mock Mercury Server
python scripts/mock_mercury_server.py

# Terminal 2: Start Webhook Receiver
python scripts/webhook_receiver.py

# Terminal 3: Run automated tests
python scripts/test_webhook_flow.py -v
```

## Scripts Overview

### 1. mock_mercury_server.py

**Complete Mercury API simulator** that implements all webhook-related endpoints.

**Port**: 8765 (configurable via `MOCK_MERCURY_PORT`)
**Token**: `mock_token_12345` (configurable via `MOCK_MERCURY_TOKEN`)

**Mercury API Endpoints**:
- `GET /api/v1/accounts` - List mock accounts
- `GET /api/v1/webhooks` - List registered webhooks
- `POST /api/v1/webhooks` - Create webhook (returns secret!)
- `GET /api/v1/webhooks/{id}` - Get webhook details
- `DELETE /api/v1/webhooks/{id}` - Delete webhook

**Simulation Endpoints**:
- `POST /simulate/transaction` - Simulate `transaction.created` event
- `POST /simulate/transaction/update` - Simulate `transaction.updated` event
- `POST /simulate/custom` - Send custom event payload

**Usage**:
```bash
# Start server
python scripts/mock_mercury_server.py

# Register a webhook (like Dify plugin does)
curl -X POST http://localhost:8765/api/v1/webhooks \
  -H "Authorization: Bearer mock_token_12345" \
  -H "Content-Type: application/json" \
  -d '{"url": "http://localhost:8766/webhook", "eventTypes": ["transaction.created"]}'

# Trigger an event
curl -X POST http://localhost:8765/simulate/transaction

# Trigger with custom data
curl -X POST http://localhost:8765/simulate/transaction \
  -H "Content-Type: application/json" \
  -d '{"amount": -500.00, "counterparty": "Amazon"}'
```

### 2. webhook_receiver.py

**Webhook receiver** that simulates Dify's webhook endpoint and validates signatures.

**Port**: 8766 (configurable via `WEBHOOK_PORT`)

**Endpoints**:
- `POST /*` - Receive any webhook (will be logged)
- `GET /` - Status page
- `GET /webhooks` - List all received webhooks
- `GET /clear` - Clear webhook history

**Usage**:
```bash
# Start without signature validation
python scripts/webhook_receiver.py

# Start with signature validation (get secret from webhook creation response)
WEBHOOK_SECRET="your_base64_secret" python scripts/webhook_receiver.py
```

### 3. test_webhook_flow.py

**Automated end-to-end test** that verifies the complete webhook flow.

**Usage**:
```bash
# Run tests (requires both servers running)
python scripts/test_webhook_flow.py

# Verbose output
python scripts/test_webhook_flow.py -v

# Keep servers running after test
python scripts/test_webhook_flow.py --keep-alive
```

### 4. diagnose_mercury_webhook.py

**Production Mercury API diagnostic tool** for checking real webhooks.

**Usage**:
```bash
# Set your production API token
export MERCURY_API_TOKEN="your_production_token"

# Run diagnostics
python scripts/diagnose_mercury_webhook.py

# Create test webhook (use webhook.site for testing)
python scripts/diagnose_mercury_webhook.py --create-test "https://webhook.site/xxx"

# Delete a webhook
python scripts/diagnose_mercury_webhook.py --delete "webhook_id"
```

## Testing the Plugin Locally

### Step 1: Start the mock environment

```bash
# Terminal 1
python scripts/mock_mercury_server.py

# Terminal 2
python scripts/webhook_receiver.py
```

### Step 2: Configure the plugin to use mock server

In your plugin's environment or Dify configuration:

```
API_ENVIRONMENT=sandbox  (or any value, the mock server accepts any)
API_TOKEN=mock_token_12345
API_BASE_URL=http://localhost:8765/api/v1  (if configurable)
```

### Step 3: Create a trigger subscription

The plugin will call `POST /api/v1/webhooks` to register. You'll see output in the mock server console.

### Step 4: Simulate events

```bash
# Send transaction.created event
curl -X POST http://localhost:8765/simulate/transaction

# Send transaction.updated event
curl -X POST http://localhost:8765/simulate/transaction/update
```

### Step 5: Verify in receiver

Check the webhook_receiver console for received events and signature validation results.

## Webhook Signature Format

Mercury uses HMAC-SHA256 with the following format:

**Header**: `Mercury-Signature: t={timestamp},v1={signature}`

**Signature calculation**:
```python
import base64
import hmac
import hashlib

# Secret is base64-encoded
secret_bytes = base64.b64decode(webhook_secret)

# Signed payload is: "{timestamp}.{json_body}"
signed_payload = f"{timestamp}.{body}"

# Calculate signature
signature = hmac.new(
    secret_bytes,
    signed_payload.encode(),
    hashlib.sha256
).hexdigest()
```

## Debugging Tips

### Webhook not received?

1. Check if webhook is registered: `curl http://localhost:8765/webhooks/list`
2. Check if URL is correct and accessible
3. Check mock server console for delivery errors

### Signature validation failed?

1. Ensure the webhook receiver has the correct secret
2. Check that the body hasn't been modified (no extra whitespace)
3. Verify timestamp is recent (within allowed window)

### Event not triggering workflow?

1. Check event type filter (`transaction.created` vs `transaction.updated`)
2. Check plugin logs for errors
3. Verify the workflow is configured to trigger on the event

## File Structure

```
scripts/
├── README.md                    # This file
├── mock_mercury_server.py       # Mercury API simulator
├── webhook_receiver.py          # Webhook receiver for testing
├── test_webhook_flow.py         # Automated e2e tests
└── diagnose_mercury_webhook.py  # Production diagnostic tool
```
