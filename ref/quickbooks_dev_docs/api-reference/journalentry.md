# JournalEntry

JournalEntry is a transaction in which:
- There are at least one pair of lines, a debit and a credit, called distribution lines.
- Each distribution line has an account from the Chart of Accounts.
- The total of the debit column equals the total of the credit column.

When you record a transaction with a JournalEntry object, the QuickBooks Online UI labels the transaction as JRNL in the register and as General Journal on reports that list transactions.

## Business Rules

- **Accounts Receivable (A/R) account**: Needs to have a Customer in the Name Field. The A/R account is visible only after there are A/R transactions such as receive payments from invoices.
- **Accounts Payable (A/P) account**: Needs to have a Vendor in the Name Field. The A/P account is visible only after there are A/P transactions such Bill objects.
- **Tax Related considerations for global companies**:
  - There are both Sales Tax and Purchase Tax.
  - On the transaction line, if TaxCodeRef is specified, TaxApplicableOn and TaxAmount are required.
  - Each TaxCodeRef can result in one or more tax lines.
  - For AU locale: On the transaction line, if GlobalTaxCalculation is TaxInclusive and TaxCodeRef is specified, TaxInclusiveAmt is required.
  - Any TxnTaxDetail lines specified are not overridden. If a user provides incorrect values such that the total amount on debit is not equal to total amount on credit, an error is returned.

## The JournalEntry Object

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **Id** | String, read only, filterable, sortable | Unique identifier for this object. Sort order is ASC by default. *Required for update* |
| **Line** | Line[] | Individual line items of a transaction. There must be at least one pair of Journal Entry Line elements, representing a debit and a credit, called distribution lines. Valid Line types include: JournalEntryLine and DescriptionOnlyLine. *Required* |
| **SyncToken** | String, read only | Version number of the object. It is used to lock an object for use by one app at a time. *Required for update* |
| **CurrencyRef** | CurrencyRefType | Reference to the currency in which all amounts on the associated transaction are expressed. Required if multicurrency is enabled for the company. *Conditionally required* |
| **GlobalTaxCalculation** | GlobalTaxCalculationEnum | Method in which tax is applied. Allowed values are: TaxExcluded, TaxInclusive. Not applicable to US companies; required for non-US companies. *Conditionally required, minorVersion: 53* |
| **DocNumber** | String (max 21 chars), filterable, sortable | Reference number for the transaction. |
| **PrivateNote** | String (max 4000 chars) | User entered, organization-private note about the transaction. |
| **TxnDate** | Date, filterable, sortable | The date when this transaction occurred. For posting transactions, this is the posting date that affects the financial statements. |
| **ExchangeRate** | Decimal | The number of home currency units it takes to equal one unit of currency specified by CurrencyRef. |
| **TaxRateRef** | ReferenceType | Reference to the Tax Adjustment Rate Ids for this item. *minorVersion: 49* |
| **TransactionLocationType** | String | The account location. For France locales only. Valid values: WithinFrance, FranceOverseas, OutsideFranceWithEU, OutsideEU. *minorVersion: 4* |
| **TxnTaxDetail** | TxnTaxDetail | Information for taxes charged on the transaction as a whole. |
| **Adjustment** | Boolean | Indicates whether this transaction is a journal entry adjustment. |
| **MetaData** | ModificationMetaData | Descriptive information about the object. Read only. |
| **RecurDataRef** | ReferenceType, read only | A reference to the Recurring Transaction. *minorVersion: 52* |
| **TotalAmt** | BigDecimal, read only | The value of this field will always be set to zero. |
| **HomeTotalAmt** | Decimal, read only | The value of this field will always be set to zero. Applicable if multicurrency is enabled. |

### JournalEntryLineDetail

| Attribute | Type | Description |
|-----------|------|-------------|
| **PostingType** | String | Indicates the posting type: Debit or Credit. *Required* |
| **AccountRef** | ReferenceType | Reference to the account from the Chart of Accounts. *Required* |
| **Entity** | Entity | Reference to a Customer or Vendor (for A/R and A/P accounts). |
| **ClassRef** | ReferenceType | Reference to a Class for tracking. |
| **DepartmentRef** | ReferenceType | Reference to a Department for location tracking. |
| **TaxCodeRef** | ReferenceType | Reference to tax code for this line. |
| **TaxApplicableOn** | String | Sales or Purchase. Required if TaxCodeRef is specified. |
| **TaxAmount** | Decimal | Tax amount for this line. Required if TaxCodeRef is specified. |
| **BillableStatus** | String | Billing status: Billable, NotBillable, HasBeenBilled. |

### Sample Object

