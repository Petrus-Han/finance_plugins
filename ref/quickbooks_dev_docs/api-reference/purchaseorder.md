# PurchaseOrder

The PurchaseOrder object is a non-posting transaction representing a request to purchase goods or services from a third party.

## The PurchaseOrder Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Required for update | Unique identifier for this object. Sort order is ASC by default. Read only, system defined. |
| **APAccountRef** | ReferenceType | Required | Specifies to which AP account the bill is credited. The specified account must have Account.Classification set to Liability and Account.AccountSubType set to AccountsPayable. |
| **VendorRef** | ReferenceType | Required | Reference to the vendor for this transaction. |
| **Line** | Line [0..n] | Required | Individual line items of a transaction. Valid Line types include: ItemBasedExpenseLine and AccountBasedExpenseLine |
| **SyncToken** | String | Required for update | Version number of the object. Read only, system defined. |
| **CurrencyRef** | CurrencyRefType | Conditionally required | Reference to the currency in which all amounts on the associated transaction are expressed. Required if multicurrency is enabled for the company. |
| **GlobalTaxCalculation** | GlobalTaxCalculationEnum | Conditionally required | Method in which tax is applied. Allowed values are: TaxExcluded, TaxInclusive, and NotApplicable. Not applicable to US companies; required for non-US companies. |
| **TxnDate** | Date, filterable, sortable | Optional | The date entered by the user when this transaction occurred. If not supplied, the current date on the server is used. |
| **CustomField** | CustomField | Optional | One of, up to three custom fields for the transaction. |
| **POEmail** | EmailAddress | Optional | Used to specify the vendor e-mail address where the purchase req is sent. Available with minorVersion 17. |
| **ClassRef** | ReferenceType | Optional | Reference to the Class associated with the transaction. |
| **SalesTermRef** | ReferenceType | Optional | Reference to the sales term associated with the transaction. |
| **LinkedTxn** | LinkedTxn [0..n] | Optional | Zero or more Bill objects linked to this purchase order; LinkedTxn.TxnType is set to Bill. |
| **Memo** | String | Optional | A message for the vendor. This text appears on the Purchase Order object sent to the vendor. Max of 4000 chars. |
| **POStatus** | String | Optional | Purchase order status. Valid values are: Open and Closed. |
| **TransactionLocationType** | String | Optional | The account location. For France locales only. Available with minorVersion 4. |
| **DueDate** | Date, filterable, sortable | Optional | Date when the payment of the transaction is due. |
| **MetaData** | ModificationMetaData | Optional | Descriptive information about the object. Read only for all applications. |
| **DocNumber** | String, filterable, sortable | Optional | Reference number for the transaction. Maximum of 21 chars. |
| **PrivateNote** | String | Optional | User entered, organization-private note about the transaction. Max of 4000 chars. |
| **ShipMethodRef** | ReferenceType | Optional | Reference to the user-defined ShipMethod associated with the transaction. |
| **TxnTaxDetail** | TxnTaxDetail | Optional | Information for taxes charged on the transaction as a whole. |
| **ShipTo** | ReferenceType | Optional | Reference to the customer to whose shipping address the order will be shipped to. |
| **ExchangeRate** | Decimal | Optional | The number of home currency units it takes to equal one unit of currency specified by CurrencyRef. |
| **ShipAddr** | PhysicalAddress | Optional | Address to which the vendor shipped or will ship any goods associated with the purchase. |
| **VendorAddr** | PhysicalAddress | Optional | Address to which the payment should be sent. |
| **EmailStatus** | String | Optional | Email status of the purchase order. Valid values: NotSet, NeedToSend, EmailSent. Available with minorVersion 45. |
| **TotalAmt** | BigDecimal | Read only, system defined | Indicates the total amount of the transaction. Calculated by QuickBooks business logic. |
| **RecurDataRef** | ReferenceType | Read only | A reference to the Recurring Transaction template. Available with minorVersion 52. |

### Sample Object

