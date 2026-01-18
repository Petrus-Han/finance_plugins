# SalesReceipt

A SalesReceipt object represents the sales receipt that is given to a customer. A sales receipt is similar to an invoice. However, for a sales receipt, payment is received as part of the sale of goods and services. The sales receipt specifies a deposit account where the customer's payment is deposited. If the deposit account is not specified, the Undeposited Account is used.

## The SalesReceipt Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Required for update | Unique identifier for this object. Sort order is ASC by default. Read only, system defined. |
| **Line** | Line [0..n] | Required | Individual line items of a transaction. Valid Line types include: SalesItemLine, GroupLine, DescriptionOnlyLine, DiscountLine and SubTotalLine (read-only). If the transaction is taxable there is a limit of 750 lines per transaction. |
| **CustomerRef** | ReferenceType, filterable | Required | Reference to a customer or job. Query the Customer name list resource to determine the appropriate Customer object for this reference. |
| **SyncToken** | String | Required for update | Version number of the object. Read only, system defined. |
| **ShipFromAddr** | PhysicalAddress | Conditionally required | Identifies the address where the goods are shipped from. Required for accurate sales tax calculation when automated sales tax is enabled. Available with minorVersion 35. |
| **CurrencyRef** | CurrencyRefType | Conditionally required | Reference to the currency in which all amounts on the associated transaction are expressed. Required if multicurrency is enabled for the company. |
| **GlobalTaxCalculation** | GlobalTaxCalculationEnum | Conditionally required | Method in which tax is applied. Allowed values are: TaxExcluded, TaxInclusive, and NotApplicable. Not applicable to US companies; required for non-US companies. |
| **ProjectRef** | ReferenceType, filterable | Conditionally required | Reference to the Project ID associated with this transaction. Available with Minor Version 69 and above. |
| **BillEmail** | EmailAddress | Conditionally required | Identifies the e-mail address where the invoice is sent. Required if EmailStatus=NeedToSend. |
| **TxnDate** | Date, filterable, sortable | Optional | The date entered by the user when this transaction occurred. If not supplied, the current date on the server is used. |
| **CustomField** | CustomField | Optional | One of, up to three custom fields for the transaction. |
| **ShipDate** | Date | Optional | Ship date for the transaction. |
| **TrackingNum** | String | Optional | Shipping provider's tracking number for the delivery. |
| **ClassRef** | ReferenceType | Optional | Reference to the Class associated with the transaction. |
| **PrintStatus** | String | Optional | Printing status of the sales receipt. Valid values: NotSet, NeedToPrint, PrintComplete. |
| **PaymentRefNum** | String | Optional | The reference number for the payment received. Max 21 characters. |
| **TxnSource** | String | Optional | Used internally to specify originating source of a credit card transaction. |
| **LinkedTxn** | LinkedTxn [0..n] | Optional | Zero or more related transactions to this sales receipt object. |
| **TransactionLocationType** | String | Optional | The account location. For France locales. Available with minorVersion 4. |
| **ApplyTaxAfterDiscount** | Boolean | Optional | If false or null, calculate the sales tax first, then apply the discount. US versions only. |
| **DocNumber** | String, filterable, sortable | Optional | Reference number for the transaction. Maximum of 21 chars. |
| **PrivateNote** | String | Optional | User entered, organization-private note. Max of 4000 chars. |
| **DepositToAccountRef** | ReferenceType | Optional | Account to which payment money is deposited. If not specified, payment is applied to the Undeposited Funds account. |
| **CustomerMemo** | MemoRef | Optional | User-entered message to the customer; visible to end user on their transactions. |
| **EmailStatus** | String | Optional | Email status of the receipt. Valid values: NotSet, NeedToSend, EmailSent. |
| **CreditCardPayment** | CreditCardPayment | Optional | Information about a credit card payment for the transaction. |
| **TxnTaxDetail** | TxnTaxDetail | Optional | Information for taxes charged on the transaction as a whole. |
| **PaymentMethodRef** | ReferenceType | Optional | Reference to a PaymentMethod associated with this transaction. |
| **ExchangeRate** | Decimal | Optional | The number of home currency units it takes to equal one unit of currency specified by CurrencyRef. |
| **ShipAddr** | PhysicalAddress | Optional | Identifies the address where the goods must be shipped. |
| **DepartmentRef** | ReferenceType | Optional | A reference to a Department object specifying the location of the transaction. |
| **ShipMethodRef** | ReferenceType | Optional | Reference to the ShipMethod associated with the transaction. |
| **BillAddr** | PhysicalAddress | Optional | Bill-to address of the sales receipt. |
| **MetaData** | ModificationMetaData | Optional | Descriptive information about the object. Read only for all applications. |
| **HomeBalance** | Decimal | Read only | Convenience field containing the amount in Balance expressed in terms of the home currency. Available with minorVersion 3. |
| **DeliveryInfo** | DeliveryInfo | Read only | Email delivery information. Returned when a request has been made to deliver email with the send operation. |
| **RecurDataRef** | ReferenceType | Read only | A reference to the Recurring Transaction template. Available with minorVersion 52. |
| **TotalAmt** | BigDecimal, filterable | Read only, system defined | Indicates the total amount of the transaction. |
| **Balance** | Decimal, filterable, sortable | Read only | The balance reflecting any payments made against the transaction. |
| **HomeTotalAmt** | Decimal | Read only, system defined | Total amount of the transaction in the home currency. |
| **FreeFormAddress** | Boolean | System defined | Denotes how ShipAddr is stored: formatted or unformatted. |

