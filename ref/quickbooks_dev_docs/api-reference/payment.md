# Payment

A Payment object records a payment in QuickBooks. The payment can be applied for a particular customer against multiple Invoices and Credit Memos. It can also be created without any Invoice or Credit Memo, by just specifying an amount.

## Business Rules

- A Payment can be updated as a full update or a sparse update.
- A Payment can be linked to multiple Invoices or Credit Memos.
- If you have a large number of invoice and corresponding payment records that you wish to import to the QuickBooks Online company, sort the invoice and payment records in chronological order and use the batch resource to send invoice and payments batches of 10, one after the other, to ensure any open invoices get credited with their payments.

## The Payment Object

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **Id** | String, read only, filterable, sortable | Unique identifier for this object. *Required for update* |
| **TotalAmt** | Decimal, filterable | Indicates the total amount of the payment. This includes the total of all the charges, allowances, and taxes. *Required* |
| **CustomerRef** | ReferenceType, filterable | Reference to a customer or job. Query the Customer name list resource to determine the appropriate Customer object for this reference. *Required* |
| **SyncToken** | String, read only | Version number of the object. It is used to lock an object for use by one app at a time. *Required for update* |
| **CurrencyRef** | CurrencyRefType | Reference to the currency in which all amounts on the associated transaction are expressed. Required if multicurrency is enabled for the company. *Conditionally required* |
| **TxnDate** | Date, filterable, sortable | The date when the transaction occurred. |
| **PrivateNote** | String (max 4000 chars) | User-entered, organization-private note about the payment. |
| **PaymentMethodRef** | ReferenceType, filterable | Reference to the PaymentMethod. |
| **DepositToAccountRef** | ReferenceType | Account to which payment money is deposited. Query the Account name list resource to determine the appropriate Account object. |
| **UnappliedAmt** | Decimal, read only | Indicates the unapplied amount (if any) that has not been applied to a transaction. |
| **Line** | Line[] | Individual line items of a transaction. |
| **ProcessPayment** | Boolean | Used to indicate that the payment should be processed by merchant account service. |
| **LinkedTxn** | LinkedTxn[] | Zero or more Invoice or CreditMemo transactions linked to this payment. |
| **ExchangeRate** | Decimal | The number of home currency units it takes to equal one unit of currency specified by CurrencyRef. |
| **TxnSource** | String | Used internally to specify originating source of a credit card transaction. |
| **ARAccountRef** | ReferenceType | Reference to the Accounts Receivable account. |
| **PaymentRefNum** | String, filterable | Reference number for the payment, like a check number. |
| **CreditCardPayment** | CreditCardPayment | Credit card payment information. |
| **TxnStatus** | String | Status of the transaction. For payments, possible values are: Pending, Approved, Declined. |
| **MetaData** | ModificationMetaData | Descriptive information about the object. Read only. |

### Sample Object

```json
{
  "Payment": {
    "CustomerRef": {
      "value": "20",
      "name": "Red Rock Diner"
    },
    "DepositToAccountRef": {
      "value": "4"
    },
    "PaymentMethodRef": {
      "value": "1"
    },
    "TotalAmt": 25,
    "UnappliedAmt": 0,
    "ProcessPayment": false,
    "domain": "QBO",
    "sparse": false,
    "Id": "125",
    "SyncToken": "0",
    "MetaData": {
      "CreateTime": "2014-09-16T14:59:48-07:00",
      "LastUpdatedTime": "2014-09-16T14:59:48-07:00"
    },
    "TxnDate": "2014-09-14",
    "CurrencyRef": {
      "value": "USD",
      "name": "United States Dollar"
    },
    "Line": [
      {
        "Amount": 25,
        "LinkedTxn": [
          {
            "TxnId": "67",
            "TxnType": "Invoice"
          }
        ]
      }
    ]
  },
  "time": "2014-09-16T14:59:48.340-07:00"
}
```

## Create a Payment

### Request

```
POST /v3/company/<realmID>/payment
Content-Type: application/json
```

**Production Base URL:** `https://quickbooks.api.intuit.com`
**Sandbox Base URL:** `https://sandbox-quickbooks.api.intuit.com`

### Required Fields

| Attribute | Type | Description |
|-----------|------|-------------|
| **TotalAmt** | Decimal | Total amount of the payment. *Required* |
| **CustomerRef** | ReferenceType | Reference to a customer. *Required* |
| **CurrencyRef** | CurrencyRefType | Required if multicurrency is enabled. *Conditionally required* |

### Sample Request Body (Payment Linked to Invoice)

