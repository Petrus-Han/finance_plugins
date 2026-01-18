# Webhooks

> QuickBooks Online API - Webhooks Implementation Guide

Use webhooks to receive event-triggered callbacks for entities that your app needs to stay on top of. Webhooks automatically notify you whenever data changes in your end-user's QuickBooks Online company files.

**Key Points:**
- Webhooks apply to all QuickBooks Online companies connected to your app
- You need to configure an endpoint for our servers to call when data changes
- Once active, webhooks send requested event data, changes, and notifications

---

## Step 1: Set Up OAuth 2.0

If you haven't already, [set up OAuth 2.0](./authentication-and-authorization/oauth-2.0.md) for your app.

Even if webhooks are active, you'll only receive change notifications for QuickBooks Online companies that are connected and authorized via OAuth 2.0.

> **Tip**: If testing webhooks for [sandbox environments](./sandboxes.md), the QuickBooks Online companies you test with need to complete the authentication flow via OAuth 2.0.

---

## Step 2: See Example Implementations

**Example webhook implementations:**
- [Java](https://github.com/intuitdeveloper/sampleapp-webhooks-java)
- [Node.js](https://github.com/IntuitDeveloper/SampleApp-WebhookNotifications-nodejs)

---

## Step 3: Review Supported API Entities

Webhooks support notifications for the following entities and operations:

| Entity | Create | Update | Delete | Merge |
|--------|--------|--------|--------|-------|
| Account | Yes | Yes | Yes | No |
| Bill | Yes | Yes | Yes | No |
| BillPayment | Yes | Yes | Yes | No |
| Budget | Yes | Yes | Yes | No |
| Class | Yes | Yes | Yes | No |
| CreditMemo | Yes | Yes | Yes | No |
| Currency | Yes | Yes | No | No |
| Customer | Yes | Yes | Yes | Yes |
| Department | Yes | Yes | Yes | No |
| Deposit | Yes | Yes | Yes | No |
| Employee | Yes | Yes | Yes | No |
| Estimate | Yes | Yes | Yes | No |
| Invoice | Yes | Yes | Yes | No |
| Item | Yes | Yes | Yes | No |
| JournalEntry | Yes | Yes | Yes | No |
| Payment | Yes | Yes | Yes | No |
| PaymentMethod | Yes | Yes | Yes | No |
| Preferences | No | Yes | No | No |
| Purchase | Yes | Yes | Yes | No |
| PurchaseOrder | Yes | Yes | Yes | No |
| RefundReceipt | Yes | Yes | Yes | No |
| SalesReceipt | Yes | Yes | Yes | No |
| Term | Yes | Yes | Yes | No |
| TimeActivity | Yes | Yes | Yes | No |
| Transfer | Yes | Yes | Yes | No |
| Vendor | Yes | Yes | Yes | Yes |
| VendorCredit | Yes | Yes | Yes | No |

---

## Step 4: Configure Webhook Endpoints for an App

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
2. Select **My Hub > App dashboard** from the upper-right corner of the toolbar.
3. Select and open the app you want to subscribe.

**Note**: There are two sets of webhooks - one for production apps and a separate set for sandbox/testing environments. Set up webhooks separately for each.

### For Live, In-Production Apps

1. From the left navigation pane, select **Webhooks**.
2. Select **Production**.
3. Enter the **Endpoint URL** (where the server will send notifications).
4. Select the **Show webhooks** dropdown.
5. Review the events and operations.
6. Select the notifications and actions you want to enable.
7. Select **Save**.

### For Sandbox and Developer Environments

1. From the left navigation pane, select **Webhooks**.
2. Select **Development**.
3. Enter the **Endpoint URL** (where the server will send notifications).
4. Select the **Show webhooks** dropdown.
5. Review the events and operations.
6. Select the notifications and actions you want to enable.
7. Select **Save**.

> **Tip**: It may take up to five minutes to get your first webhook notification.

---

## Step 5: Validate Webhook Notifications

After you configure webhook endpoints, Intuit provides an app-specific **verifier token**. Use verifier tokens to validate that webhook notifications are from Intuit.

### To See Verifier Tokens

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
2. Select **My Hub > App dashboard** from the upper-right corner of the toolbar.
3. Select and open the app you want to verify.
4. From the left navigation pane, select **Webhooks**.
5. Select **Development** or **Production**.
6. Review the **Verifier Token** field.

### To Use Verifier Tokens

1. Hash the notification payload with **HMAC_SHA256_ALGORITHM** using the `<verifier token>` value as the key.
2. Compare the payload hash value with the `intuit-signature` header from the notification. The values should be identical.

### Sample Header

```
content-length:262
intuit-created-time:2016-02-02T16:25:00-0800
intuit-t-id:9cf50b60-8b0e-4fea-8327-e6a66099fe6f
proxy-connection:keep-alive
host:sample-endpoint.ilb.idg-notify-ppd.a.intuit.com:8443
intuit-notification-schema-version:0.1
content-type:application/json; charset=utf-8
intuit-signature:6kQBQtjwjupelRMwkyJsnpq80uhz2o+Rn92+m03GhKE=
accept:application/json
user-agent:intuit_notification_server/0.1
```

### Python Signature Verification Example

```python
import hmac
import hashlib
import base64

def verify_webhook_signature(payload: str, signature: str, verifier_token: str) -> bool:
    """
    Verify that a webhook notification is from Intuit.
    
    Args:
        payload: The raw JSON payload as a string
        signature: The intuit-signature header value
        verifier_token: Your app's verifier token
    
    Returns:
        True if the signature is valid, False otherwise
    """
    # Create HMAC-SHA256 hash of the payload
    hash_obj = hmac.new(
        verifier_token.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    )
    
    # Base64 encode the hash
    computed_signature = base64.b64encode(hash_obj.digest()).decode('utf-8')
    
    # Compare with the provided signature
    return hmac.compare_digest(computed_signature, signature)
```

### Java Signature Verification Example

```java
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;
import java.util.Map;

public class VerifySignatureExample {
    private static final String SIGNATURE = "intuit-signature";
    private static final String ALGORITHM = "HmacSHA256";
    
    public boolean isRequestValid(Map<String, String> headers, String payload, String verifier) {
        String signature = headers.get(SIGNATURE);
        if (signature == null) {
            return false;
        }
        try {
            SecretKeySpec secretKey = new SecretKeySpec(verifier.getBytes("UTF-8"), ALGORITHM);
            Mac mac = Mac.getInstance(ALGORITHM);
            mac.init(secretKey);
            String hash = Base64.getEncoder().encodeToString(mac.doFinal(payload.getBytes()));
            return hash.equals(signature);
        } catch (Exception e) {
            return false;
        }
    }
}
```

---

## Step 6: Review Webhook Notifications

Webhook notifications are POSTs with a JSON body.

### Response Fields

| Field | Description |
|-------|-------------|
| `name` | The name of the entity that changed (Customer, Invoice, etc.) |
| `id` | The ID of the changed entity |
| `operation` | The type of change (Create, Update, Delete, Merge) |
| `lastUpdated` | The latest timestamp in UTC |
| `deletedID` | The ID of the deleted or merged entity (only for merge events) |

### Example Webhook Payload

```json
{
  "eventNotifications": [
    {
      "realmId": "1185883450",
      "dataChangeEvent": {
        "entities": [
          {
            "name": "Customer",
            "id": "1",
            "operation": "Create",
            "lastUpdated": "2015-10-05T14:42:19-0700"
          },
          {
            "name": "Vendor",
            "id": "1",
            "operation": "Create",
            "lastUpdated": "2015-10-05T14:42:19-0700"
          }
        ]
      }
    }
  ]
}
```

### Understanding the Payload Structure

- **eventNotifications**: Array of individual event notifications
- Each event notification corresponds to a unique **realm ID** (company)
- Each realm ID can include **multiple entities** representing various types of data changes
- If your app is connected to multiple companies, you receive an array with updates for each company

> **Tip**: There are no Intuit-imposed limits to payload size or number of events. Individual server architectures may impose their own limits (2MB is a common default size limit).

---

## Webhook Best Practices

### Reliability

To compensate for the possibility of missed events:
- Make a **ChangeDataCapture (CDC)** call for all required entities, dating back to the last known successfully processed webhook event for each entity
- Make a **daily CDC call** for all required entities to ensure your app has always processed the most up-to-date data

### Respond Promptly

**CRITICAL**: Your endpoint must respond within **3 seconds**, or the transaction will time out and retry.

**Recommendations:**
- Don't process the notification payload within the webhooks endpoint implementation
- Don't perform complex operations in the endpoint handler
- Do the processing on a **separate thread asynchronously** using a queue
- Respond with HTTP 200 immediately, then process

### Manage Concurrency

- Event notifications are sent **one realm ID at a time**
- When there are multiple rapid changes, your app may get frequent notifications
- Process the queue **linearly** to avoid processing the same changes more than once

### Notification Ordering

- It's possible to receive events **out of sequence**
- The `lastUpdated` (timestamp) field in the notification payload is always the **source of truth** for when events occur

### Retry Policy

| Scenario | Behavior |
|----------|----------|
| Endpoint down | Retry at intervals of 20, 30, and 50 minutes |
| Still down after retries | Drop message and blacklist endpoint |
| Endpoint inactive | After one day |
| Retry triggered for | Status codes: 500, 502, 503, 504, 408 |

---

## Python Webhook Handler Example

```python
from flask import Flask, request, jsonify
import hmac
import hashlib
import base64
import threading
import queue

app = Flask(__name__)
notification_queue = queue.Queue()

VERIFIER_TOKEN = "your_verifier_token"

def verify_signature(payload: str, signature: str) -> bool:
    hash_obj = hmac.new(
        VERIFIER_TOKEN.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    )
    computed_signature = base64.b64encode(hash_obj.digest()).decode('utf-8')
    return hmac.compare_digest(computed_signature, signature)

def process_notifications():
    """Background worker to process notifications"""
    while True:
        notification = notification_queue.get()
        try:
            for event in notification.get('eventNotifications', []):
                realm_id = event.get('realmId')
                for entity in event.get('dataChangeEvent', {}).get('entities', []):
                    # Process each entity change
                    print(f"Processing {entity['operation']} on {entity['name']} (ID: {entity['id']}) for realm {realm_id}")
                    # Add your processing logic here
        except Exception as e:
            print(f"Error processing notification: {e}")
        finally:
            notification_queue.task_done()

# Start background worker
worker_thread = threading.Thread(target=process_notifications, daemon=True)
worker_thread.start()

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    # Verify signature
    signature = request.headers.get('intuit-signature')
    if not signature or not verify_signature(request.data.decode('utf-8'), signature):
        return jsonify({'error': 'Invalid signature'}), 401
    
    # Queue for async processing
    notification_queue.put(request.json)
    
    # Respond immediately
    return jsonify({'status': 'received'}), 200
```

---

## Related Documentation

- [OAuth 2.0 Setup](./authentication-and-authorization/oauth-2.0.md)
- [Sandbox Testing](./sandboxes.md)
- [API Reference](../api-reference/README.md)
- [Troubleshooting](./troubleshooting.md)
