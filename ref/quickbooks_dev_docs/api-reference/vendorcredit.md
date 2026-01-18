# VendorCredit

The VendorCredit object is an accounts payable transaction that represents a refund or credit of payment for goods or services. It is a credit that a vendor owes you for various reasons such as overpaid bill, returned merchandise, or other reasons.

## The VendorCredit Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Required for update | Unique identifier for this object. Sort order is ASC by default. Read only, system defined. |
| **VendorRef** | ReferenceType | Required | Reference to the vendor for this transaction. Query the Vendor name list resource to determine the appropriate Vendor object for this reference. Use Vendor.Id and Vendor.Name from that object for VendorRef.value and VendorRef.name, respectively. |
| **Line** | Line [0..n] | Required | Individual line items of a transaction. Valid Line types include: ItemBasedExpenseLine and AccountBasedExpenseLine |
| **SyncToken** | String | Required for update | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. Read only, system defined. |
| **GlobalTaxCalculation** | GlobalTaxCalculationEnum | Conditionally required | Method in which tax is applied. Allowed values are: TaxExcluded, TaxInclusive, and NotApplicable. Not applicable to US companies; required for non-US companies. |
| **CurrencyRef** | CurrencyRefType | Conditionally required | Reference to the currency in which all amounts on the associated transaction are expressed. This must be defined if multicurrency is enabled for the company. Required if multicurrency is enabled for the company. |
| **DocNumber** | String, filterable, sortable | Optional | Reference number for the transaction. Maximum of 21 chars. If not explicitly provided at create time, this field is populated based on the setting of Preferences:OtherPrefs:NameValue.Name = VendorAndPurchasesPrefs.UseCustomTxnNumbers. Sort order is ASC by default. |
| **PrivateNote** | String | Optional | User entered, organization-private note about the transaction. This note does not appear on the transaction to the vendor. This field maps to the Memo field on the transaction form. Max of 4000 chars. |
| **LinkedTxn** | LinkedTxn [0..n] | Optional | Zero or more transactions linked to this object. The LinkedTxn.TxnType can be set to ReimburseCharge. The LinkedTxn.TxnId can be set as the ID of the transaction. Available with minorVersion 55. |
| **ExchangeRate** | Decimal | Optional | The number of home currency units it takes to equal one unit of currency specified by CurrencyRef. Applicable if multicurrency is enabled for the company. Default: 1 |
| **APAccountRef** | ReferenceType, filterable, sortable | Optional | Specifies to which AP account the bill is credited. Query the Account name list resource to determine the appropriate Account object for this reference. The specified account must have Account.Classification set to Liability and Account.AccountSubType set to AccountsPayable. |
| **DepartmentRef** | ReferenceType | Optional | A reference to a Department object specifying the location of the transaction. Available if Preferences.AccountingInfoPrefs.TrackDepartments is set to true. |
| **TxnDate** | Date, filterable, sortable | Optional | The date entered by the user when this transaction occurred. For posting transactions, this is the posting date that affects the financial statements. If the date is not supplied, the current date on the server is used. Sort order is ASC by default. |
| **IncludeInAnnualTPAR** | Boolean | Optional | Include the supplier in the annual TPAR. TPAR stands for Taxable Payments Annual Report. Available with minorVersion 40. |
| **TransactionLocationType** | String | Optional | The account location. Valid values include: WithinFrance, FranceOverseas, OutsideFranceWithEU, OutsideEU. For France locales, only. Available with minorVersion 4. |
| **Balance** | Decimal, sortable | Optional, read only | The current amount of the vendor credit reflecting any adjustments to the original credit amount. Initially set to the value of TotalAmt. Calculated by QuickBooks business logic. Available with minorVersion 12. |
| **MetaData** | ModificationMetaData | Optional | Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications. |
| **RecurDataRef** | ReferenceType | Read only | A reference to the Recurring Transaction. It captures what recurring transaction template the VendorCredit was created from. Available with minorVersion 52. |
| **TotalAmt** | BigDecimal, filterable, sortable | Read only, system defined | Indicates the total credit amount, determined by taking the total of all all lines of the transaction. This includes all charges, allowances, discounts, and taxes. Calculated by QuickBooks business logic. |

### Line Types

#### ItemBasedExpenseLine

Line item for item-based expenses.

#### AccountBasedExpenseLine

Line item for account-based expenses.

### Sample Object

