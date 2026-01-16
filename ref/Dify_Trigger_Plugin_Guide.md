# Dify Trigger Plugin Development Guide

> **Source**: Official Dify Documentation (2025-12-26)
> **Minimum Requirements**: Dify v1.10.0+, SDK ≥ 0.6.0

## Overview

Trigger plugins convert third-party events into formats Dify can process. Introduced in **Dify v1.10.0**, they function as webhook-based or polling-based start nodes that automatically trigger workflows when events occur.

**Key Use Cases**:
- Webhook integrations (GitHub, Stripe, etc.)
- **Polling integrations** (APIs without webhook support like Mercury)
- Real-time event processing
- Automated workflow activation

---

## Core Concepts

### Subscription
The configuration process that registers Dify's webhook address (or polling schedule) on a third-party platform. For polling-based plugins, this stores the polling configuration.

### Event
Individual event types (e.g., "transaction.created", "email.received") that trigger workflows.

### Event Dispatch
The mechanism that validates incoming webhooks or poll results, extracts event types, and routes them to the appropriate event handler.

---

## Plugin Structure

```
trigger-plugin/
├── _assets/
│   └── icon.svg
├── events/
│   └── [event_name]/
│       ├── [event_name].py      # Event handler implementation
│       └── [event_name].yaml    # Event schema definition
├── main.py                       # Entry point (optional)
├── manifest.yaml                 # Plugin metadata
├── provider/
│   ├── [provider_name].py       # Trigger implementation
│   └── [provider_name].yaml     # Provider schema
├── README.md
├── PRIVACY.md
└── requirements.txt
```

---

## Manifest Configuration

**File**: `manifest.yaml`

```yaml
version: 0.0.1
type: plugin
author: your_name
name: mercury-trigger
label:
  en_US: Mercury Banking Events
  zh_Hans: Mercury 银行事件
icon: _assets/icon.svg

meta:
  version: 0.0.1
  minimum_dify_version: 1.10.0    # Required for triggers
  arch:
    - amd64
    - arm64

resource:
  memory: 134217728                # 128MB
  permission:
    storage:
      enabled: true                # Enable for polling state
      size: 10485760              # 10MB

plugins:
  triggers:
    - provider: mercury            # Provider name
```

**Important Fields**:
- `minimum_dify_version`: Must be >= 1.10.0
- `permission.storage.enabled`: Set to `true` for state management (polling)
- `plugins.triggers`: List of trigger providers

---

## Provider Configuration

**File**: `provider/[provider_name].yaml`

### Basic Structure (Webhook Pattern)

```yaml
identity:
  author: your_name
  name: mercury
  label:
    en_US: Mercury Banking
    zh_Hans: Mercury 银行
  description:
    en_US: Mercury banking transaction events
  icon: icon.svg

subscription_schema:
  - name: webhook_secret
    type: secret-input
    required: false
    label:
      en_US: Webhook Secret
      zh_Hans: Webhook 密钥
    help:
      en_US: Optional secret for webhook validation
```

### With OAuth Authentication

```yaml
identity:
  # ... same as above

subscription_schema:
  - name: account_id
    type: string
    required: false
    label:
      en_US: Account ID
    placeholder:
      en_US: Leave empty to monitor all accounts

subscription_constructor:
  # OAuth Client Setup
  client_schema:
    - name: client_id
      type: secret-input
      required: true
      label:
        en_US: OAuth Client ID
      url: https://docs.mercury.com/docs/integrations-with-oauth2
    - name: client_secret
      type: secret-input
      required: true
      label:
        en_US: OAuth Client Secret

  # OAuth User Credentials
  oauth_schema:
    credentials_schema:
      - name: access_token
        type: secret-input
      - name: refresh_token
        type: secret-input
      - name: expires_at
        type: secret-input

  # Subscription Parameters
  parameters:
    - name: account_id
      type: string
      required: false
    - name: polling_interval
      type: number
      required: false
      default: 60
      label:
        en_US: Polling Interval (seconds)
      help:
        en_US: Minimum 30 seconds
```

---

## Provider Implementation

**File**: `provider/[provider_name].py`

### Webhook Pattern Implementation

