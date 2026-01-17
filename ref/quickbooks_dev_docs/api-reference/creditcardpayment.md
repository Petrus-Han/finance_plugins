# CreditCardPayment

Represents a financial transaction to record a Credit Card balance payment in QuickBooks Online. It provides an easy way for users to move money from a Bank account to a Credit Card account. It is essentially a more limited Transfer form.

## Business Rules

- This transaction does not support multi-currency. Only payments made from home currency Bank accounts to home currency Credit Card accounts will be accepted.

## The CreditCardPayment Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Required for update | Unique identifier for this object. Sort order is ASC by default. Read only, system defined. |
| **CreditCardAccountRef** | ReferenceType | Required | Identifies the credit card account to which funds are transferred. Query the Account name list resource to determine the appropriate Account object for this reference. |
| **Amount** | Decimal | Required | Indicates the total amount of the transaction. |
| **BankAccountRef** | ReferenceType | Required | Identifies the bank account from which funds are transferred. Query the Account name list resource to determine the appropriate Account object for this reference. |
| **SyncToken** | String | Required for update | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. Read only, system defined. |
| **PrivateNote** | String | Optional | User entered, organization-private note about the transaction. This field maps to the Memo field on the Pay down credit card form. Max of 4000 chars. |
| **VendorRef** | ReferenceType, filterable | Optional | Reference to the vendor for this transaction. Query the Vendor name list resource to determine the appropriate Vendor object for this reference. Use Vendor.Id and Vendor.Name from that object for VendorRef.value and VendorRef.name, respectively. Available with minorVersion 54. |
| **TxnDate** | Date, filterable, sortable | Optional | The date entered by the user when this transaction occurred. For posting transactions, this is the posting date that affects the financial statements. If the date is not supplied, the current date on the server is used. Sort order is ASC by default. |
| **Memo** | String | Optional | User entered, organization-private note about the transaction. This field maps to the Memo field on the Pay down credit card form. Max of 4000 chars. Available with minorVersion 54. |
| **PrintStatus** | String | Optional | Printing status of the credit-card-payment. Valid values: NotSet, NeedToPrint, PrintComplete. Available with minorVersion 54. |
| **CheckNum** | String | Optional | User entered, Check number. This field maps to the Check no. field on the Pay down credit card form. Available with minorVersion 54. |
| **MetaData** | ModificationMetaData | Optional | Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications. |

### Sample Object

```json
{
  "CreditCardPaymentTxn": {
    "SyncToken": "0",
    "domain": "QBO",
    "CreditCardAccountRef": {
      "name": "Credit Card",
      "value": "57"
    },
    "TxnDate": "2020-03-27",
    "CurrencyRef": {
      "name": "United States Dollar",
      "value": "USD"
    },
    "Amount": 10.0,
    "sparse": false,
    "BankAccountRef": {
      "name": "Checking",
      "value": "37"
    },
    "Id": "29",
    "MetaData": {
      "CreateTime": "2020-03-27T07:01:04-07:00",
      "LastUpdatedTime": "2020-03-27T07:01:04-07:00"
    }
  },
  "time": "2020-03-27T07:06:45.630-07:00"
}
```

## Create a CreditCardPayment

### Minimum Required Elements

| Attribute | Type | Description |
|-----------|------|-------------|
| **TxnDate** | Date | Date of transaction. |
| **Amount** | Decimal | Total amount of the payment. Denominated in the currency of the credit card account. |
| **BankAccountRef** | ReferenceType | Bank account used to pay the Credit Card balance. Must be a Bank account. |
| **CreditCardAccountRef** | ReferenceType | Credit Card account for which a payment is being entered. Must be a Credit Card account. |
| **PrivateNote** | String | User entered, organization-private note about the transaction. (Optional) |

### Request

```
POST /v3/company/<realmID>/creditcardpayment
Content-Type: application/json, application/xml
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "PrivateNote": "This will fill in the memo field.",
  "TxnDate": "2020-03-27",
  "Amount": "100",
  "BankAccountRef": {
    "name": "Checking",
    "value": 37
  },
  "CreditCardAccountRef": {
    "name": "Credit Card",
    "value": 57
  }
}
```

### Response

```json
{
  "CreditCardPaymentTxn": {
    "SyncToken": "0",
    "domain": "QBO",
    "CreditCardAccountRef": {
      "name": "Credit Card",
      "value": "57"
    },
    "TxnDate": "2020-03-27",
    "CurrencyRef": {
      "name": "United States Dollar",
      "value": "USD"
    },
    "PrivateNote": "This will fill in the memo field.",
    "Amount": 100.0,
    "sparse": false,
    "BankAccountRef": {
      "name": "Checking",
      "value": "37"
    },
    "Id": "31",
    "MetaData": {
      "CreateTime": "2020-03-27T07:18:05-07:00",
      "LastUpdatedTime": "2020-03-27T07:18:05-07:00"
    }
  },
  "time": "2020-03-27T07:18:05.713-07:00"
}
```

## Delete a CreditCardPayment

This operation deletes the CreditCardPayment object specified in the request body. The request body must include the full payload of the CreditCardPayment as returned in a read response.

### Request

```
POST /v3/company/<realmID>/creditcardpayment?operation=delete
Content-Type: application/json, application/xml
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "TxnDate": "2020-03-27",
  "PrivateNote": "This will fill in the memo field.",
  "CreditCardAccountRef": {
    "name": "Credit Card",
    "value": 57
  },
  "SyncToken": "0",
  "Amount": "100",
  "BankAccountRef": {
    "name": "Checking",
    "value": 37
  },
  "Id": "31"
}
```

### Response