```json
{
  "VendorCredit": {
    "SyncToken": "0",
    "domain": "QBO",
    "VendorRef": {
      "name": "Books by Bessie",
      "value": "30"
    },
    "TxnDate": "2014-12-23",
    "TotalAmt": 90.0,
    "APAccountRef": {
      "name": "Accounts Payable (A/P)",
      "value": "33"
    },
    "sparse": false,
    "Line": [
      {
        "DetailType": "AccountBasedExpenseLineDetail",
        "Amount": 90.0,
        "ProjectRef": {
          "value": "39298045"
        },
        "Id": "1",
        "AccountBasedExpenseLineDetail": {
          "TaxCodeRef": {
            "value": "TAX"
          },
          "AccountRef": {
            "name": "Bank Charges",
            "value": "8"
          },
          "BillableStatus": "Billable",
          "CustomerRef": {
            "name": "Amy's Bird Sanctuary",
            "value": "1"
          }
        }
      }
    ],
    "Id": "255",
    "MetaData": {
      "CreateTime": "2015-07-28T14:13:30-07:00",
      "LastUpdatedTime": "2015-07-28T14:13:30-07:00"
    }
  },
  "time": "2015-07-28T14:16:42.709-07:00"
}
```

## Create a VendorCredit

The VendorRef attribute must be specified. At least one Line with Line.Amount must be specified.

### Minimum Required Elements

| Attribute | Type | Description |
|-----------|------|-------------|
| **VendorRef** | ReferenceType | The vendor reference for this transaction. |
| **Line** | Line [0..n] | Individual line items of a transaction. Valid Line types include: ItemBasedExpenseLine and AccountBasedExpenseLine |
| **CurrencyRef** | CurrencyRefType | Required if multicurrency is enabled for the company. |

### Request

```
POST /v3/company/<realmID>/vendorcredit
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "TotalAmt": 90.0,
  "TxnDate": "2014-12-23",
  "Line": [
    {
      "DetailType": "AccountBasedExpenseLineDetail",
      "Amount": 90.0,
      "ProjectRef": {
        "value": "39298045"
      },
      "Id": "1",
      "AccountBasedExpenseLineDetail": {
        "TaxCodeRef": {
          "value": "TAX"
        },
        "AccountRef": {
          "name": "Bank Charges",
          "value": "8"
        },
        "BillableStatus": "Billable",
        "CustomerRef": {
          "name": "Amy's Bird Sanctuary",
          "value": "1"
        }
      }
    }
  ],
  "APAccountRef": {
    "name": "Accounts Payable (A/P)",
    "value": "33"
  },
  "VendorRef": {
    "name": "Books by Bessie",
    "value": "30"
  }
}
```

### Response

```json
{
  "VendorCredit": {
    "SyncToken": "0",
    "domain": "QBO",
    "VendorRef": {
      "name": "Books by Bessie",
      "value": "30"
    },
    "TxnDate": "2014-12-23",
    "TotalAmt": 90.0,
    "APAccountRef": {
      "name": "Accounts Payable (A/P)",
      "value": "33"
    },
    "sparse": false,
    "Line": [
      {
        "DetailType": "AccountBasedExpenseLineDetail",
        "Amount": 90.0,
        "ProjectRef": {
          "value": "39298045"
        },
        "Id": "1",
        "AccountBasedExpenseLineDetail": {
          "TaxCodeRef": {
            "value": "TAX"
          },
          "AccountRef": {
            "name": "Bank Charges",
            "value": "8"
          },
          "BillableStatus": "Billable",
          "CustomerRef": {
            "name": "Amy's Bird Sanctuary",
            "value": "1"
          }
        }
      }
    ],
    "Id": "157",
    "MetaData": {
      "CreateTime": "2014-12-23T11:14:15-08:00",
      "LastUpdatedTime": "2014-12-23T11:14:15-08:00"
    }
  },
  "time": "2014-12-23T11:14:15.462-08:00"
}
```

## Delete a VendorCredit

This operation deletes the vendorcredit object specified in the request body. Include a minimum of VendorCredit.Id and VendorCredit.SyncToken in the request body.

### Request

```
POST /v3/company/<realmID>/vendorcredit?operation=delete
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "SyncToken": "0",
  "Id": "13"
}
```

### Response

```json
{
  "VendorCredit": {
    "status": "Deleted",
    "domain": "QBO",
    "Id": "13"
  },
  "time": "2015-05-27T10:42:58.468-07:00"
}
```

