# Bill

A Bill object is an AP transaction representing a request-for-payment from a third party for goods/services rendered, received, or both.

## The Bill Object

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **Id** | String, filterable, sortable | *Required for update, read only, system defined*. Unique identifier for this object. Sort order is ASC by default. |
| **VendorRef** | ReferenceType, filterable, sortable | *Required*. Reference to the vendor for this transaction. Query the Vendor name list resource to determine the appropriate Vendor object for this reference. Use Vendor.Id and Vendor.Name from that object for VendorRef.value and VendorRef.name, respectively. |
| **Line [0..n]** | Line | *Required*. Individual line items of a transaction. Valid Line types include: ItemBasedExpenseLine and AccountBasedExpenseLine |
| **SyncToken** | String | *Required for update, read only, system defined*. Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. |
| **CurrencyRef** | CurrencyRefType | *Conditionally required*. Reference to the currency in which all amounts on the associated transaction are expressed. This must be defined if multicurrency is enabled for the company. Multicurrency is enabled for the company if Preferences.MultiCurrencyEnabled is set to true. Required if multicurrency is enabled for the company. |
| **GlobalTaxCalculation** | GlobalTaxCalculationEnum | *Conditionally required*. Method in which tax is applied. Allowed values are: TaxExcluded, TaxInclusive, and NotApplicable. Not applicable to US companies; required for non-US companies. |
| **TxnDate** | Date, filterable, sortable | *Optional*. The date entered by the user when this transaction occurred. For posting transactions, this is the posting date that affects the financial statements. If the date is not supplied, the current date on the server is used. Sort order is ASC by default. |
| **APAccountRef** | ReferenceType, filterable, sortable | *Optional*. Specifies to which AP account the bill is credited. Query the Account name list resource to determine the appropriate Account object for this reference. Use Account.Id and Account.Name from that object for APAccountRef.value and APAccountRef.name, respectively. The specified account must have Account.Classification set to Liability and Account.AccountSubType set to AccountsPayable. |
| **SalesTermRef** | ReferenceType, filterable, sortable | *Optional*. Reference to the Term associated with the transaction. Query the Term name list resource to determine the appropriate Term object for this reference. |
| **LinkedTxn [0..n]** | LinkedTxn | *Optional*. Zero or more transactions linked to this Bill object. The LinkedTxn.TxnType can be set to PurchaseOrder, BillPaymentCheck or if using Minor Version 55 and above ReimburseCharge. Use LinkedTxn.TxnId as the ID of the transaction. |
| **TotalAmt** | BigDecimal, filterable, sortable | *Optional, read only*. Indicates the total amount of the transaction. This includes the total of all the charges, allowances, and taxes. Calculated by QuickBooks business logic; any value you supply is over-written by QuickBooks. |
| **TransactionLocationType** | String | *Optional, minorVersion: 4*. The account location. Valid values include: WithinFrance, FranceOverseas, OutsideFranceWithEU, OutsideEU. For France locales, only. |
| **DueDate** | Date, filterable, sortable | *Optional*. Date when the payment of the transaction is due. If date is not provided, the number of days specified in SalesTermRef added the transaction date will be used. |
| **MetaData** | ModificationMetaData | *Optional*. Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications. |
| **DocNumber** | String (max 21 chars), filterable, sortable | *Optional*. Reference number for the transaction. If not explicitly provided at create time, a custom value can be provided. If no value is supplied, the resulting DocNumber is null. Throws an error when duplicate DocNumber is sent in the request. |
| **PrivateNote** | String (max 4000 chars) | *Optional*. User entered, organization-private note about the transaction. This note does not appear on the invoice to the customer. This field maps to the Memo field on the Invoice form. |
| **TxnTaxDetail** | TxnTaxDetail | *Optional*. This data type provides information for taxes charged on the transaction as a whole. It captures the details of all taxes calculated for the transaction based on the tax codes referenced by the transaction. |
| **ExchangeRate** | Decimal | *Optional*. The number of home currency units it takes to equal one unit of currency specified by CurrencyRef. Applicable if multicurrency is enabled for the company. |
| **DepartmentRef** | ReferenceType | *Optional*. A reference to a Department object specifying the location of the transaction, as defined using location tracking in QuickBooks Online. |
| **IncludeInAnnualTPAR** | Boolean | *Optional, minorVersion: 40*. Include the supplier in the annual TPAR. TPAR stands for Taxable Payments Annual Report. |
| **HomeBalance** | Decimal | *Read only, minorVersion: 3*. Convenience field containing the amount in Balance expressed in terms of the home currency. Calculated by QuickBooks business logic. |
| **RecurDataRef** | ReferenceType | *Read only, minorVersion: 52*. A reference to the Recurring Transaction. It captures what recurring transaction template the Bill was created from. |
| **Balance** | Decimal, filterable | *Read only*. The balance reflecting any payments made against the transaction. Initially set to the value of TotalAmt. A Balance of 0 indicates the bill is fully paid. |