```json
{
  "PurchaseOrder": {
    "DocNumber": "1005",
    "SyncToken": "0",
    "POEmail": {
      "Address": "send_email@intuit.com"
    },
    "APAccountRef": {
      "name": "Accounts Payable (A/P)",
      "value": "33"
    },
    "CurrencyRef": {
      "name": "United States Dollar",
      "value": "USD"
    },
    "TxnDate": "2015-07-28",
    "TotalAmt": 25.0,
    "ShipAddr": {
      "Line4": "Half Moon Bay, CA  94213",
      "Line3": "65 Ocean Dr.",
      "Id": "121",
      "Line1": "Grace Pariente",
      "Line2": "Cool Cars"
    },
    "domain": "QBO",
    "Id": "257",
    "POStatus": "Open",
    "sparse": false,
    "EmailStatus": "NotSet",
    "VendorRef": {
      "name": "Hicks Hardware",
      "value": "41"
    },
    "Line": [
      {
        "DetailType": "ItemBasedExpenseLineDetail",
        "Amount": 25.0,
        "ProjectRef": {
          "value": "39298034"
        },
        "Id": "1",
        "ItemBasedExpenseLineDetail": {
          "ItemRef": {
            "name": "Garden Supplies",
            "value": "38"
          },
          "CustomerRef": {
            "name": "Cool Cars",
            "value": "3"
          },
          "Qty": 1,
          "TaxCodeRef": {
            "value": "NON"
          },
          "BillableStatus": "NotBillable",
          "UnitPrice": 25
        }
      }
    ],
    "CustomField": [
      {
        "DefinitionId": "1",
        "Type": "StringType",
        "Name": "Crew #"
      },
      {
        "DefinitionId": "2",
        "Type": "StringType",
        "Name": "Sales Rep"
      }
    ],
    "VendorAddr": {
      "Line4": "Middlefield, CA  94303",
      "Line3": "42 Main St.",
      "Id": "120",
      "Line1": "Geoff Hicks",
      "Line2": "Hicks Hardware"
    },
    "MetaData": {
      "CreateTime": "2015-07-28T16:01:47-07:00",
      "LastUpdatedTime": "2015-07-28T16:01:47-07:00"
    }
  },
  "time": "2015-07-28T16:04:49.874-07:00"
}
```

## Create a Purchase Order

### Minimum Required Elements

| Attribute | Type | Description |
|-----------|------|-------------|
| **APAccountRef** | ReferenceType | Specifies which AP account to which the bill is credited. Must be a Liability account with sub-type Payables. |
| **VendorRef** | ReferenceType | The vendor reference for this transaction. |
| **Line** | Line [0..n] | Individual line items of a transaction. The ItemRef must reference an Item with an expense account linked to it. |
| **CurrencyRef** | CurrencyRefType | Required if multicurrency is enabled for the company. |

### Request

```
POST /v3/company/<realmID>/purchaseorder
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "TotalAmt": 25.0,
  "Line": [
    {
      "DetailType": "ItemBasedExpenseLineDetail",
      "Amount": 25.0,
      "ProjectRef": {
        "value": "39298034"
      },
      "Id": "1",
      "ItemBasedExpenseLineDetail": {
        "ItemRef": {
          "name": "Pump",
          "value": "11"
        },
        "CustomerRef": {
          "name": "Cool Cars",
          "value": "3"
        },
        "Qty": 1,
        "TaxCodeRef": {
          "value": "NON"
        },
        "BillableStatus": "NotBillable",
        "UnitPrice": 25
      }
    }
  ],
  "APAccountRef": {
    "name": "Accounts Payable (A/P)",
    "value": "33"
  },
  "VendorRef": {
    "name": "Hicks Hardware",
    "value": "41"
  },
  "ShipTo": {
    "name": "Jeff's Jalopies",
    "value": "12"
  }
}
```

### Response

```json
{
  "PurchaseOrder": {
    "DocNumber": "1007",
    "SyncToken": "0",
    "domain": "QBO",
    "VendorRef": {
      "name": "Hicks Hardware",
      "value": "41"
    },
    "TxnDate": "2015-07-28",
    "TotalAmt": 25.0,
    "APAccountRef": {
      "name": "Accounts Payable (A/P)",
      "value": "33"
    },
    "EmailStatus": "NotSet",
    "sparse": false,
    "Line": [
      {
        "DetailType": "ItemBasedExpenseLineDetail",
        "Amount": 25.0,
        "ProjectRef": {
          "value": "39298034"
        },
        "Id": "1",
        "ItemBasedExpenseLineDetail": {
          "ItemRef": {
            "name": "Pump",
            "value": "11"
          },
          "CustomerRef": {
            "name": "Cool Cars",
            "value": "3"
          },
          "Qty": 1,
          "TaxCodeRef": {
            "value": "NON"
          },
          "BillableStatus": "NotBillable",
          "UnitPrice": 25
        }
      }
    ],
    "CustomField": [
      {
        "DefinitionId": "1",
        "Type": "StringType",
        "Name": "Crew #"
      },
      {
        "DefinitionId": "2",
        "Type": "StringType",
        "Name": "Sales Rep"
      }
    ],
    "Id": "259",
    "MetaData": {
      "CreateTime": "2015-07-28T16:06:03-07:00",
      "LastUpdatedTime": "2015-07-28T16:06:03-07:00"
    }
  },
  "time": "2015-07-28T16:06:04.864-07:00"
}
```

