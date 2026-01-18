# BillPayment

A BillPayment object represents the payment transaction for a bill that the business owner receives from a vendor for goods or services purchased from the vendor. QuickBooks Online supports bill payments through a credit card or a checking account.

BillPayment.TotalAmt is the total amount associated with this payment. This includes the total of all the payments from the payment line details. If TotalAmt is greater than the total on the lines being paid, the overpayment is treated as a credit and exposed as such on the QuickBooks UI. The total amount cannot be negative.

## The BillPayment Object

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **Id** | String, filterable, sortable | *Required for update, read only, system defined*. Unique Identifier for an Intuit entity (object). Sort order is ASC by default. |
| **VendorRef** | ReferenceType, filterable, sortable | *Required*. Reference to the vendor for this transaction. Query the Vendor name list resource to determine the appropriate Vendor object for this reference. |
| **Line [0..n]** | Line | *Required*. Individual line items representing zero or more Bill, VendorCredit, and JournalEntry objects linked to this BillPayment object. |
| **TotalAmt** | BigDecimal, filterable, sortable | *Required*. Indicates the total amount associated with this payment. This includes the total of all the payments from the payment line details. If TotalAmt is greater than the total on the lines being paid, the overpayment is treated as a credit. |
| **PayType** | BillPaymentTypeEnum | *Required*. The payment type. Valid values include: Check, CreditCard |
| **SyncToken** | String | *Required for update, read only, system defined*. Version number of the object. It is used to lock an object for use by one app at a time. |
| **CurrencyRef** | CurrencyRefType | *Conditionally required*. Reference to the currency in which all amounts on the associated transaction are expressed. Required if multicurrency is enabled for the company. |
| **DocNumber** | String (max 21 chars), filterable, sortable | *Optional*. Reference number for the transaction. |
| **PrivateNote** | String (max 4000 chars) | *Optional*. User entered, organization-private note about the transaction. |
| **TxnDate** | Date, filterable, sortable | *Optional*. The date entered by the user when this transaction occurred. |
| **ExchangeRate** | Decimal | *Optional*. The number of home currency units it takes to equal one unit of currency specified by CurrencyRef. |
| **APAccountRef** | ReferenceType, filterable, sortable | *Optional*. Specifies to which AP account the bill is credited. |
| **DepartmentRef** | ReferenceType | *Optional*. A reference to a Department object specifying the location of the transaction. |
| **TransactionLocationType** | String | *Optional, minorVersion: 4*. The account location. Valid values include: WithinFrance, FranceOverseas, OutsideFranceWithEU, OutsideEU. For France locales only. |
| **ProcessBillPayment** | Boolean | *Optional*. Indicates that the payment should be processed by merchant account service. Valid for QuickBooks companies with credit card processing. |
| **MetaData** | ModificationMetaData | *Optional*. Descriptive information about the object. The MetaData values are set by Data Services and are read only. |
| **CheckPayment** | BillPaymentCheck, filterable, sortable | Information about a check payment for the transaction. Used when PayType is Check. |
| **CreditCardPayment** | BillPaymentCreditCard, filterable, sortable | Information about a credit card payment for the transaction. Used when PayType is CreditCard. |

### Sample Object

```json
{
  "BillPayment": {
    "SyncToken": "0", 
    "domain": "QBO", 
    "VendorRef": {
      "name": "Bob's Burger Joint", 
      "value": "56"
    }, 
    "TxnDate": "2015-07-14", 
    "TotalAmt": 200.0, 
    "PayType": "Check", 
    "PrivateNote": "Acct. 1JK90", 
    "sparse": false, 
    "Line": [
      {
        "Amount": 200.0, 
        "LinkedTxn": [
          {
            "TxnId": "234", 
            "TxnType": "Bill"
          }
        ]
      }
    ], 
    "Id": "236", 
    "CheckPayment": {
      "PrintStatus": "NeedToPrint", 
      "BankAccountRef": {
        "name": "Checking", 
        "value": "35"
      }
    }, 
    "MetaData": {
      "CreateTime": "2015-07-14T12:34:04-07:00", 
      "LastUpdatedTime": "2015-07-14T12:34:04-07:00"
    }
  }, 
  "time": "2015-07-14T12:34:03.964-07:00"
}
```

## Create a BillPayment

The minimum elements to create a billpayment are listed here.

### Required Attributes

- **VendorRef** - Reference to the vendor for this transaction
- **TotalAmt** - Indicates the total amount associated with this payment
- **Line [0..n]** - Individual line items representing linked Bill, VendorCredit, and JournalEntry objects
- **PayType** - The payment type (Check or CreditCard)
- **CurrencyRef** - *Conditionally required*. Required if multicurrency is enabled
- **CreditCardPayment** - *Conditionally required*. Required when PayType is CreditCard
- **CheckPayment** - *Conditionally required*. Required when PayType is Check

### Request

```
POST /v3/company/<realmID>/billpayment
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body Example

```json
{
  "PrivateNote": "Acct. 1JK90", 
  "VendorRef": {
    "name": "Bob's Burger Joint", 
    "value": "56"
  }, 
  "TotalAmt": 200.0, 
  "PayType": "Check", 
  "Line": [
    {
      "Amount": 200.0, 
      "LinkedTxn": [
        {
          "TxnId": "234", 
          "TxnType": "Bill"
        }
      ]
    }
  ], 
  "CheckPayment": {
    "BankAccountRef": {
      "name": "Checking", 
      "value": "35"
    }
  }
}
```

## Void a BillPayment

Use a sparse update operation with include=void to void an existing BillPayment object; include a minimum of BillPayment.Id and BillPayment.SyncToken. The transaction remains active but all amounts and quantities are zeroed, all lines are cleared, and the string, Voided, is injected into BillPayment.PrivateNote, prepended to existing text if present.

### Request

```
POST /v3/company/<realmID>/billpayment?operation=update&include=void
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body Example

```json
{
  "SyncToken": "0", 
  "Id": "104", 
  "sparse": true
}
```

## Delete a BillPayment

This operation deletes the billpayment object specified in the request body. Include a minimum of BillPayment.Id and BillPayment.SyncToken in the request body.

### Request

```
POST /v3/company/<realmID>/billpayment?operation=delete
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body Example

```json
{
  "SyncToken": "0", 
  "Id": "117"
}
```

### Response Example

```json
{
  "BillPayment": {
    "status": "Deleted", 
    "domain": "QBO", 
    "Id": "117"
  }, 
  "time": "2015-05-26T13:17:25.316-07:00"
}
```

## Query a BillPayment

### Request

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content-Type: application/text
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Sample Query

```sql
select * from billpayment Where Metadata.LastUpdatedTime>'2014-12-12T14:50:22-08:00' Order By Metadata.LastUpdatedTime
```

## Read a BillPayment

Retrieves the details of a billpayment that has been previously created.

### Request

```
GET /v3/company/<realmID>/billpayment/<billpaymentId>
Content-Type: application/text
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

## Full Update a BillPayment

Use this operation to update any of the writable fields of an existing billpayment object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL. The ID of the object to update is specified in the request body.

### Request

```
POST /v3/company/<realmID>/billpayment
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```