### Sample Object

```json
{
  "SalesReceipt": {
    "TxnDate": "2014-09-14",
    "domain": "QBO",
    "PrintStatus": "NotSet",
    "PaymentRefNum": "10264",
    "TotalAmt": 337.5,
    "Line": [
      {
        "Description": "Custom Design",
        "DetailType": "SalesItemLineDetail",
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
          "Qty": 4.5,
          "UnitPrice": 75,
          "ItemRef": {
            "name": "Design",
            "value": "4"
          }
        },
        "LineNum": 1,
        "Amount": 337.5,
        "Id": "1"
      },
      {
        "DetailType": "SubTotalLineDetail",
        "Amount": 337.5,
        "SubTotalLineDetail": {}
      }
    ],
    "ApplyTaxAfterDiscount": false,
    "DocNumber": "1003",
    "sparse": false,
    "DepositToAccountRef": {
      "name": "Checking",
      "value": "35"
    },
    "CustomerMemo": {
      "value": "Thank you for your business and have a great day!"
    },
    "ProjectRef": {
      "value": "39298243"
    },
    "Balance": 0,
    "CustomerRef": {
      "name": "Dylan Sollfrank",
      "value": "6"
    },
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "SyncToken": "0",
    "PaymentMethodRef": {
      "name": "Check",
      "value": "2"
    },
    "EmailStatus": "NotSet",
    "BillAddr": {
      "Lat": "INVALID",
      "Long": "INVALID",
      "Id": "49",
      "Line1": "Dylan Sollfrank"
    },
    "MetaData": {
      "CreateTime": "2014-09-16T14:59:48-07:00",
      "LastUpdatedTime": "2014-09-16T14:59:48-07:00"
    },
    "CustomField": [
      {
        "DefinitionId": "1",
        "Type": "StringType",
        "Name": "Crew #"
      }
    ],
    "Id": "11"
  },
  "time": "2015-07-29T09:29:56.229-07:00"
}
```

## Create a SalesReceipt

A SalesReceipt object must have at least one line that describes an item and an amount.

### Minimum Required Elements

| Attribute | Type | Description |
|-----------|------|-------------|
| **Line** | Line [0..n] | The minimum line item required for the request is one of the following: SalesItemLine and GroupLine |
| **CurrencyRef** | CurrencyRefType | Required if multicurrency is enabled for the company. |
| **ProjectRef** | ReferenceType | Available with Minor Version 69 and above. |

### Request

```
POST /v3/company/<realmID>/salesreceipt
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "Line": [
    {
      "Description": "Pest Control Services",
      "DetailType": "SalesItemLineDetail",
      "SalesItemLineDetail": {
        "TaxCodeRef": {
          "value": "NON"
        },
        "Qty": 1,
        "UnitPrice": 35,
        "ItemRef": {
          "name": "Pest Control",
          "value": "10"
        }
      },
      "LineNum": 1,
      "Amount": 35.0,
      "Id": "1"
    }
  ]
}
```

### Response