## Query a VendorCredit

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
select * from vendorcredit
```

### Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "totalCount": 2,
    "VendorCredit": [
      {
        "SyncToken": "0",
        "domain": "QBO",
        "VendorRef": {
          "name": "Books by Bessie",
          "value": "30"
        },
        "TxnDate": "2014-12-23",
        "TotalAmt": 90.0,
        "APAccountRef": {
          "name": "Accounts Payable (A/P)",
          "value": "33"
        },
        "sparse": false,
        "Line": [
          {
            "DetailType": "AccountBasedExpenseLineDetail",
            "Amount": 90.0,
            "ProjectRef": {
              "value": "39298045"
            },
            "Id": "1",
            "AccountBasedExpenseLineDetail": {
              "TaxCodeRef": {
                "value": "TAX"
              },
              "AccountRef": {
                "name": "Bank Charges",
                "value": "8"
              },
              "BillableStatus": "Billable",
              "CustomerRef": {
                "name": "Amy's Bird Sanctuary",
                "value": "1"
              }
            }
          }
        ],
        "Id": "255",
        "MetaData": {
          "CreateTime": "2015-07-28T14:13:30-07:00",
          "LastUpdatedTime": "2015-07-28T14:13:30-07:00"
        }
      }
    ],
    "maxResults": 2
  },
  "time": "2015-07-28T14:14:36.327-07:00"
}
```

## Read a VendorCredit

Retrieves the details of a VendorCredit object that has been previously created.

### Request

```
GET /v3/company/<realmID>/vendorcredit/<vendorcreditId>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "VendorCredit": {
    "SyncToken": "0",
    "domain": "QBO",
    "VendorRef": {
      "name": "Books by Bessie",
      "value": "30"
    },
    "TxnDate": "2014-12-23",
    "TotalAmt": 90.0,
    "APAccountRef": {
      "name": "Accounts Payable (A/P)",
      "value": "33"
    },
    "sparse": false,
    "Line": [
      {
        "DetailType": "AccountBasedExpenseLineDetail",
        "Amount": 90.0,
        "ProjectRef": {
          "value": "39298045"
        },
        "Id": "1",
        "AccountBasedExpenseLineDetail": {
          "TaxCodeRef": {
            "value": "TAX"
          },
          "AccountRef": {
            "name": "Bank Charges",
            "value": "8"
          },
          "BillableStatus": "Billable",
          "CustomerRef": {
            "name": "Amy's Bird Sanctuary",
            "value": "1"
          }
        }
      }
    ],
    "Id": "255",
    "MetaData": {
      "CreateTime": "2015-07-28T14:13:30-07:00",
      "LastUpdatedTime": "2015-07-28T14:13:30-07:00"
    }
  },
  "time": "2015-07-28T14:16:42.709-07:00"
}
```

## Full Update a VendorCredit

Use this operation to update any of the writable fields of an existing vendorcredit object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL. The ID of the object to update is specified in the request body.

### Request

```
POST /v3/company/<realmID>/vendorcredit
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "SyncToken": "1",
  "domain": "QBO",
  "VendorRef": {
    "name": "Books by Bessie",
    "value": "30"
  },
  "TxnDate": "2014-12-23",
  "TotalAmt": 140.0,
  "APAccountRef": {
    "name": "Accounts Payable (A/P)",
    "value": "33"
  },
  "sparse": false,
  "Line": [
    {
      "DetailType": "AccountBasedExpenseLineDetail",
      "Amount": 140.0,
      "ProjectRef": {
        "value": "39298045"
      },
      "Id": "1",
      "AccountBasedExpenseLineDetail": {
        "TaxCodeRef": {
          "value": "TAX"
        },
        "AccountRef": {
          "name": "Bank Charges",
          "value": "8"
        },
        "BillableStatus": "Billable",
        "CustomerRef": {
          "name": "Amy's Bird Sanctuary",
          "value": "1"
        }
      }
    }
  ],
  "Id": "255",
  "MetaData": {
    "CreateTime": "2015-07-28T14:13:30-07:00",
    "LastUpdatedTime": "2015-07-28T14:22:05-07:00"
  }
}
```

### Response

```json
{
  "VendorCredit": {
    "SyncToken": "2",
    "domain": "QBO",
    "VendorRef": {
      "name": "Books by Bessie",
      "value": "30"
    },
    "TxnDate": "2014-12-23",
    "TotalAmt": 140.0,
    "APAccountRef": {
      "name": "Accounts Payable (A/P)",
      "value": "33"
    },
    "sparse": false,
    "Line": [
      {
        "DetailType": "AccountBasedExpenseLineDetail",
        "Amount": 140.0,
        "ProjectRef": {
          "value": "39298045"
        },
        "Id": "1",
        "AccountBasedExpenseLineDetail": {
          "TaxCodeRef": {
            "value": "TAX"
          },
          "AccountRef": {
            "name": "Bank Charges",
            "value": "8"
          },
          "BillableStatus": "Billable",
          "CustomerRef": {
            "name": "Amy's Bird Sanctuary",
            "value": "1"
          }
        }
      }
    ],
    "Id": "255",
    "MetaData": {
      "CreateTime": "2015-07-28T14:13:30-07:00",
      "LastUpdatedTime": "2015-07-28T14:23:50-07:00"
    }
  },
  "time": "2015-07-28T14:23:52.196-07:00"
}
```
