# Batch Operation

> Source: https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api/batch

Instead of sending requests individually, you can eliminate overhead and send "batches" of requests to the QuickBooks Online Accounting API.

---

## How the Batch Operation Works

- Send up to **10 payloads** with a single batch operation
- Send up to **40 batch requests per minute** to an end-user's QuickBooks Online company (specified by the `realmId`)

### Benefits

- Streamline your app's code
- Reduce network latency caused by individual, synchronous API calls

---

## Batch Request Format

```http
POST https://quickbooks.api.intuit.com/v3/company/<realmId>/batch
Content-Type: application/json
```

### Request Body Structure

```json
{
  "BatchItemRequest": [
    {
      "bId": "1",
      "operation": "create",
      "Customer": {
        "DisplayName": "John Doe"
      }
    },
    {
      "bId": "2",
      "operation": "query",
      "Query": "SELECT * FROM Invoice WHERE TotalAmt > '100'"
    },
    {
      "bId": "3",
      "operation": "update",
      "Invoice": {
        "Id": "123",
        "SyncToken": "0",
        "sparse": true,
        "Line": []
      }
    }
  ]
}
```

### Response Structure

```json
{
  "BatchItemResponse": [
    {
      "bId": "1",
      "Customer": {
        "Id": "456",
        "DisplayName": "John Doe"
      }
    },
    {
      "bId": "2",
      "QueryResponse": {
        "Invoice": [],
        "startPosition": 1,
        "maxResults": 0
      }
    },
    {
      "bId": "3",
      "Invoice": {
        "Id": "123",
        "SyncToken": "1"
      }
    }
  ]
}
```

---

## Supported Operations

| Operation | Description |
|-----------|-------------|
| `create` | Create a new entity |
| `update` | Update an existing entity |
| `delete` | Delete an entity |
| `query` | Query entities |

---

## Rate Limits

| Limit Type | Value |
|------------|-------|
| Payloads per batch | 10 |
| Batch requests per minute | 40 |

---

## SDK Support

Learn more about batch operations for supported SDKs:
- [Java SDK](https://developer.intuit.com/app/developer/qbo/docs/develop/sdks-and-samples-collections/java/asynchronous-calls#batch-process)
- [.NET SDK](https://developer.intuit.com/app/developer/qbo/docs/develop/sdks-and-samples-collections/net/asynchronous-calls#batch-process)
- [PHP SDK](https://developer.intuit.com/app/developer/qbo/docs/develop/sdks-and-samples-collections/php/synchronous-calls#batch-process)

---

## Mercury Integration Notes

For Mercury bank transaction sync, batch operations can be useful for:

1. **Creating multiple transactions at once**: When syncing multiple Mercury transactions, batch them together
2. **Creating vendors and transactions**: Create a vendor and its associated purchase in one batch

### Example: Batch Create Purchase and Vendor

```json
{
  "BatchItemRequest": [
    {
      "bId": "1",
      "operation": "create",
      "Vendor": {
        "DisplayName": "Mercury Vendor ABC"
      }
    },
    {
      "bId": "2",
      "operation": "create",
      "Purchase": {
        "PaymentType": "Cash",
        "AccountRef": {"value": "35"},
        "Line": [{
          "Amount": 100.00,
          "DetailType": "AccountBasedExpenseLineDetail",
          "AccountBasedExpenseLineDetail": {
            "AccountRef": {"value": "54"}
          }
        }]
      }
    }
  ]
}
```

> **Note**: For list entities (Customer, Vendor, etc.), serial processing is recommended. Use batch operations primarily for transactions.

---

## Learn More

- [Batch API Reference](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/batch)
- [Data Queries](./data-queries.md)
- [Change Data Capture](./change-data-capture.md)
