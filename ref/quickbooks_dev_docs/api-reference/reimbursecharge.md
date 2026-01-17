# ReimburseCharge

A Reimburse Charge is a billable Expense. This happens when you mark your Expense/Bill lines as Billable to some customer to be invoiced later.

## The ReimburseCharge Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Optional | Unique identifier for this object. Sort order is ASC by default. Read only, system defined. |
| **Line** | Line | Required | Line items for the reimbursable charge. |
| **Amount** | Decimal (max 15 digits in 10.5 format) | Required | The amount of the line item. |
| **CustomerRef** | ReferenceType, filterable | Required | Reference to a customer or job. Query the Customer name list resource to determine the appropriate Customer object for this reference. Use Customer.Id and Customer.DisplayName from that object for CustomerRef.value and CustomerRef.name, respectively. |
| **SyncToken** | String | Required for update | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. Read only, system defined. |
| **CurrencyRef** | CurrencyRefType | Conditionally required | Reference to the currency in which all amounts on the associated transaction are expressed. This must be defined if multicurrency is enabled for the company. Multicurrency is enabled for the company if Preferences.MultiCurrencyEnabled is set to true. Applicable if multicurrency is enabled for the company. |
| **PrivateNote** | String (max 4000 chars) | Optional | User entered, organization-private note about the transaction. This note does not appear on the invoice to the customer. This field maps to the Statement Memo field on the Invoice form in the QuickBooks Online UI. |
| **LinkedTxn** | LinkedTxn | Optional | The LinkedTxn will contain the Invoice Id if the ReimburseCharge has been linked with an Invoice. |
| **ExchangeRate** | Decimal | Optional | The number of home currency units it takes to equal one unit of currency specified by CurrencyRef. Applicable if multicurrency is enabled for the company. |
| **MetaData** | ModificationMetaData | Optional | Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications. |
| **HasBeenInvoiced** | Boolean, filterable | - | Boolean indicating whether the reimbursable charge has been linked to an Invoice. |
| **HomeTotalAmt** | Decimal | Read only | Total amount of the transaction in the home currency. Includes the total of all the charges, allowances and taxes. Calculated by QuickBooks business logic. Value is valid only when CurrencyRef is specified. Applicable if multicurrency is enabled for the company. System defined. |

### ReimburseLineDetail Object

| Attribute | Type | Description |
|-----------|------|-------------|
| **ItemRef** | ReferenceType | Reference to the Item. |
| **Qty** | Decimal | Quantity. |
| **TaxCodeRef** | ReferenceType | Reference to TaxCode. |
| **MarkupInfo** | Object | Contains markup percentage. |
| **ItemAccountRef** | ReferenceType | Reference to the account associated with the item. |
| **UnitPrice** | Decimal | Unit price. |

### Sample Object

```json
{
  "ReimburseCharge": {
    "SyncToken": "0",
    "domain": "QBO",
    "HasBeenInvoiced": true,
    "TxnDate": "2020-06-23",
    "CurrencyRef": {
      "name": "United States Dollar",
      "value": "USD"
    },
    "LinkedTxn": [
      {
        "TxnId": "495",
        "TxnType": "Invoice"
      }
    ],
    "Amount": 100.0,
    "sparse": false,
    "Line": [
      {
        "LinkedTxn": [
          {
            "TxnId": "495",
            "TxnType": "Invoice"
          }
        ],
        "DetailType": "ReimburseLineDetail",
        "ReimburseLineDetail": {
          "ItemRef": {
            "name": "Sales",
            "value": "3"
          },
          "Qty": 1,
          "TaxCodeRef": {
            "value": "NON"
          },
          "MarkupInfo": {
            "Percent": 900
          },
          "ItemAccountRef": {
            "name": "Billable Expense Income",
            "value": "37"
          },
          "UnitPrice": 10
        },
        "LineNum": 1,
        "Amount": 10.0,
        "Id": "1"
      },
      {
        "LinkedTxn": [
          {
            "TxnId": "495",
            "TxnType": "Invoice"
          }
        ],
        "Description": "900% markup",
        "DetailType": "ReimburseLineDetail",
        "ReimburseLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
          "MarkupInfo": {
            "Percent": 900
          },
          "ItemAccountRef": {
            "name": "Markup",
            "value": "49"
          }
        },
        "LineNum": 2,
        "Amount": 90.0,
        "Id": "2"
      }
    ],
    "CustomerRef": {
      "name": "Cust1",
      "value": "1"
    },
    "Id": "491",
    "MetaData": {
      "CreateTime": "2020-06-23T23:26:13-07:00",
      "LastUpdatedTime": "2020-06-23T23:28:54-07:00"
    }
  },
  "time": "2020-11-07T13:29:41.836-07:00"
}
```