### Sample Object

```json
{
  "Bill": {
    "SyncToken": "2", 
    "domain": "QBO", 
    "APAccountRef": {
      "name": "Accounts Payable (A/P)", 
      "value": "33"
    }, 
    "VendorRef": {
      "name": "Norton Lumber and Building Materials", 
      "value": "46"
    }, 
    "TxnDate": "2014-11-06", 
    "TotalAmt": 103.55, 
    "CurrencyRef": {
      "name": "United States Dollar", 
      "value": "USD"
    }, 
    "LinkedTxn": [
      {
        "TxnId": "118", 
        "TxnType": "BillPaymentCheck"
      }
    ], 
    "SalesTermRef": {
      "value": "3"
    }, 
    "DueDate": "2014-12-06", 
    "sparse": false, 
    "Line": [
      {
        "Description": "Lumber", 
        "DetailType": "AccountBasedExpenseLineDetail", 
        "ProjectRef": {
          "value": "39298034"
        }, 
        "Amount": 103.55, 
        "Id": "1", 
        "AccountBasedExpenseLineDetail": {
          "TaxCodeRef": {
            "value": "TAX"
          }, 
          "AccountRef": {
            "name": "Job Expenses:Job Materials:Decks and Patios", 
            "value": "64"
          }, 
          "BillableStatus": "Billable", 
          "CustomerRef": {
            "name": "Travis Waldron", 
            "value": "26"
          }
        }
      }
    ], 
    "Balance": 0, 
    "Id": "25", 
    "MetaData": {
      "CreateTime": "2014-11-06T15:37:25-08:00", 
      "LastUpdatedTime": "2015-02-09T10:11:11-08:00"
    }
  }, 
  "time": "2015-02-09T10:17:20.251-08:00"
}
```

## Create a Bill

The minimum elements to create a bill are listed here.

### Required Attributes

- **VendorRef** - Reference to the vendor for this transaction
- **Line [0..n]** - The minimum line item required for the request
- **CurrencyRef** - *Conditionally required*. Required if multicurrency is enabled for the company

### Request

```
POST /v3/company/<realmID>/bill
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body Example

```json
{
  "Line": [
    {
      "DetailType": "AccountBasedExpenseLineDetail", 
      "Amount": 200.0, 
      "Id": "1", 
      "AccountBasedExpenseLineDetail": {
        "AccountRef": {
          "value": "7"
        }
      }
    }
  ], 
  "VendorRef": {
    "value": "56"
  }
}
```

### Response Example

```json
{
  "Bill": {
    "SyncToken": "0", 
    "domain": "QBO", 
    "VendorRef": {
      "name": "Bob's Burger Joint", 
      "value": "56"
    }, 
    "TxnDate": "2014-12-31", 
    "TotalAmt": 200.0, 
    "APAccountRef": {
      "name": "Accounts Payable (A/P)", 
      "value": "33"
    }, 
    "Id": "151", 
    "sparse": false, 
    "Line": [
      {
        "DetailType": "AccountBasedExpenseLineDetail", 
        "Amount": 200.0, 
        "Id": "1", 
        "AccountBasedExpenseLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          }, 
          "AccountRef": {
            "name": "Advertising", 
            "value": "7"
          }, 
          "BillableStatus": "NotBillable"
        }
      }
    ], 
    "Balance": 200.0, 
    "DueDate": "2014-12-31", 
    "MetaData": {
      "CreateTime": "2014-12-31T09:59:18-08:00", 
      "LastUpdatedTime": "2014-12-31T09:59:18-08:00"
    }
  }, 
  "time": "2014-12-31T09:59:17.449-08:00"
}
```

## Delete a Bill

This operation deletes the bill object specified in the request body. Include a minimum of Bill.Id and Bill.SyncToken in the request body. You must unlink any linked transactions associated with the bill object before deleting it.

### Required Attributes

- **SyncToken** - Version number of the object
- **Id** - Unique identifier for this object

### Request

```
POST /v3/company/<realmID>/bill?operation=delete
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body Example