```python
from dify_plugin.interfaces.trigger import Trigger, EventDispatch, Subscription
from dify_plugin.entities.trigger import TriggerValidationError
from werkzeug import Request, Response
import hmac
import hashlib

class MercuryTrigger(Trigger):
    """
    Mercury webhook trigger implementation
    """

    def _dispatch_event(self,
                       subscription: Subscription,
                       request: Request) -> EventDispatch:
        """
        Validate webhook and dispatch events

        Args:
            subscription: Subscription configuration
            request: Incoming webhook request

        Returns:
            EventDispatch with events list and HTTP response
        """
        # 1. Validate webhook signature
        webhook_secret = subscription.properties.get("webhook_secret")
        if webhook_secret:
            self._validate_signature(request, webhook_secret)

        # 2. Parse webhook payload
        payload = request.get_json()

        # 3. Extract event type from payload or headers
        event_type = payload.get("event_type") or \
                    request.headers.get("X-Mercury-Event")

        # 4. Return EventDispatch
        response = Response(
            response='{"status": "ok"}',
            status=200,
            mimetype="application/json"
        )

        return EventDispatch(
            events=[event_type],  # List of event names to trigger
            response=response
        )

    def _validate_signature(self, request: Request, webhook_secret: str):
        """Validate HMAC signature (GitHub pattern)"""
        signature = request.headers.get("X-Mercury-Signature-256")
        if not signature:
            raise TriggerValidationError("Missing signature")

        body = request.get_data()
        expected = "sha256=" + hmac.new(
            webhook_secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected):
            raise TriggerValidationError("Invalid signature")
```

### Polling Pattern Implementation (For APIs without Webhooks)

```python
from dify_plugin.interfaces.trigger import (
    Trigger,
    TriggerSubscriptionConstructor,
    Subscription,
    CredentialType
)
from typing import Mapping, Any
import requests
import time
from datetime import datetime, timedelta

class MercuryTriggerConstructor(TriggerSubscriptionConstructor):
    """
    Handles subscription creation and polling logic
    """

    def _create_subscription(self,
                            endpoint: str,
                            parameters: Mapping[str, Any],
                            credentials: Mapping[str, Any],
                            credential_type: CredentialType) -> Subscription:
        """
        Create subscription for polling

        Args:
            endpoint: Webhook URL (not used for polling)
            parameters: User-configured parameters
            credentials: OAuth tokens or API keys
            credential_type: Type of credentials

        Returns:
            Subscription object with polling configuration
        """
        account_id = parameters.get("account_id")
        polling_interval = parameters.get("polling_interval", 60)

        # Validate credentials by making test API call
        access_token = credentials.get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(
            "https://api.mercury.com/api/v1/accounts",
            headers=headers
        )

        if response.status_code != 200:
            raise Exception(f"Failed to validate credentials: {response.text}")

        # Store polling configuration
        return Subscription(
            expires_at=int(time.time()) + (365 * 24 * 3600),  # 1 year
            endpoint=endpoint,  # Not used for polling
            parameters=parameters,
            properties={
                "account_id": account_id,
                "polling_interval": polling_interval,
                "last_check_time": None,  # Initialize state
                "access_token": access_token,
                "refresh_token": credentials.get("refresh_token"),
            }
        )

    def _delete_subscription(self, subscription: Subscription):
        """Clean up subscription (no-op for polling)"""
        pass

    def _refresh_subscription(self, subscription: Subscription) -> Subscription:
        """Refresh subscription expiration"""
        subscription.expires_at = int(time.time()) + (365 * 24 * 3600)
        return subscription

    # OAuth Methods (if using OAuth)
    def _oauth_get_authorization_url(self,
                                    redirect_uri: str,
                                    system_credentials: Mapping[str, Any]) -> str:
        """Generate OAuth authorization URL"""
        import secrets
        import urllib.parse

        state = secrets.token_urlsafe(16)

        params = {
            "client_id": system_credentials["client_id"],
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "read:accounts read:transactions offline_access",
            "state": state,
        }

        return f"https://app.mercury.com/oauth/authorize?{urllib.parse.urlencode(params)}"

    def _oauth_get_credentials(self,
                               code: str,
                               redirect_uri: str,
                               system_credentials: Mapping[str, Any]) -> dict:
        """Exchange authorization code for tokens"""
        response = requests.post(
            "https://oauth2.mercury.com/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": system_credentials["client_id"],
                "client_secret": system_credentials["client_secret"],
            }
        )

        if response.status_code != 200:
            raise Exception(f"Failed to get credentials: {response.text}")

        data = response.json()

        return {
            "access_token": data["access_token"],
            "refresh_token": data.get("refresh_token"),
            "expires_at": str(int(time.time()) + data.get("expires_in", 3600)),
        }

    def _oauth_refresh_credentials(self,
                                   refresh_token: str,
                                   system_credentials: Mapping[str, Any]) -> dict:
        """Refresh expired access token"""
        response = requests.post(
            "https://oauth2.mercury.com/oauth2/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": system_credentials["client_id"],
                "client_secret": system_credentials["client_secret"],
            }
        )

        if response.status_code != 200:
            raise Exception(f"Failed to refresh token: {response.text}")

        data = response.json()

        return {
            "access_token": data["access_token"],
            "refresh_token": data.get("refresh_token", refresh_token),
            "expires_at": str(int(time.time()) + data.get("expires_in", 3600)),
        }


class MercuryTrigger(Trigger):
    """
    Polling-based trigger (runs periodically)
    """

    def __init__(self):
        super().__init__()
        # Dify will call this trigger periodically

    def _poll_events(self, subscription: Subscription) -> list[dict]:
        """
        Poll Mercury API for new transactions

        This method is called periodically by Dify based on polling_interval
        """
        access_token = subscription.properties.get("access_token")
        account_id = subscription.properties.get("account_id")
        last_check_time = subscription.properties.get("last_check_time")

        # Default to 1 hour ago if first run
        if not last_check_time:
            last_check_time = (datetime.utcnow() - timedelta(hours=1)).isoformat()

        # Fetch new transactions since last check
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {
            "postedAtStart": last_check_time,
            "limit": 100,
        }

        if account_id:
            url = f"https://api.mercury.com/api/v1/account/{account_id}/transactions"
        else:
            url = "https://api.mercury.com/api/v1/transactions"

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            self.logger.error(f"Failed to fetch transactions: {response.text}")
            return []

        transactions = response.json().get("transactions", [])

        # Update last check time
        subscription.properties["last_check_time"] = datetime.utcnow().isoformat()

        # Return events for each transaction
        events = []
        for txn in transactions:
            events.append({
                "event_name": "transaction.created",
                "payload": self._normalize_transaction(txn)
            })

        return events

    def _normalize_transaction(self, raw_txn: dict) -> dict:
        """Normalize Mercury transaction format"""
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
        }
```