```json
{
  "time": "2015-06-29T12:43:42.132-07:00",
  "JournalEntry": {
    "SyncToken": "0",
    "domain": "QBO",
    "TxnDate": "2015-06-29",
    "sparse": false,
    "Line": [
      {
        "Description": "Four sprinkler heads damaged",
        "JournalEntryLineDetail": {
          "PostingType": "Debit",
          "AccountRef": {
            "name": "Job Expenses:Job Materials:Fountain and Garden Lighting",
            "value": "65"
          },
          "Entity": {
            "Type": "Customer",
            "EntityRef": {
              "name": "Amy's Bird Sanctuary",
              "value": "1"
            }
          }
        },
        "DetailType": "JournalEntryLineDetail",
        "ProjectRef": {
          "value": "39298034"
        },
        "Amount": 25.54,
        "Id": "0"
      },
      {
        "JournalEntryLineDetail": {
          "PostingType": "Credit",
          "AccountRef": {
            "name": "Notes Payable",
            "value": "44"
          },
          "Entity": {
            "Type": "Vendor",
            "EntityRef": {
              "name": "IDX Vendor",
              "value": "2"
            }
          }
        },
        "DetailType": "JournalEntryLineDetail",
        "Amount": 25.54,
        "Id": "1",
        "Description": "Sprinkler Hds - Sprinkler Hds Inventory Adjustment"
      }
    ],
    "Adjustment": false,
    "Id": "227",
    "TxnTaxDetail": {},
    "MetaData": {
      "CreateTime": "2015-06-29T12:33:57-07:00",
      "LastUpdatedTime": "2015-06-29T12:33:57-07:00"
    }
  }
}
```

## Create a JournalEntry

A JournalEntry must have at least one set of two Line elements that balance each other out: one for the debit side and one for the credit side describing the entry.

### Request

```
POST /v3/company/<realmID>/journalentry
Content-Type: application/json
```

**Production Base URL:** `https://quickbooks.api.intuit.com`
**Sandbox Base URL:** `https://sandbox-quickbooks.api.intuit.com`

### Required Fields

| Attribute | Type | Description |
|-----------|------|-------------|
| **Line** | Line[] | At least two line items: one with PostingType set to Debit and one with PostingType set to Credit. *Required* |
| **JournalCodeRef** | ReferenceType | Reference to a JournalCode object. Required for France locales. *Conditionally required, minorVersion: 5* |
| **CurrencyRef** | CurrencyRefType | Required if multicurrency is enabled for the company. *Conditionally required* |

### Sample Request Body

```json
{
  "Line": [
    {
      "JournalEntryLineDetail": {
        "PostingType": "Debit",
        "AccountRef": {
          "name": "Opening Bal Equity",
          "value": "39"
        }
      },
      "DetailType": "JournalEntryLineDetail",
      "Amount": 100.0,
      "Id": "0",
      "Description": "nov portion of rider insurance"
    },
    {
      "JournalEntryLineDetail": {
        "PostingType": "Credit",
        "AccountRef": {
          "name": "Notes Payable",
          "value": "44"
        }
      },
      "DetailType": "JournalEntryLineDetail",
      "Amount": 100.0,
      "Description": "nov portion of rider insurance"
    }
  ]
}
```

### Sample Response

```json
{
  "time": "2015-06-29T12:45:32.183-07:00",
  "JournalEntry": {
    "SyncToken": "0",
    "domain": "QBO",
    "TxnDate": "2015-06-29",
    "sparse": false,
    "Line": [
      {
        "JournalEntryLineDetail": {
          "PostingType": "Debit",
          "AccountRef": {
            "name": "Truck:Depreciation",
            "value": "39"
          }
        },
        "DetailType": "JournalEntryLineDetail",
        "Amount": 100.0,
        "Id": "0",
        "Description": "nov portion of rider insurance"
      },
      {
        "JournalEntryLineDetail": {
          "PostingType": "Credit",
          "AccountRef": {
            "name": "Notes Payable",
            "value": "44"
          }
        },
        "DetailType": "JournalEntryLineDetail",
        "Amount": 100.0,
        "Id": "1",
        "Description": "nov portion of rider insurance"
      }
    ],
    "Adjustment": false,
    "Id": "228",
    "TxnTaxDetail": {},
    "MetaData": {
      "CreateTime": "2015-06-29T12:45:32-07:00",
      "LastUpdatedTime": "2015-06-29T12:45:32-07:00"
    }
  }
}
```

## Delete a JournalEntry

This operation deletes the JournalEntry object specified in the request body. Include a minimum of JournalEntry.Id and JournalEntry.SyncToken.

### Request