```json
{
  "SyncToken": "0", 
  "Id": "108"
}
```

### Response Example

```json
{
  "Bill": {
    "status": "Deleted", 
    "domain": "QBO", 
    "Id": "108"
  }, 
  "time": "2015-05-26T13:14:34.775-07:00"
}
```

## Query a Bill

### Request

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content-Type: application/text
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Sample Query

```sql
select * from bill maxresults 2
```

### Response Example

```json
{
  "QueryResponse": {
    "startPosition": 1, 
    "totalCount": 2, 
    "Bill": [
      {
        "SyncToken": "2", 
        "domain": "QBO", 
        "VendorRef": {
          "name": "Norton Lumber and Building Materials", 
          "value": "46"
        }, 
        "TxnDate": "2014-10-07", 
        "TotalAmt": 225.0, 
        "APAccountRef": {
          "name": "Accounts Payable (A/P)", 
          "value": "33"
        }, 
        "Id": "150", 
        "sparse": false, 
        "Line": [
          {
            "DetailType": "ItemBasedExpenseLineDetail", 
            "Amount": 100.0, 
            "Id": "1", 
            "ItemBasedExpenseLineDetail": {
              "TaxCodeRef": {
                "value": "NON"
              }, 
              "Qty": 8, 
              "BillableStatus": "NotBillable", 
              "UnitPrice": 10, 
              "ItemRef": {
                "name": "Pump", 
                "value": "11"
              }
            }, 
            "Description": "Fountain Pump"
          }
        ], 
        "Balance": 225.0, 
        "DueDate": "2014-10-07", 
        "MetaData": {
          "CreateTime": "2014-10-15T13:55:31-07:00", 
          "LastUpdatedTime": "2014-10-15T14:24:54-07:00"
        }
      }
    ], 
    "maxResults": 2
  }, 
  "time": "2014-10-15T14:41:39.98-07:00"
}
```

## Read a Bill

Retrieves the details of a bill that has been previously created.

### Request

```
GET /v3/company/<realmID>/bill/<billId>
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

## Full Update a Bill

Use this operation to update any of the writable fields of an existing bill object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL. The ID of the object to update is specified in the request body.

### Request

```
POST /v3/company/<realmID>/bill
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body Example

```json
{
  "DocNumber": "56789", 
  "SyncToken": "1", 
  "domain": "QBO", 
  "APAccountRef": {
    "name": "Accounts Payable", 
    "value": "49"
  }, 
  "VendorRef": {
    "name": "Bayshore CalOil Service", 
    "value": "81"
  }, 
  "TxnDate": "2014-04-04", 
  "TotalAmt": 200.0, 
  "CurrencyRef": {
    "name": "United States Dollar", 
    "value": "USD"
  }, 
  "PrivateNote": "This is a updated memo.", 
  "SalesTermRef": {
    "value": "12"
  }, 
  "DepartmentRef": {
    "name": "Garden Services", 
    "value": "1"
  }, 
  "DueDate": "2013-06-09", 
  "sparse": false, 
  "Line": [
    {
      "Description": "Gasoline", 
      "DetailType": "AccountBasedExpenseLineDetail", 
      "ProjectRef": {
        "value": "39298034"
      }, 
      "Amount": 200.0, 
      "Id": "1", 
      "AccountBasedExpenseLineDetail": {
        "TaxCodeRef": {
          "value": "TAX"
        }, 
        "AccountRef": {
          "name": "Automobile", 
          "value": "75"
        }, 
        "BillableStatus": "Billable", 
        "CustomerRef": {
          "name": "Blackwell, Edward", 
          "value": "20"
        }, 
        "MarkupInfo": {
          "Percent": 10
        }
      }
    }
  ], 
  "Balance": 200.0, 
  "Id": "890", 
  "MetaData": {
    "CreateTime": "2014-04-04T12:38:01-07:00", 
    "LastUpdatedTime": "2014-04-04T12:48:56-07:00"
  }
}
```
