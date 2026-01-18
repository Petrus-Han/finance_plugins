# REST API Schema and Data Formats

> QuickBooks Online API: Basic schema and data formats

## Base URLs

| Environment | Base URL |
|-------------|----------|
| **Production** | `https://quickbooks.api.intuit.com` |
| **Sandbox** | `https://sandbox-quickbooks.api.intuit.com` |

## URI Formats

| Operation | URI Pattern |
|-----------|-------------|
| **Create/Update** | `POST {baseURL}/v3/company/{realmId}/{resourceName}` |
| **Read (single)** | `GET {baseURL}/v3/company/{realmId}/{resourceName}/{entityId}` |
| **Read (query)** | `GET {baseURL}/v3/company/{realmId}/query?query={selectStatement}` |
| **Delete** | `POST {baseURL}/v3/company/{realmId}/{resourceName}?operation=delete` |

### URI Components

| Component | Description |
|-----------|-------------|
| `baseURL` | Production or sandbox URL |
| `realmId` | Company ID (from OAuth callback) |
| `resourceName` | Entity name (customer, invoice, purchase, etc.) |
| `entityId` | Specific entity's unique ID |

---

## Request Headers

| Header | Description | Required |
|--------|-------------|----------|
| `Authorization` | `Bearer {access_token}` | **Required** |
| `Content-Type` | `application/json` | Required for POST |
| `Accept` | `application/json` or `application/pdf` | Optional |
| `Accept-Encoding` | `gzip`, `deflate` | Optional (improves performance) |

### Example POST Request

```http
POST /v3/company/12345678/invoice HTTP/1.1
Host: quickbooks.api.intuit.com
Accept: application/json
Content-Type: application/json
Authorization: Bearer eyJlbmMiOiJ**************xPfzFFw

{
  "Line": [
    {
      "Amount": 100.00,
      "DetailType": "SalesItemLineDetail",
      "SalesItemLineDetail": {
        "ItemRef": {
          "value": "1",
          "name": "Services"
        }
      }
    }
  ],
  "CustomerRef": {
    "value": "1"
  }
}
```

---

## Response Headers

| Header | Description |
|--------|-------------|
| `Content-Type` | MIME type of response |
| `intuit_tid` | Transaction ID (log this for support) |
| `QBO-Version` | API version that processed the request |
| `Date` | Response timestamp |

### Example Response

```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8
intuit_tid: gw-756b01cf-3fe0-4414-a2a2-321dd2287b7b
QBO-Version: 1512.462

{
  "Invoice": { ... },
  "time": "2024-01-15T09:19:21.923-08:00"
}
```

---

## Rate Limits and Throttles

### Standard Limits

| Server | API Endpoints | Batch Endpoint |
|--------|---------------|----------------|
| Sandbox | 500 req/min per realm | 40 batch req/min per realm |
| Production | 500 req/min per realm | 40 batch req/min per realm |

### Additional Limits

- **Per app**: 10 requests/second per realm
- **Query response**: Max 1000 entities (use pagination)
- **Line items**: Max 10,000 per transaction
- **Attachments**: Max 10,000 per transaction
- **Linked transactions**: Max 10,000 per transaction
- **Request timeout**: 120 seconds

### Throttling Response

When throttled, you'll receive **HTTP 429**. Wait **60 seconds** before retrying.

```json
{
  "Fault": {
    "Error": [
      {
        "Message": "Too Many Requests",
        "code": "429"
      }
    ]
  }
}
```

---

## Timestamps and Time Zones

### Format

```
<date>T<time><UTC offset>
YYYY-MM-DDTHH:MM:SS±HH:MM
```

### Example

```
2024-01-15T10:33:39-08:00
```

This represents 10:33:39 AM on January 15, 2024, in PST (UTC-8).

### Components

| Part | Format | Example |
|------|--------|---------|
| Date | `YYYY-MM-DD` | `2024-01-15` |
| Time | `HH:MM:SS` | `10:33:39` |
| UTC Offset | `±HH:MM` | `-08:00` |

---

## Character Encoding

| Region | Encoding |
|--------|----------|
| US | ISO-8859-1 (extended ASCII) |
| Non-US | UTF-8 |

---

## Reference Types

Many fields use reference types to link entities:

```json
{
  "AccountRef": {
    "value": "35",
    "name": "Checking"
  },
  "VendorRef": {
    "value": "42",
    "name": "ABC Supplies"
  },
  "CustomerRef": {
    "value": "58",
    "name": "XYZ Corp"
  }
}
```

| Field | Description |
|-------|-------------|
| `value` | Entity ID (required) |
| `name` | Entity display name (optional, for readability) |

---

## Common Field Patterns

### SyncToken (Optimistic Locking)

Every update requires the current `SyncToken`:

```json
{
  "Id": "123",
  "SyncToken": "0",
  "Name": "Updated Name"
}
```

- Token increments on each successful update
- Stale token → update rejected (re-read and retry)

### MetaData (Audit Fields)

```json
{
  "MetaData": {
    "CreateTime": "2024-01-15T10:00:00-08:00",
    "LastUpdatedTime": "2024-01-15T15:30:00-08:00"
  }
}
```

- Read-only
- Set by QuickBooks automatically

### Line Items

Transactions use `Line` arrays:

```json
{
  "Line": [
    {
      "Id": "1",
      "LineNum": 1,
      "Amount": 100.00,
      "DetailType": "AccountBasedExpenseLineDetail",
      "AccountBasedExpenseLineDetail": {
        "AccountRef": {
          "value": "54"
        }
      }
    }
  ]
}
```

---

## Minor Versions

Access incremental API changes via query parameter:

```
?minorversion=65
```

Always specify a minor version for consistent behavior:

```
GET /v3/company/12345/account?minorversion=65
```

See [Minor Versions](https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api/minor-versions) for current version.

---

## Read-Only Attributes

Values supplied for read-only attributes are silently ignored:

| Attribute | Behavior |
|-----------|----------|
| `Id` | System-generated on create |
| `SyncToken` | System-managed |
| `MetaData` | System-generated |
| `TotalAmt` | Calculated by QuickBooks |
| `Balance` | Calculated by QuickBooks |

---

## Sparse Updates

Update only specific fields without sending the entire object:

```json
{
  "Id": "123",
  "SyncToken": "0",
  "sparse": true,
  "DisplayName": "New Name Only"
}
```

- Set `sparse: true` in request body
- Only specified writable fields are updated
- Omitted fields remain unchanged
