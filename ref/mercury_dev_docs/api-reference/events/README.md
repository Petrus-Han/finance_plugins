# Events API

Base URL: `https://api.mercury.com/api/v1`

The Events API provides visibility into changes to your Mercury resources through a pull-based event log. Query and replay historical changes for backfills, reconciliation, and audit trails.

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/events` | Get all events |
| GET | `/event/{eventId}` | Get event by ID |

---

## GET /events

Retrieve a list of events for your organization.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Max results per page (default: 50) |
| start_after | string | No | Cursor for forward pagination |
| end_before | string | No | Cursor for backward pagination |
| resourceType | string | No | Filter by resource type |
| eventType | string | No | Filter by event type |
| start | string | No | Start timestamp (ISO 8601) |
| end | string | No | End timestamp (ISO 8601) |

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/events?resourceType=transaction&limit=50" \
  -H "Authorization: Bearer <token>"
```

### Response

```json
{
  "events": [
    {
      "id": "evt_123",
      "type": "transaction.created",
      "resourceType": "transaction",
      "resourceId": "txn_456",
      "createdAt": "2024-01-15T10:30:00Z",
      "data": {
        "id": "txn_456",
        "accountId": "account_123",
        "amount": -1500.00,
        "status": "pending",
        "counterpartyName": "Acme Corp"
      }
    },
    {
      "id": "evt_124",
      "type": "transaction.updated",
      "resourceType": "transaction",
      "resourceId": "txn_456",
      "createdAt": "2024-01-15T10:35:00Z",
      "data": {
        "id": "txn_456",
        "status": "sent"
      },
      "previousData": {
        "status": "pending"
      }
    }
  ],
  "hasMore": true,
  "nextCursor": "evt_125"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique event ID |
| type | string | Event type (e.g., `transaction.created`) |
| resourceType | string | Resource type (e.g., `transaction`) |
| resourceId | string | ID of affected resource |
| createdAt | string | ISO 8601 timestamp |
| data | object | Current resource state |
| previousData | object | Previous state (for updates) |

### Event Types

| Event Type | Description |
|------------|-------------|
| transaction.created | New transaction created |
| transaction.updated | Transaction status or details changed |
| transaction.deleted | Transaction cancelled/deleted |

### Resource Types

Currently supported:
- `transaction`

Coming soon:
- `account`
- `card`
- `recipient`

---

## GET /event/{eventId}

Get details for a specific event.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| eventId | string | Yes | Event ID |

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/event/{eventId}" \
  -H "Authorization: Bearer <token>"
```

---

## Use Cases

### Backfill Historical Data

```python
def backfill_transactions(start_date):
    events = []
    cursor = None
    
    while True:
        params = {
            "resourceType": "transaction",
            "start": start_date,
            "limit": 100
        }
        if cursor:
            params["start_after"] = cursor
            
        response = requests.get(
            "https://api.mercury.com/api/v1/events",
            headers={"Authorization": f"Bearer {token}"},
            params=params
        )
        data = response.json()
        events.extend(data["events"])
        
        if not data.get("hasMore"):
            break
        cursor = data["nextCursor"]
    
    return events
```

### Reconciliation

```python
def reconcile_transactions():
    # Fetch events since last sync
    events = get_events_since(last_sync_timestamp)
    
    for event in events:
        if event["type"] == "transaction.created":
            create_local_record(event["data"])
        elif event["type"] == "transaction.updated":
            update_local_record(event["resourceId"], event["data"])
        elif event["type"] == "transaction.deleted":
            delete_local_record(event["resourceId"])
    
    update_last_sync_timestamp()
```

### Audit Trail

```python
def get_transaction_history(transaction_id):
    response = requests.get(
        "https://api.mercury.com/api/v1/events",
        headers={"Authorization": f"Bearer {token}"},
        params={
            "resourceType": "transaction",
            "resourceId": transaction_id
        }
    )
    
    events = response.json()["events"]
    
    # Build timeline of changes
    timeline = []
    for event in events:
        timeline.append({
            "timestamp": event["createdAt"],
            "action": event["type"],
            "changes": event.get("previousData", {}),
            "new_state": event["data"]
        })
    
    return timeline
```

---

## Best Practices

1. **Use cursor pagination** - Don't use offset-based pagination for large datasets
2. **Store cursors** - Save the last cursor for incremental syncing
3. **Handle duplicates** - Events may be delivered more than once; use event ID for idempotency
4. **Process in order** - Events for the same resource should be processed chronologically
5. **Prefer Events over polling** - Use Events API instead of repeatedly polling `/transactions`
