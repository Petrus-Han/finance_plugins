# TaxPayment

Tax Payment/Refund made against filed taxReturn. Applicable for AU, CA and UK locales only.

## The TaxPayment Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Required for update, read only, system defined | Unique identifier for this object. Sort order is ASC by default. |
| **SyncToken** | String | Required for update, read only, system defined | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. |
| **MetaData** | ModificationMetaData, filterable, sortable | Optional | Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications. |
| **Refund** | Boolean (minorVersion: 47) | Optional | Indicate if this transaction is a refund. Returns false for the payment. |
| **TxnDate** | Date (minorVersion: 47) | read only | Indicates the tax payment date. |
| **PaymentAccountRef** | ReferenceType (minorVersion: 47) | read only, system defined | Indicates the Account ID from which the payment was made (or refund was moved to). |
| **Description** | String (minorVersion: 47) | read only, system defined | Specifies the Memo/Description added for this payment. |
| **PaymentAmount** | Decimal (minorVersion: 47) | read only | Specifies the tax payment amount paid towards a filed tax return. |

### Sample Object

```json
{
  "TaxPayment": {
    "Refund": "false",
    "SyncToken": "0",
    "domain": "QBO",
    "PaymentAccountRef": {
      "name": "Cash and cash equivalents-BAS Payment",
      "value": "57"
    },
    "PaymentAmount": "10.00",
    "PaymentDate": "2019-08-30",
    "sparse": "false",
    "Id": "8",
    "MetaData": {
      "CreateTime": "2019-08-30T06:00:26-07:00",
      "LastUpdatedTime": "2019-08-30T06:00:26-07:00"
    }
  },
  "time": "2020-02-03T11:05:54.491-08:00"
}
```

## Query TaxPayment

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
select * From TaxPayment
```

### Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "TaxPayment": [
      {
        "Refund": "false",
        "SyncToken": "0",
        "domain": "QBO",
        "PaymentAccountRef": {
          "name": "Cash and cash equivalents-BAS Payment",
          "value": "57"
        },
        "PaymentAmount": "10.00",
        "PaymentDate": "2019-08-30",
        "sparse": "false",
        "Id": "8",
        "MetaData": {
          "CreateTime": "2019-08-30T06:00:26-07:00",
          "LastUpdatedTime": "2019-08-30T06:00:26-07:00"
        }
      },
      {
        "Refund": "false",
        "SyncToken": "0",
        "domain": "QBO",
        "PaymentAccountRef": {
          "name": "Cash and cash equivalents-BAS Payment",
          "value": "57"
        },
        "Description": "testing VAT Payment",
        "PaymentAmount": "10.00",
        "PaymentDate": "2019-08-30",
        "sparse": "false",
        "Id": "9",
        "MetaData": {
          "CreateTime": "2019-08-30T06:02:40-07:00",
          "LastUpdatedTime": "2019-08-30T06:02:40-07:00"
        }
      },
      {
        "Refund": "false",
        "SyncToken": "0",
        "domain": "QBO",
        "PaymentAccountRef": {
          "name": "Cash and cash equivalents-BAS Payment",
          "value": "57"
        },
        "Description": "test the id",
        "PaymentAmount": "10.00",
        "PaymentDate": "2019-09-01",
        "sparse": "false",
        "Id": "10",
        "MetaData": {
          "CreateTime": "2019-09-01T01:48:39-07:00",
          "LastUpdatedTime": "2019-09-01T01:48:39-07:00"
        }
      },
      {
        "Refund": "false",
        "SyncToken": "0",
        "domain": "QBO",
        "PaymentAccountRef": {
          "name": "Cash and cash equivalents-BAS Payment",
          "value": "57"
        },
        "Description": "qwerty",
        "PaymentAmount": "15.00",
        "PaymentDate": "2019-09-01",
        "sparse": "false",
        "Id": "11",
        "MetaData": {
          "CreateTime": "2019-09-01T01:50:30-07:00",
          "LastUpdatedTime": "2019-09-01T01:50:30-07:00"
        }
      }
    ],
    "maxResults": 5,
    "totalCount": 5
  },
  "time": "2020-02-03T15:59:25.586-08:00"
}
```

## Read TaxPayment

Retrieves the tax payment/refund made against filed tax return.

### Returns

Returns the taxpayment object.

### Request URL

```
GET /v3/company/<realmID>/taxpayment/<taxPaymentId>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "TaxPayment": {
    "Refund": "false",
    "SyncToken": "0",
    "domain": "QBO",
    "PaymentAccountRef": {
      "name": "Cash and cash equivalents-BAS Payment",
      "value": "57"
    },
    "PaymentAmount": "10.00",
    "PaymentDate": "2019-08-30",
    "sparse": "false",
    "Id": "8",
    "MetaData": {
      "CreateTime": "2019-08-30T06:00:26-07:00",
      "LastUpdatedTime": "2019-08-30T06:00:26-07:00"
    }
  },
  "time": "2020-02-03T11:05:54.491-08:00"
}
```