```json
{
  "SalesReceipt": {
    "DocNumber": "1074",
    "SyncToken": "0",
    "domain": "QBO",
    "Balance": 0,
    "DepositToAccountRef": {
      "name": "Undeposited Funds",
      "value": "4"
    },
    "TxnDate": "2015-07-29",
    "TotalAmt": 35.0,
    "PrintStatus": "NeedToPrint",
    "EmailStatus": "NotSet",
    "sparse": false,
    "Line": [
      {
        "Description": "Pest Control Services",
        "DetailType": "SalesItemLineDetail",
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
          "Qty": 1,
          "UnitPrice": 35,
          "ItemRef": {
            "name": "Pest Control",
            "value": "10"
          }
        },
        "LineNum": 1,
        "Amount": 35.0,
        "Id": "1"
      },
      {
        "DetailType": "SubTotalLineDetail",
        "Amount": 35.0,
        "SubTotalLineDetail": {}
      }
    ],
    "ApplyTaxAfterDiscount": false,
    "CustomField": [
      {
        "DefinitionId": "1",
        "Type": "StringType",
        "Name": "Crew #"
      }
    ],
    "Id": "263",
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "MetaData": {
      "CreateTime": "2015-07-29T09:25:02-07:00",
      "LastUpdatedTime": "2015-07-29T09:25:02-07:00"
    }
  },
  "time": "2015-07-29T09:25:04.214-07:00"
}
```

## Delete a SalesReceipt

This operation deletes the SalesReceipt object specified in the request body. Include a minimum of SalesReceipt.Id and SalesReceipt.SyncToken in the request body.

### Request

```
POST /v3/company/<realmID>/salesreceipt?operation=delete
Content-Type: application/json or application/xml
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "SyncToken": "1",
  "Id": "98"
}
```

### Response

```json
{
  "SalesReceipt": {
    "status": "Deleted",
    "domain": "QBO",
    "Id": "98"
  },
  "time": "2013-03-13T13:39:58.505-07:00"
}
```

## Void a SalesReceipt

Use a sparse update operation with include=void to void an existing SalesReceipt object; include a minimum of SalesReceipt.Id and SalesReceipt.SyncToken. The transaction remains active but all amounts and quantities are zeroed and the string, Voided, is injected into SalesReceipt.PrivateNote. If a sales receipt is paid and funds have been deposited, you must delete the associated deposit object before voiding the salesreceipt object.

### Request

```
POST /v3/company/<realmID>/salesreceipt?operation=update&include=void
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "SyncToken": "0",
  "Id": "161",
  "sparse": true
}
```

### Response

```json
{
  "SalesReceipt": {
    "TxnDate": "2014-12-31",
    "domain": "QBO",
    "PrintStatus": "NeedToPrint",
    "TotalAmt": 0,
    "Line": [
      {
        "LineNum": 1,
        "Amount": 0,
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
          "Qty": 0,
          "ItemRef": {
            "name": "Services",
            "value": "1"
          }
        },
        "Id": "1",
        "DetailType": "SalesItemLineDetail"
      },
      {
        "DetailType": "SubTotalLineDetail",
        "Amount": 0,
        "SubTotalLineDetail": {}
      }
    ],
    "ApplyTaxAfterDiscount": false,
    "DocNumber": "1038",
    "PrivateNote": "Voided",
    "sparse": false,
    "Balance": 0,
    "SyncToken": "1",
    "Id": "161"
  },
  "time": "2015-02-09T12:29:52.970-08:00"
}
```

## Get a SalesReceipt as PDF

Returns the specified object in the response body as an Adobe Portable Document Format (PDF) file. The resulting PDF file is formatted according to custom form styles in the company settings.

### Request

```
GET /v3/company/<realmID>/salesreceipt/<salesreceiptId>/pdf
Content-Type: application/pdf
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

## Query a SalesReceipt

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
select * from SalesReceipt where id='11'
```

## Read a SalesReceipt

Retrieves the details of a SalesReceipt object that has been previously created.

### Request

```
GET /v3/company/<realmID>/salesreceipt/<salesreceiptId>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

## Send a SalesReceipt

Sends the sales receipt via email to the customer.

The following actions occur:
- The SalesReceipt.EmailStatus parameter is set to EmailSent.
- The SalesReceipt.DeliveryInfo element is populated with sending information.
- The SalesReceipt.BillEmail.Address parameter is updated to the address specified with the value of the sendTo query parameter, if specified.

### Request

```
POST /v3/company/<realmID>/salesreceipt/<salesreceiptId>/send
Content-Type: application/octet-stream
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

To specify an explicit email address:
```
POST /v3/company/<realmID>/salesreceipt/<salesreceiptId>/send?sendTo=<emailAddr>
```

## Full Update a SalesReceipt

Use this operation to update any of the writable fields of an existing SalesReceipt object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL.

### Request

```
POST /v3/company/<realmID>/salesreceipt
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

## Sparse Update a SalesReceipt

Sparse updating provides the ability to update a subset of properties for a given object; only elements specified in the request are updated. Missing elements are left untouched.

### Request

```
POST /v3/company/<realmID>/salesreceipt
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "sparse": true,
  "Id": "11",
  "SyncToken": "2",
  "CustomerMemo": {
    "value": "Updated customer memo via sparse update operation."
  }
}
```