---

## Event Definition

**File**: `events/transaction_created/transaction_created.yaml`

```yaml
identity:
  name: transaction_created
  author: your_name
  label:
    en_US: New Transaction Created
    zh_Hans: 新交易创建
description:
  en_US: Triggered when a new transaction is detected
  zh_Hans: 检测到新交易时触发

# User-configurable parameters
parameters:
  - name: transaction_type
    type: select
    required: false
    label:
      en_US: Transaction Type Filter
    options:
      - value: all
        label:
          en_US: All Transactions
      - value: debit
        label:
          en_US: Debits Only
      - value: credit
        label:
          en_US: Credits Only
    default: all

# Event output schema (available to workflow)
output_schema:
  type: object
  properties:
    transaction_id:
      type: string
      description: Unique transaction ID
    account_id:
      type: string
      description: Account ID
    amount:
      type: number
      description: Transaction amount
    type:
      type: string
      description: Transaction type (debit/credit)
      enum: [debit, credit]
    date:
      type: string
      description: Transaction date
    merchant:
      type: string
      description: Merchant name
    description:
      type: string
      description: Transaction description
    category:
      type: string
      description: Transaction category
    status:
      type: string
      description: Transaction status
```

---

**File**: `events/transaction_created/transaction_created.py`

```python
from dify_plugin.interfaces.trigger import Event, Variables, EventIgnoreError
from werkzeug import Request
from typing import Mapping, Any

class TransactionCreatedEvent(Event):
    """
    Handle transaction.created events
    """

    def _on_event(self,
                  request: Request,
                  parameters: Mapping[str, Any],
                  payload: Mapping[str, Any]) -> Variables:
        """
        Process event and apply filters

        Args:
            request: Webhook request (for webhook pattern)
            parameters: User-configured event parameters
            payload: Event payload from _dispatch_event or polling

        Returns:
            Variables matching output_schema

        Raises:
            EventIgnoreError: To filter out unwanted events
        """
        # Apply transaction type filter
        transaction_type_filter = parameters.get("transaction_type", "all")
        transaction_type = payload.get("type")

        if transaction_type_filter != "all":
            if transaction_type != transaction_type_filter:
                # Filter out this event
                raise EventIgnoreError(
                    f"Transaction type {transaction_type} doesn't match filter"
                )

        # Return variables for workflow
        return Variables(variables={
            "transaction_id": payload.get("transaction_id"),
            "account_id": payload.get("account_id"),
            "amount": payload.get("amount"),
            "type": payload.get("type"),
            "date": payload.get("date"),
            "merchant": payload.get("merchant"),
            "description": payload.get("description"),
            "category": payload.get("category", ""),
            "status": payload.get("status"),
        })
```

---

## State Management (For Polling)

Dify provides persistent key-value storage for triggers:

```python
# In your Trigger class

# Store state
self.session.storage.set("last_check_time", datetime.utcnow().isoformat())
self.session.storage.set("last_transaction_id", "txn_123")

# Retrieve state
last_check = self.session.storage.get("last_check_time")
last_txn_id = self.session.storage.get("last_transaction_id")

# Delete state
self.session.storage.delete("last_check_time")
```

**Important**:
- Enable storage in `manifest.yaml`: `permission.storage.enabled: true`
- State persists across polling intervals
- Use for tracking last processed items