## Read a ReimburseCharge

Retrieves the details of a ReimburseCharge object.

### Request

```
GET /v3/company/<realmID>/reimbursecharge/<reimbursechargeId>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

Returns the ReimburseCharge object.

```json
{
  "ReimburseCharge": {
    "SyncToken": "0",
    "domain": "QBO",
    "HasBeenInvoiced": true,
    "TxnDate": "2020-06-23",
    "CurrencyRef": {
      "name": "United States Dollar",
      "value": "USD"
    },
    "LinkedTxn": [
      {
        "TxnId": "495",
        "TxnType": "Invoice"
      }
    ],
    "Amount": 100.0,
    "sparse": false,
    "Line": [
      {
        "LinkedTxn": [
          {
            "TxnId": "495",
            "TxnType": "Invoice"
          }
        ],
        "DetailType": "ReimburseLineDetail",
        "ReimburseLineDetail": {
          "ItemRef": {
            "name": "Sales",
            "value": "3"
          },
          "Qty": 1,
          "TaxCodeRef": {
            "value": "NON"
          },
          "MarkupInfo": {
            "Percent": 900
          },
          "ItemAccountRef": {
            "name": "Billable Expense Income",
            "value": "37"
          },
          "UnitPrice": 10
        },
        "LineNum": 1,
        "Amount": 10.0,
        "Id": "1"
      },
      {
        "LinkedTxn": [
          {
            "TxnId": "495",
            "TxnType": "Invoice"
          }
        ],
        "Description": "900% markup",
        "DetailType": "ReimburseLineDetail",
        "ReimburseLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
          "MarkupInfo": {
            "Percent": 900
          },
          "ItemAccountRef": {
            "name": "Markup",
            "value": "49"
          }
        },
        "LineNum": 2,
        "Amount": 90.0,
        "Id": "2"
      }
    ],
    "CustomerRef": {
      "name": "Cust1",
      "value": "1"
    },
    "Id": "491",
    "MetaData": {
      "CreateTime": "2020-06-23T23:26:13-07:00",
      "LastUpdatedTime": "2020-06-23T23:28:54-07:00"
    }
  },
  "time": "2020-11-07T13:29:41.836-07:00"
}
```

## Query a ReimburseCharge

### Request

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content-Type: text/plain
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Sample Query

```sql
Select * from ReimburseCharge Where HasBeenInvoiced = false
```

### Response

```json
{
  "QueryResponse": {
    "ReimburseCarge": [
      {
        "SyncToken": "0",
        "domain": "QBO",
        "HasBeenInvoiced": true,
        "TxnDate": "2020-06-23",
        "CurrencyRef": {
          "name": "United States Dollar",
          "value": "USD"
        },
        "LinkedTxn": [
          {
            "TxnId": "495",
            "TxnType": "Invoice"
          }
        ],
        "Amount": 100.0,
        "sparse": false,
        "Line": [
          {
            "LinkedTxn": [
              {
                "TxnId": "495",
                "TxnType": "Invoice"
              }
            ],
            "DetailType": "ReimburseLineDetail",
            "ReimburseLineDetail": {
              "ItemRef": {
                "name": "Sales",
                "value": "3"
              },
              "Qty": 1,
              "TaxCodeRef": {
                "value": "NON"
              },
              "MarkupInfo": {
                "Percent": 900
              },
              "ItemAccountRef": {
                "name": "Billable Expense Income",
                "value": "37"
              },
              "UnitPrice": 10
            },
            "LineNum": 1,
            "Amount": 10.0,
            "Id": "1"
          },
          {
            "LinkedTxn": [
              {
                "TxnId": "495",
                "TxnType": "Invoice"
              }
            ],
            "Description": "900% markup",
            "DetailType": "ReimburseLineDetail",
            "ReimburseLineDetail": {
              "TaxCodeRef": {
                "value": "NON"
              },
              "MarkupInfo": {
                "Percent": 900
              },
              "ItemAccountRef": {
                "name": "Markup",
                "value": "49"
              }
            },
            "LineNum": 2,
            "Amount": 90.0,
            "Id": "2"
          }
        ],
        "CustomerRef": {
          "name": "Cust1",
          "value": "1"
        },
        "Id": "491",
        "MetaData": {
          "CreateTime": "2020-06-23T23:26:13-07:00",
          "LastUpdatedTime": "2020-06-23T23:28:54-07:00"
        }
      }
    ],
    "startPosition": 1,
    "maxResults": 1,
    "totalCount": 1
  },
  "time": "2020-11-07T13:32:06.76-07:00"
}
```