```
POST /v3/company/<realmID>/journalentry?operation=delete
```

### Sample Request Body

```json
{
  "SyncToken": "0",
  "Id": "228"
}
```

### Sample Response

```json
{
  "time": "2015-05-26T14:03:31.321-07:00",
  "JournalEntry": {
    "status": "Deleted",
    "domain": "QBO",
    "Id": "228"
  }
}
```

## Query a JournalEntry

### Request

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content-Type: application/text
```

### Sample Query

```sql
select * from JournalEntry Where Metadata.LastUpdatedTime>'2014-09-15T00:00:00-07:00' Order By Metadata.LastUpdatedTime
```

## Read a JournalEntry

Retrieves the details of a JournalEntry that has been previously created.

### Request

```
GET /v3/company/<realmID>/journalentry/<journalentryId>
```

### Sample Response

Returns the full JournalEntry object as shown in the Sample Object section.

## Full Update a JournalEntry

Use this operation to update any of the writable fields of an existing JournalEntry object. The request body must include all writable fields of the existing object, including all lines, as returned in a read response. Writable fields omitted from the request body are set to NULL.

### Request

```
POST /v3/company/<realmID>/journalentry
Content-Type: application/json
```

### Required Fields

| Attribute | Type | Description |
|-----------|------|-------------|
| **Id** | String | Unique identifier. *Required for update* |
| **SyncToken** | String | Version number. *Required for update* |
| **Line** | Line[] | At least two line items: one Debit, one Credit. *Required* |

### Sample Request Body

```json
{
  "SyncToken": "1",
  "domain": "QBO",
  "TxnDate": "2015-06-29",
  "sparse": false,
  "Line": [
    {
      "JournalEntryLineDetail": {
        "PostingType": "Debit",
        "AccountRef": {
          "name": "Job Expenses:Job Materials:Fountain and Garden Lighting",
          "value": "65"
        }
      },
      "DetailType": "JournalEntryLineDetail",
      "Amount": 25.54,
      "Id": "0",
      "Description": "Updated description"
    },
    {
      "JournalEntryLineDetail": {
        "PostingType": "Credit",
        "AccountRef": {
          "name": "Notes Payable",
          "value": "44"
        }
      },
      "DetailType": "JournalEntryLineDetail",
      "Amount": 25.54,
      "Id": "1",
      "Description": "Sprinkler Hds - Sprinkler Hds Inventory Adjustment"
    }
  ],
  "Adjustment": false,
  "Id": "227",
  "TxnTaxDetail": {},
  "MetaData": {
    "CreateTime": "2015-06-29T12:33:57-07:00",
    "LastUpdatedTime": "2015-06-29T12:33:57-07:00"
  }
}
```

## Sparse Update a JournalEntry

Sparse updating provides the ability to update a subset of properties for a given object; only elements specified in the request are updated. Missing elements are left untouched.

### Request

```
POST /v3/company/<realmID>/journalentry
Content-Type: application/json
```

### Sample Request Body

```json
{
  "SyncToken": "1",
  "domain": "QBO",
  "TxnDate": "2015-11-30",
  "PrivateNote": "Revised private note via sparse update",
  "sparse": true,
  "Adjustment": false,
  "Id": "227"
}
```

### Sample Response

```json
{
  "time": "2015-06-29T12:54:38.135-07:00",
  "JournalEntry": {
    "DocNumber": "1112",
    "SyncToken": "1",
    "domain": "QBO",
    "TxnDate": "2015-11-30",
    "PrivateNote": "Revised private note via sparse update",
    "sparse": false,
    "Line": [
      {
        "JournalEntryLineDetail": {
          "PostingType": "Debit",
          "AccountRef": {
            "name": "Job Expenses:Job Materials:Fountain and Garden Lighting",
            "value": "65"
          }
        },
        "DetailType": "JournalEntryLineDetail",
        "Amount": 25.54,
        "Id": "0",
        "Description": "Four sprinkler heads damaged"
      },
      {
        "JournalEntryLineDetail": {
          "PostingType": "Credit",
          "AccountRef": {
            "name": "Notes Payable",
            "value": "44"
          }
        },
        "DetailType": "JournalEntryLineDetail",
        "Amount": 25.54,
        "Id": "1",
        "Description": "Sprinkler Hds - Sprinkler Hds Inventory Adjustment"
      }
    ],
    "Adjustment": false,
    "Id": "227",
    "TxnTaxDetail": {},
    "MetaData": {
      "CreateTime": "2015-06-29T12:33:57-07:00",
      "LastUpdatedTime": "2015-06-29T12:54:38-07:00"
    }
  }
}
```