```json
{
  "TotalAmt": 25,
  "CustomerRef": {
    "value": "20"
  },
  "Line": [
    {
      "Amount": 25,
      "LinkedTxn": [
        {
          "TxnId": "67",
          "TxnType": "Invoice"
        }
      ]
    }
  ]
}
```

### Sample Request Body (Unlinked Payment)

```json
{
  "TotalAmt": 100,
  "CustomerRef": {
    "value": "1"
  }
}
```

### Sample Response

```json
{
  "Payment": {
    "CustomerRef": {
      "value": "20",
      "name": "Red Rock Diner"
    },
    "DepositToAccountRef": {
      "value": "4"
    },
    "TotalAmt": 25,
    "UnappliedAmt": 0,
    "ProcessPayment": false,
    "domain": "QBO",
    "sparse": false,
    "Id": "125",
    "SyncToken": "0",
    "MetaData": {
      "CreateTime": "2014-09-16T14:59:48-07:00",
      "LastUpdatedTime": "2014-09-16T14:59:48-07:00"
    },
    "TxnDate": "2014-09-16",
    "Line": [
      {
        "Amount": 25,
        "LinkedTxn": [
          {
            "TxnId": "67",
            "TxnType": "Invoice"
          }
        ]
      }
    ]
  },
  "time": "2014-09-16T14:59:48.340-07:00"
}
```

## Delete a Payment

This operation deletes the payment object specified in the request body. Include a minimum of Payment.Id and Payment.SyncToken.

### Request

```
POST /v3/company/<realmID>/payment?operation=delete
Content-Type: application/json
```

### Sample Request Body

```json
{
  "Id": "125",
  "SyncToken": "1"
}
```

### Sample Response

```json
{
  "Payment": {
    "status": "Deleted",
    "domain": "QBO",
    "Id": "125"
  },
  "time": "2014-09-16T15:05:22.322-07:00"
}
```

## Void a Payment

Use this operation to void an existing payment object. Include a minimum of Payment.Id and Payment.SyncToken. The transaction remains active but all amounts and quantities are zeroed and the string "Voided" is injected into Payment.PrivateNote.

### Request

```
POST /v3/company/<realmID>/payment?operation=void
Content-Type: application/json
```

### Sample Request Body

```json
{
  "Id": "125",
  "SyncToken": "0"
}
```

### Sample Response

```json
{
  "Payment": {
    "CustomerRef": {
      "value": "20",
      "name": "Red Rock Diner"
    },
    "TotalAmt": 0,
    "UnappliedAmt": 0,
    "PrivateNote": "Voided",
    "domain": "QBO",
    "sparse": false,
    "Id": "125",
    "SyncToken": "1",
    "Line": []
  },
  "time": "2014-09-16T15:10:22.322-07:00"
}
```

## Get a Payment as PDF

Returns the specified object in the response body as an Adobe Portable Document Format (PDF) file.

### Request

```
GET /v3/company/<realmID>/payment/<paymentId>/pdf
Content-Type: application/pdf
```

### Response

Returns binary PDF data.

## Query a Payment

### Request

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content-Type: application/text
```

### Sample Query

```sql
select * from Payment where TotalAmt > '10.00'
```

### Sample Query (with Customer filter)

```sql
select * from Payment where CustomerRef = '20'
```

## Read a Payment

Retrieves the details of a payment that has been previously created.

### Request

```
GET /v3/company/<realmID>/payment/<paymentId>
```

### Sample Response

Returns the full Payment object as shown in the Sample Object section.

## Send a Payment

Sends the payment receipt via email.

### Request

```
POST /v3/company/<realmID>/payment/<paymentId>/send
Content-Type: application/octet-stream
```

Or with explicit email address:

```
POST /v3/company/<realmID>/payment/<paymentId>/send?sendTo=<emailAddr>
```

## Full Update a Payment

Use this operation to update any of the writable fields of an existing payment object. The request body must include all writable fields of the existing object as returned in a read response.

### Request

```
POST /v3/company/<realmID>/payment
Content-Type: application/json
```

### Required Fields

| Attribute | Type | Description |
|-----------|------|-------------|
| **Id** | String | Unique identifier. *Required for update* |
| **SyncToken** | String | Version number. *Required for update* |
| **TotalAmt** | Decimal | Total amount of the payment. *Required* |
| **CustomerRef** | ReferenceType | Reference to a customer. *Required* |

### Sample Request Body

```json
{
  "CustomerRef": {
    "value": "20"
  },
  "TotalAmt": 50,
  "Line": [
    {
      "Amount": 50,
      "LinkedTxn": [
        {
          "TxnId": "67",
          "TxnType": "Invoice"
        }
      ]
    }
  ],
  "Id": "125",
  "SyncToken": "0"
}
```

### Sample Response

Returns the updated Payment object with incremented SyncToken.