## Delete a Purchase Order

This operation deletes the purchaseorder object specified in the request body. Include a minimum of PurchaseOrder.Id and PurchaseOrder.SyncToken in the request body. You must unlink any linked transactions associated with the purchaseorder object before deleting it.

### Request

```
POST /v3/company/<realmID>/purchaseorder?operation=delete
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "SyncToken": "0",
  "Id": "125"
}
```

### Response

```json
{
  "PurchaseOrder": {
    "status": "Deleted",
    "domain": "QBO",
    "Id": "125"
  },
  "time": "2015-05-26T14:08:39.858-07:00"
}
```

## Get a Purchase Order as PDF

Returns the specified object in the response body as an Adobe Portable Document Format (PDF) file. The resulting PDF file is formatted according to custom form styles in the company settings.

### Request

```
GET /v3/company/<realmID>/purchaseorder/<purchaseorderId>/pdf
Content-Type: application/pdf
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

## Query a Purchase Order

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
select * from PurchaseOrder where Id = '259'
```

## Read a Purchase Order

Retrieves the details of a purchase order that has been previously created.

### Request

```
GET /v3/company/<realmID>/purchaseorder/<purchaseorderId>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

## Send a Purchase Order

Sends the purchase order via email to the vendor.

The following actions occur:
- The PurchaseOrder.EmailStatus parameter is set to EmailSent
- The PurchaseOrder.POEmail.Address parameter is updated to the address specified with the value of the sendTo query parameter, if specified and if the request's minor version is 17 and above.

### Request

```
POST /v3/company/<realmID>/purchaseorder/<purchaseorderId>/send
Content-Type: application/octet-stream
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

To specify an explicit email address:
```
POST /v3/company/<realmID>/purchaseorder/<purchaseorderId>/send?sendTo=<emailAddr>
```

## Full Update a Purchase Order

Use this operation to update any of the writable fields of an existing purchase order object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL. The ID of the object to update is specified in the request body.

### Request

```
POST /v3/company/<realmID>/purchaseorder
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body Example

```json
{
  "DocNumber": "1005",
  "SyncToken": "0",
  "POEmail": {
    "Address": "send_email@intuit.com"
  },
  "APAccountRef": {
    "name": "Accounts Payable (A/P)",
    "value": "33"
  },
  "CurrencyRef": {
    "name": "United States Dollar",
    "value": "USD"
  },
  "sparse": false,
  "TxnDate": "2015-07-28",
  "TotalAmt": 25.0,
  "ShipAddr": {
    "Line4": "Half Moon Bay, CA  94213",
    "Line3": "65 Ocean Dr.",
    "Id": "121",
    "Line1": "Grace Pariente",
    "Line2": "Cool Cars"
  },
  "PrivateNote": "This is a private note added during update.",
  "Id": "257",
  "POStatus": "Open",
  "domain": "QBO",
  "VendorRef": {
    "name": "Hicks Hardware",
    "value": "41"
  },
  "Line": [
    {
      "DetailType": "ItemBasedExpenseLineDetail",
      "Amount": 25.0,
      "ProjectRef": {
        "value": "39298034"
      },
      "Id": "1",
      "ItemBasedExpenseLineDetail": {
        "ItemRef": {
          "name": "Garden Supplies",
          "value": "38"
        },
        "CustomerRef": {
          "name": "Cool Cars",
          "value": "3"
        },
        "Qty": 1,
        "TaxCodeRef": {
          "value": "NON"
        },
        "BillableStatus": "NotBillable",
        "UnitPrice": 25
      }
    }
  ],
  "CustomField": [
    {
      "DefinitionId": "1",
      "Type": "StringType",
      "Name": "Crew #"
    },
    {
      "DefinitionId": "2",
      "Type": "StringType",
      "Name": "Sales Rep"
    }
  ],
  "VendorAddr": {
    "Line4": "Middlefield, CA  94303",
    "Line3": "42 Main St.",
    "Id": "120",
    "Line1": "Geoff Hicks",
    "Line2": "Hicks Hardware"
  },
  "MetaData": {
    "CreateTime": "2015-07-28T16:01:47-07:00",
    "LastUpdatedTime": "2015-07-28T16:01:47-07:00"
  }
}
```