```json
{
  "CreditCardPaymentTxn": {
    "status": "Deleted",
    "domain": "QBO",
    "Id": "31"
  },
  "time": "2020-03-27T07:38:07.499-07:00"
}
```

## Query a CreditCardPayment

Returns the results of the query.

### Request

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content-Type: application/text
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Sample Query

```sql
select * from creditcardpayment
```

### Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "totalCount": 2,
    "CreditCardPaymentTxn": [
      {
        "SyncToken": "0",
        "domain": "QBO",
        "CreditCardAccountRef": {
          "name": "Credit Card",
          "value": "57"
        },
        "TxnDate": "2020-03-27",
        "CurrencyRef": {
          "name": "United States Dollar",
          "value": "USD"
        },
        "PrivateNote": "This is a memo",
        "Amount": 15.0,
        "sparse": false,
        "BankAccountRef": {
          "name": "Checking",
          "value": "37"
        },
        "Id": "30",
        "MetaData": {
          "CreateTime": "2020-03-27T07:15:05-07:00",
          "LastUpdatedTime": "2020-03-27T07:15:05-07:00"
        }
      },
      {
        "SyncToken": "0",
        "domain": "QBO",
        "CreditCardAccountRef": {
          "name": "Credit Card",
          "value": "57"
        },
        "TxnDate": "2020-03-27",
        "CurrencyRef": {
          "name": "United States Dollar",
          "value": "USD"
        },
        "Amount": 10.0,
        "sparse": false,
        "BankAccountRef": {
          "name": "Checking",
          "value": "37"
        },
        "Id": "29",
        "MetaData": {
          "CreateTime": "2020-03-27T07:01:04-07:00",
          "LastUpdatedTime": "2020-03-27T07:01:04-07:00"
        }
      }
    ],
    "maxResults": 2
  },
  "time": "2020-03-27T07:15:46.750-07:00"
}
```

## Read a CreditCardPayment

Retrieves the details of a CreditCardPayment object that has been previously created.

### Request

```
GET /v3/company/<realmID>/creditcardpayment/<creditcardpaymentId>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "CreditCardPaymentTxn": {
    "SyncToken": "0",
    "domain": "QBO",
    "CreditCardAccountRef": {
      "name": "Credit Card",
      "value": "57"
    },
    "TxnDate": "2020-03-27",
    "CurrencyRef": {
      "name": "United States Dollar",
      "value": "USD"
    },
    "Amount": 10.0,
    "sparse": false,
    "BankAccountRef": {
      "name": "Checking",
      "value": "37"
    },
    "Id": "29",
    "MetaData": {
      "CreateTime": "2020-03-27T07:01:04-07:00",
      "LastUpdatedTime": "2020-03-27T07:01:04-07:00"
    }
  },
  "time": "2020-03-27T07:06:45.630-07:00"
}
```

## Full Update a CreditCardPayment

Use this operation to update any of the writable fields of an existing CreditCardPayment object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL. The ID of the object to update is specified in the request body.

### Request

```
POST /v3/company/<realmID>/creditcardpayment
Content-Type: application/json, application/xml
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "TxnDate": "2020-03-27",
  "PrivateNote": "This will fill in the memo field.",
  "CreditCardAccountRef": {
    "name": "Credit Card",
    "value": 57
  },
  "SyncToken": "0",
  "Amount": "100",
  "BankAccountRef": {
    "name": "Checking",
    "value": 37
  },
  "Id": "29"
}
```

### Response

```json
{
  "CreditCardPaymentTxn": {
    "SyncToken": "1",
    "domain": "QBO",
    "CreditCardAccountRef": {
      "name": "Credit Card",
      "value": "57"
    },
    "TxnDate": "2020-03-27",
    "CurrencyRef": {
      "name": "United States Dollar",
      "value": "USD"
    },
    "PrivateNote": "This will fill in the memo field.",
    "Amount": 100.0,
    "sparse": false,
    "BankAccountRef": {
      "name": "Checking",
      "value": "37"
    },
    "Id": "29",
    "MetaData": {
      "CreateTime": "2020-03-27T07:01:04-07:00",
      "LastUpdatedTime": "2020-03-27T07:31:22-07:00"
    }
  },
  "time": "2020-03-27T07:31:22.379-07:00"
}
```

## Sparse Update a CreditCardPayment

Sparse updating provides the ability to update a subset of properties for a given object; only elements specified in the request are updated. Missing elements are left untouched. The ID of the object to update is specified in the request body.

### Request

```
POST /v3/company/<realmID>/creditcardpayment
Content-Type: application/json, application/xml
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "TxnDate": "2020-03-27",
  "PrivateNote": "This is a corrected memo field.",
  "CreditCardAccountRef": {
    "name": "Credit Card",
    "value": 57
  },
  "SyncToken": "1",
  "Amount": "100",
  "sparse": true,
  "BankAccountRef": {
    "name": "Checking",
    "value": 37
  },
  "Id": "29"
}
```

### Response

```json
{
  "CreditCardPaymentTxn": {
    "SyncToken": "2",
    "domain": "QBO",
    "CreditCardAccountRef": {
      "name": "Credit Card",
      "value": "57"
    },
    "TxnDate": "2020-03-27",
    "CurrencyRef": {
      "name": "United States Dollar",
      "value": "USD"
    },
    "PrivateNote": "This is a corrected memo field.",
    "Amount": 100.0,
    "sparse": false,
    "BankAccountRef": {
      "name": "Checking",
      "value": "37"
    },
    "Id": "29",
    "MetaData": {
      "CreateTime": "2020-03-27T07:01:04-07:00",
      "LastUpdatedTime": "2020-03-27T07:59:42-07:00"
    }
  },
  "time": "2020-03-27T07:59:42.418-07:00"
}
```