---

## Error Handling

### Available Exceptions

```python
from dify_plugin.entities.trigger import (
    TriggerValidationError,      # Security validation failures
    TriggerDispatchError,         # Parsing or routing errors
    SubscriptionError,            # API errors during subscription
    EventIgnoreError,             # Filter out unwanted events
)
```

### Usage Examples

```python
# Webhook signature validation failure
if not valid_signature:
    raise TriggerValidationError("Invalid webhook signature")

# Event filtering
if not meets_criteria:
    raise EventIgnoreError("Event doesn't match filters")

# Subscription creation failure
if api_response.status_code != 200:
    raise SubscriptionError(f"Failed to create subscription: {api_response.text}")

# Event dispatch parsing error
try:
    payload = request.get_json()
except:
    raise TriggerDispatchError("Invalid JSON payload")
```

---

## Testing & Debugging

### Remote Debugging

```bash
cd mercury-trigger
dify plugin debug
```

In Dify Studio:
1. Go to Plugins → Add Remote Plugin
2. Enter the debug endpoint URL
3. Configure subscription
4. Trigger events (webhook or wait for polling)

### Testing Polling Logic

```python
# Add logging for debugging
class MercuryTrigger(Trigger):
    def _poll_events(self, subscription: Subscription):
        self.logger.info(f"Starting poll at {datetime.utcnow()}")

        # ... polling logic

        self.logger.info(f"Found {len(events)} new events")
        return events
```

### Packaging

```bash
cd mercury-trigger
dify plugin package ./
# Generates mercury-trigger.difypkg
```

---

## Best Practices

### Polling Pattern

1. **Efficient Polling**:
   - Use reasonable intervals (60-300 seconds)
   - Store last check timestamp
   - Use API filtering (e.g., `postedAtStart` parameter)
   - Limit batch size to avoid timeouts

2. **State Management**:
   - Always initialize state on first run
   - Update state after successful processing
   - Handle missing state gracefully

3. **Error Handling**:
   - Log errors but don't crash
   - Implement retry with exponential backoff
   - Handle token expiration gracefully

### Webhook Pattern

1. **Security**:
   - Always validate signatures
   - Use constant-time comparison (`hmac.compare_digest`)
   - Return appropriate HTTP status codes

2. **Idempotency**:
   - Track processed event IDs
   - Ignore duplicate events

3. **Response**:
   - Respond quickly (< 3 seconds)
   - Return 200 even if event is filtered
   - Use appropriate HTTP status codes

### General

1. **OAuth**:
   - Never return `client_secret` in credentials
   - Implement token refresh
   - Handle token expiration gracefully

2. **Performance**:
   - Keep memory usage low
   - Avoid blocking operations
   - Use async operations where possible

3. **Logging**:
   - Log important events
   - Don't log sensitive data (tokens, secrets)
   - Use appropriate log levels

---

## Complete Example Structure

```python
# provider/mercury.py

from dify_plugin.interfaces.trigger import (
    Trigger,
    TriggerSubscriptionConstructor,
    EventDispatch,
    Subscription,
    CredentialType
)
from werkzeug import Request, Response
from typing import Mapping, Any
import requests
import time
from datetime import datetime, timedelta


class MercuryTriggerConstructor(TriggerSubscriptionConstructor):
    """Subscription management"""

    def _create_subscription(self, endpoint, parameters, credentials, credential_type):
        # Implementation here
        pass

    def _delete_subscription(self, subscription):
        pass

    def _refresh_subscription(self, subscription):
        pass

    def _oauth_get_authorization_url(self, redirect_uri, system_credentials):
        # Implementation here
        pass

    def _oauth_get_credentials(self, code, redirect_uri, system_credentials):
        # Implementation here
        pass

    def _oauth_refresh_credentials(self, refresh_token, system_credentials):
        # Implementation here
        pass


class MercuryTrigger(Trigger):
    """Main trigger class - polling implementation"""

    def _poll_events(self, subscription: Subscription) -> list[dict]:
        """Poll for new transactions"""
        # Implementation here
        pass

    def _normalize_transaction(self, raw_txn: dict) -> dict:
        """Normalize transaction data"""
        # Implementation here
        pass
```

---

## Resources

- **Official Documentation**: https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/trigger-plugin
- **OAuth Guide**: https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/tool-oauth
- **Release Notes**: https://github.com/langgenius/dify/releases/tag/1.10.0
- **SDK Repository**: https://github.com/langgenius/dify-plugin-sdks
- **Example (GitHub Trigger)**: https://github.com/langgenius/dify-plugin-sdks/tree/feat/trigger/python/examples/github_trigger

---

*Last Updated: 2025-12-26*
*Dify Version: 1.10.0+*
*SDK Version: 0.6.0+*
