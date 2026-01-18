# Change Data Capture Operation

> Source: https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api/change-data-capture

Use the change data capture operation (also known as CDC) to see which API entities and what data changed within a certain timeframe. This lets you track recent changes made by your app or QuickBooks Online users.

Use the CDC operation to poll Intuit's data services. This returns the full payload for entities that changed within the specified "look-back" period.

> **Tip**: If you'd rather get periodic event notifications via HTTP POSTs, consider [using webhooks](../../develop/webhooks.md). This reduces the need to dedicate servers for polling.

---

## How Change Data Capture Works

- CDC operations can track changes within the **last 30 days**
- Server responses can handle a maximum of **1,000 objects**
- Query for shorter time periods to ensure all data changes are captured

### Unsupported Entities

CDC operation works for [all API entities](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account) **except**:

- `JournalCode`
- `TaxAgency`
- `TimeActivity`
- `TaxCode`
- `TaxRate`

---

## Step 1: Use the Change Data Capture Operation

Use a **GET** operation with the following parameter:

```http
GET https://quickbooks.api.intuit.com/v3/company/<realmId>/cdc?entities=<entityList>&changedSince=<dateTime>
Content-Type: text/plain
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `realmId` | The company ID of the QuickBooks Online company you're sending requests to |
| `entityList` | The comma-separated list of entities you want to see changes for |
| `dateTime` | The date-time stamp within the past 30 days. This sets the look-back date from today. The date format is ISO (YYYY-MM-DD) |

### Response Notes

- The server response only lists entities that changed since the "look-back" date
- Deleted entities return a `Deleted` value for the `status` field

Learn more [about the change data capture operation](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/changedatacapture).

---

## Example CDC Request

Your app needs to synchronize with QuickBooks Online every hour. The last refresh was on December 23, 2015, at 9:00 PST (2015-12-23T09:00-07:00).

Your app needs to refresh its local data for:
- Estimate
- Customer

Since then, a QuickBooks Online customer has:
- Updated two Estimate entities
- Deleted one Estimate entity
- Updated two Customer entities

### Request

```http
GET https://quickbooks.api.intuit.com/v3/company/<realmId>/cdc?entities=estimate,customer&changedSince=2015-12-23T10:00:00-07:00
```

### Response

```json
{
  "CDCResponse": [{
    "QueryResponse": [{
      "Customer": [{
        "Id": "63",
        ...
      }, {
        "Id": "99",
        ...
      }],
      "startPosition": 1,
      "maxResults": 2
    }, {
      "Estimate": [{
        "Id": "34",
        ...
      }, {
        "Id": "123",
        ...
      }, {
        "domain": "QBO",
        "status": "Deleted",
        "Id": "979",
        "MetaData": {
          "LastUpdatedTime": "2015-12-23T12:55:50-08:00"
        }
      }],
      "startPosition": 1,
      "maxResults": 3,
      "totalCount": 5
    }]
  }],
  "time": "2015-12-23T10:00:01-07:00"
}
```

The server response includes full payloads for the two **Customer** and two **Estimate** objects. Both were modified (i.e. `LastUpdatedTime` field) between 9:00 and 10:00 PST.

### No Changes Response

If there were no changes since the last refresh:

```json
{
  "CDCResponse": [
    {
      "QueryResponse": [
        {}
      ]
    }
  ],
  "time": "2015-12-23T12:36:51.763-08:00"
}
```

---

## Step 2: Refresh Your App's Local Data

Set up your app to update its local database based on the CDC response:

Based on the example above, your app should:

| Action | Entity | IDs |
|--------|--------|-----|
| **Refresh** | Customer | 63, 99 |
| **Refresh** | Estimate | 34, 123 |
| **Remove/Mark Deleted** | Estimate | 979 |

---

## Mercury Integration Notes

For Mercury bank transaction sync, CDC is useful for:

1. **Detecting external changes**: When QuickBooks users manually edit or delete transactions
2. **Syncing local state**: Keeping your app's cache in sync with QuickBooks
3. **Conflict resolution**: Detecting if a transaction was modified before your update

### Example: Check for Purchase Changes

```http
GET https://quickbooks.api.intuit.com/v3/company/<realmId>/cdc?entities=Purchase,Deposit,Vendor&changedSince=2024-01-15T00:00:00-08:00
```

This returns all Purchases, Deposits, and Vendors modified since January 15, 2024.

---

## Best Practices

1. **Query frequently**: Use shorter time periods (e.g., hourly) to stay within the 1,000 object limit
2. **Track last sync time**: Store the timestamp of your last successful CDC query
3. **Handle deletions**: Check for `status: "Deleted"` and update your local data accordingly
4. **Consider webhooks**: For real-time notifications, webhooks may be more efficient than polling

---

## Learn More

- [CDC API Reference](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/changedatacapture)
- [Webhooks](../../develop/webhooks.md)
- [Data Queries](./data-queries.md)
