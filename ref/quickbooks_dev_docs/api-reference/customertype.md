# CustomerType

Customer types allow categorizing customers in ways that are meaningful to the business. For example, one could set up customer types so that they indicate which industry a customer represents, a customer's geographic location, or how a customer first heard about the business. The categorization then can be used for reporting or mailings.

## The CustomerType Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Required for update, read only, system defined | Unique identifier for this object. Sort order is ASC by default. |
| **SyncToken** | String | Required for update, read only, system defined | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. |
| **Name** | String | Required for update, system defined | The full name of the customer type. |
| **Active** | Boolean, filterable, sortable | Optional | Indicates whether this customer type is active in the company or not. true--This customer type is active and enabled for use by QuickBooks. false—This customer type is inactive, is hidden from most display purposes, and is not available for use with financial transactions. |
| **MetaData** | ModificationMetaData, filterable, sortable | Optional | Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications. |

### Sample Object

```json
{
  "CustomerType": {
    "SyncToken": "1",
    "domain": "QBO",
    "Name": "ActiveNew",
    "sparse": false,
    "Active": true,
    "Id": "5000000000000003466",
    "MetaData": {
      "CreateTime": "2019-04-10T15:18:04-07:00",
      "LastUpdatedTime": "2019-04-10T15:36:53-07:00"
    }
  },
  "time": "2019-04-12T16:19:36.824-07:00"
}
```

## Query a CustomerType

### Returns

Returns the results of the query.

### Request URL

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content type: text/plain
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Sample Query

```sql
Select * From CustomerType
```

### Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "CustomerType": [
      {
        "SyncToken": "1",
        "domain": "QBO",
        "Name": "ActiveNew",
        "sparse": false,
        "Active": true,
        "Id": "5000000000000003466",
        "MetaData": {
          "CreateTime": "2019-04-10T15:18:04-07:00",
          "LastUpdatedTime": "2019-04-10T15:36:53-07:00"
        }
      },
      {
        "SyncToken": "0",
        "domain": "QBO",
        "Name": "Value",
        "sparse": false,
        "Active": true,
        "Id": "5000000000000003467",
        "MetaData": {
          "CreateTime": "2019-04-10T15:24:02-07:00",
          "LastUpdatedTime": "2019-04-10T15:24:02-07:00"
        }
      }
    ],
    "maxResults": 2
  },
  "time": "2019-04-12T16:17:47.414-07:00"
}
```

## Read a CustomerType

Retrieves the details of a CustomerType object.

### Returns

Returns the CustomerType object.

### Request URL

```
GET /v3/company/<realmID>/customertype/<Id>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "CustomerType": {
    "SyncToken": "1",
    "domain": "QBO",
    "Name": "ActiveNew",
    "sparse": false,
    "Active": true,
    "Id": "5000000000000003466",
    "MetaData": {
      "CreateTime": "2019-04-10T15:18:04-07:00",
      "LastUpdatedTime": "2019-04-10T15:36:53-07:00"
    }
  },
  "time": "2019-04-12T16:19:36.824-07:00"
}
```
