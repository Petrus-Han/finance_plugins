# Invoice

An Invoice represents a sales form where the customer pays for a product or service later.

## Business Rules

- An invoice must have at least one Line for either a sales item or an inline subtotal.
- An invoice must have CustomerRef populated.
- The DocNumber attribute is populated automatically by the data service if not supplied.
- If ShipAddr, BillAddr, or both are not provided, the appropriate customer address from the referenced Customer object is used to fill those values.
- If you have a large number of invoice and corresponding payment records that you wish to import to the QuickBooks Online company, sort the invoice and payment records in chronological order and use the batch resource to send invoice and payments batches of 10, one after the other, to ensure any open invoices get credited with their payments.
- If an invoice is taxable, there is a limit of 750 lines per invoice.

## The Invoice Object

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **Id** | String, read only, filterable, sortable | Unique identifier for this object. Sort order is ASC by default. *Required for update* |
| **Line** | Line[] | Individual line items of a transaction. Valid Line types include SalesItemLine, GroupLine, DescriptionOnlyLine (also used for inline Subtotal lines), DiscountLine and SubTotalLine (used for the overall transaction). If the transaction is taxable there is a limit of 750 lines per transaction. *Required* |
| **CustomerRef** | ReferenceType, filterable | Reference to a customer or job. Query the Customer name list resource to determine the appropriate Customer object for this reference. Use Customer.Id and Customer.DisplayName from that object for CustomerRef.value and CustomerRef.name, respectively. *Required* |
| **SyncToken** | String, read only | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. *Required for update* |
| **ShipFromAddr** | PhysicalAddress | Identifies the address where the goods are shipped from. For transactions without shipping, it represents the address where the sale took place. If automated sales tax is enabled and automated tax calculations are being used, this field is required for an accurate sales tax calculation. *Conditionally required, minorVersion: 35* |
| **CurrencyRef** | CurrencyRefType | Reference to the currency in which all amounts on the associated transaction are expressed. This must be defined if multicurrency is enabled for the company. *Conditionally required* |
| **GlobalTaxCalculation** | GlobalTaxCalculationEnum | Method in which tax is applied. Allowed values are: TaxExcluded, TaxInclusive, and NotApplicable. Not applicable to US companies; required for non-US companies. *Conditionally required* |
| **DocNumber** | String (max 21 chars), filterable, sortable | Reference number for the transaction. If not explicitly provided at create time, this field is populated based on the setting of Preferences:CustomTxnNumber. *Conditionally required* |
| **ProjectRef** | ReferenceType, filterable | Reference to the Project ID associated with this transaction. Available with Minor Version 69 and above. *Conditionally required, minorVersion: 69* |
| **BillEmail** | EmailAddress | Identifies the e-mail address where the invoice is sent. If EmailStatus=NeedToSend, BillEmail is a required input. *Conditionally required* |
| **TxnDate** | Date, filterable, sortable | The date entered by the user when this transaction occurred. yyyy/MM/dd is the valid date format. |
| **ShipDate** | Date | Date for delivery of goods or services. |
| **TrackingNum** | String | Shipping provider's tracking number for the delivery of the goods associated with the transaction. |
| **ClassRef** | ReferenceType | Reference to the Class associated with the transaction. Available if Preferences.AccountingInfoPrefs.ClassTrackingPerTxn is set to true. |
| **PrintStatus** | String | Printing status of the invoice. Valid values: NotSet, NeedToPrint, PrintComplete. |
| **SalesTermRef** | ReferenceType, filterable | Reference to the sales term associated with the transaction. |
| **TxnSource** | String | Used internally to specify originating source of a credit card transaction. |
| **LinkedTxn** | LinkedTxn[] | Zero or more related transactions to this Invoice object. Links to Estimate and TimeActivity objects can be established directly with UI or API. |
| **DepositToAccountRef** | ReferenceType | Account to which money is deposited. Query the Account name list resource to determine the appropriate Account object for this reference. |
| **AllowOnlineACHPayment** | Boolean | Specifies if this invoice can be paid with online bank transfers. |
| **TransactionLocationType** | String | The account location. For France, UAE, and India locales. *minorVersion: 4* |
| **DueDate** | Date, filterable, sortable | Date when the payment of the transaction is due. |
| **MetaData** | ModificationMetaData | Descriptive information about the object. Read only. |
| **PrivateNote** | String (max 4000 chars) | User entered, organization-private note about the transaction. This note does not appear on the invoice to the customer. |
| **BillEmailCc** | EmailAddress | Identifies the carbon copy e-mail address where the invoice is sent. *minorVersion: 8* |
| **CustomerMemo** | MemoRef | User-entered message to the customer; this message is visible to end user on their transactions. |
| **EmailStatus** | String | Email status of the invoice. Valid values: NotSet, NeedToSend, EmailSent |
| **ExchangeRate** | Decimal | The number of home currency units it takes to equal one unit of currency specified by CurrencyRef. |
| **Deposit** | Decimal | The deposit made towards this invoice. |
| **TxnTaxDetail** | TxnTaxDetail | This data type provides information for taxes charged on the transaction as a whole. |
| **AllowOnlineCreditCardPayment** | Boolean | Specifies if online credit card payments are allowed for this invoice. |
| **CustomField** | CustomField[] | One of, up to three custom fields for the transaction. |
| **ShipAddr** | PhysicalAddress | Identifies the address where the goods must be shipped. |
| **DepartmentRef** | ReferenceType | A reference to a Department object specifying the location of the transaction. |
| **BillEmailBcc** | EmailAddress | Identifies the blind carbon copy e-mail address where the invoice is sent. *minorVersion: 8* |
| **ShipMethodRef** | ReferenceType | Reference to the ShipMethod associated with the transaction. |
| **BillAddr** | PhysicalAddress | Bill-to address of the Invoice. |
| **ApplyTaxAfterDiscount** | Boolean | If false or null, calculate the sales tax first, and then apply the discount. If true, subtract the discount first and then calculate the sales tax. |
| **HomeBalance** | Decimal, read only | Convenience field containing the amount in Balance expressed in terms of the home currency. *minorVersion: 3* |
| **DeliveryInfo** | DeliveryInfo, read only | Email delivery information. Returned when a request has been made to deliver email with the send operation. |
| **TotalAmt** | BigDecimal, read only | Indicates the total amount of the transaction. This includes the total of all the charges, allowances, and taxes. Calculated by QuickBooks business logic. |
| **InvoiceLink** | String, read only | Sharable link for the invoice sent to external customers. *minorVersion: 36* |
| **RecurDataRef** | ReferenceType, read only | A reference to the Recurring Transaction. It captures what recurring transaction template the Invoice was created from. *minorVersion: 52* |
| **TaxExemptionRef** | ReferenceType, read only | Reference to the TaxExemption ID associated with this object. *minorVersion: 21* |
| **Balance** | Decimal, read only, filterable, sortable | The balance reflecting any payments made against the transaction. Initially set to the value of TotalAmt. A Balance of 0 indicates the invoice is fully paid. |
| **HomeTotalAmt** | Decimal, read only | Total amount of the transaction in the home currency. |
| **FreeFormAddress** | Boolean, system defined | Denotes how ShipAddr is stored: formatted or unformatted. |
| **AllowOnlinePayment** | Boolean, deprecated | Deprecated flag to allow online payments. Do not modify. |
| **AllowIPNPayment** | Boolean, deprecated | Flag to allow payments from legacy Intuit Payment Network (IPN). Must always be set to false. Do not modify. |

### Line Types

#### SalesItemLine
Used for products or services sold.

#### GroupLine
Used for grouping line items.

#### DescriptionOnlyLine
Used for descriptions and inline subtotals.

#### DiscountLine
Used for discounts applied to the invoice.

#### SubTotalLine
Used for the overall transaction subtotal.

### Sample Object

```json
{
  "Invoice": {
    "TxnDate": "2014-09-19",
    "domain": "QBO",
    "PrintStatus": "NeedToPrint",
    "SalesTermRef": {
      "value": "3"
    },
    "TotalAmt": 362.07,
    "Line": [
      {
        "Description": "Rock Fountain",
        "DetailType": "SalesItemLineDetail",
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "TAX"
          },
          "Qty": 1,
          "UnitPrice": 275,
          "ItemRef": {
            "name": "Rock Fountain",
            "value": "5"
          }
        },
        "LineNum": 1,
        "Amount": 275.0,
        "Id": "1"
      },
      {
        "Description": "Fountain Pump",
        "DetailType": "SalesItemLineDetail",
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "TAX"
          },
          "Qty": 1,
          "UnitPrice": 12.75,
          "ItemRef": {
            "name": "Pump",
            "value": "11"
          }
        },
        "LineNum": 2,
        "Amount": 12.75,
        "Id": "2"
      },
      {
        "Description": "Concrete for fountain installation",
        "DetailType": "SalesItemLineDetail",
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "TAX"
          },
          "Qty": 5,
          "UnitPrice": 9.5,
          "ItemRef": {
            "name": "Concrete",
            "value": "3"
          }
        },
        "LineNum": 3,
        "Amount": 47.5,
        "Id": "3"
      },
      {
        "DetailType": "SubTotalLineDetail",
        "Amount": 335.25,
        "SubTotalLineDetail": {}
      }
    ],
    "DueDate": "2014-10-19",
    "ApplyTaxAfterDiscount": false,
    "DocNumber": "1037",
    "sparse": false,
    "CustomerMemo": {
      "value": "Thank you for your business and have a great day!"
    },
    "ProjectRef": {
      "value": "39298045"
    },
    "Deposit": 0,
    "Balance": 362.07,
    "CustomerRef": {
      "name": "Sonnenschein Family Store",
      "value": "24"
    },
    "TxnTaxDetail": {
      "TxnTaxCodeRef": {
        "value": "2"
      },
      "TotalTax": 26.82,
      "TaxLine": [
        {
          "DetailType": "TaxLineDetail",
          "Amount": 26.82,
          "TaxLineDetail": {
            "NetAmountTaxable": 335.25,
            "TaxPercent": 8,
            "TaxRateRef": {
              "value": "3"
            },
            "PercentBased": true
          }
        }
      ]
    },
    "SyncToken": "0",
    "LinkedTxn": [
      {
        "TxnId": "100",
        "TxnType": "Estimate"
      }
    ],
    "BillEmail": {
      "Address": "Familiystore@intuit.com"
    },
    "ShipAddr": {
      "City": "Middlefield",
      "Line1": "5647 Cypress Hill Ave.",
      "PostalCode": "94303",
      "Lat": "37.4238562",
      "Long": "-122.1141681",
      "CountrySubDivisionCode": "CA",
      "Id": "25"
    },
    "EmailStatus": "NotSet",
    "BillAddr": {
      "Line4": "Middlefield, CA  94303",
      "Line3": "5647 Cypress Hill Ave.",
      "Line2": "Sonnenschein Family Store",
      "Line1": "Russ Sonnenschein",
      "Long": "-122.1141681",
      "Lat": "37.4238562",
      "Id": "95"
    },
    "MetaData": {
      "CreateTime": "2014-09-19T13:16:17-07:00",
      "LastUpdatedTime": "2014-09-19T13:16:17-07:00"
    },
    "CustomField": [
      {
        "DefinitionId": "1",
        "StringValue": "102",
        "Type": "StringType",
        "Name": "Crew #"
      }
    ],
    "Id": "130"
  },
  "time": "2015-07-24T10:48:27.082-07:00"
}
```

## Create an Invoice

Have at least one Line a sales item or inline subtotal. Have a populated CustomerRef element.

### Request

```
POST /v3/company/<realmID>/invoice
Content-Type: application/json
```

**Production Base URL:** `https://quickbooks.api.intuit.com`
**Sandbox Base URL:** `https://sandbox-quickbooks.api.intuit.com`

### Minimum Required Fields

| Attribute | Type | Description |
|-----------|------|-------------|
| **CustomerRef** | ReferenceType | Reference to a customer or job. *Required* |
| **Line** | Line[] | The minimum line item required is one of: SalesItemLine, GroupLine, or DescriptionOnlyLine (inline subtotal). *Required* |
| **ProjectRef** | ReferenceType | Reference to the Project ID. *Conditionally required, minorVersion: 69* |
| **CurrencyRef** | CurrencyRefType | Reference to the currency. Required if multicurrency is enabled for the company. *Conditionally required* |

### Sample Request Body

```json
{
  "Line": [
    {
      "DetailType": "SalesItemLineDetail",
      "Amount": 100.0,
      "SalesItemLineDetail": {
        "ItemRef": {
          "name": "Services",
          "value": "1"
        }
      }
    }
  ],
  "CustomerRef": {
    "value": "1"
  }
}
```

### Sample Response

```json
{
  "Invoice": {
    "TxnDate": "2015-07-24",
    "domain": "QBO",
    "PrintStatus": "NeedToPrint",
    "TotalAmt": 100.0,
    "Line": [
      {
        "LineNum": 1,
        "Amount": 100.0,
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
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
        "Amount": 100.0,
        "SubTotalLineDetail": {}
      }
    ],
    "DueDate": "2015-08-23",
    "ApplyTaxAfterDiscount": false,
    "DocNumber": "1069",
    "sparse": false,
    "ProjectRef": {
      "value": "39298034"
    },
    "Deposit": 0,
    "Balance": 100.0,
    "CustomerRef": {
      "name": "Amy's Bird Sanctuary",
      "value": "1"
    },
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "SyncToken": "0",
    "LinkedTxn": [],
    "ShipAddr": {
      "City": "Bayshore",
      "Line1": "4581 Finch St.",
      "PostalCode": "94326",
      "Lat": "INVALID",
      "Long": "INVALID",
      "CountrySubDivisionCode": "CA",
      "Id": "109"
    },
    "EmailStatus": "NotSet",
    "BillAddr": {
      "City": "Bayshore",
      "Line1": "4581 Finch St.",
      "PostalCode": "94326",
      "Lat": "INVALID",
      "Long": "INVALID",
      "CountrySubDivisionCode": "CA",
      "Id": "2"
    },
    "MetaData": {
      "CreateTime": "2015-07-24T10:33:39-07:00",
      "LastUpdatedTime": "2015-07-24T10:33:39-07:00"
    },
    "CustomField": [
      {
        "DefinitionId": "1",
        "Type": "StringType",
        "Name": "Crew #"
      }
    ],
    "Id": "238"
  },
  "time": "2015-07-24T10:33:39.11-07:00"
}
```

## Delete an Invoice

This operation deletes the invoice object specified in the request body. Include a minimum of Invoice.Id and Invoice.SyncToken in the request body. You must unlink any linked transactions associated with the invoice object before deleting it.

### Request

```
POST /v3/company/<realmID>/invoice?operation=delete
Content-Type: application/json
```

### Required Fields

| Attribute | Type | Description |
|-----------|------|-------------|
| **SyncToken** | String | Version number of the object. *Required* |
| **Id** | String | Unique identifier for this object. *Required* |

### Sample Request Body

```json
{
  "SyncToken": "3",
  "Id": "33"
}
```

### Sample Response

```json
{
  "Invoice": {
    "status": "Deleted",
    "domain": "QBO",
    "Id": "33"
  },
  "time": "2013-03-15T00:18:15.322-07:00"
}
```

## Void an Invoice

Use this operation to void an existing invoice object; include a minimum of Invoice.Id and the current Invoice.SyncToken. The transaction remains active but all amounts and quantities are zeroed and the string, Voided, is injected into Invoice.PrivateNote, prepended to existing text if present.

### Request

```
POST /v3/company/<realmID>/invoice?operation=void
Content-Type: application/json
```

### Sample Request Body

```json
{
  "SyncToken": "0",
  "Id": "129"
}
```

### Sample Response

```json
{
  "Invoice": {
    "AllowOnlineACHPayment": false,
    "domain": "QBO",
    "TxnDate": "2014-11-09",
    "PrintStatus": "NEED_TO_PRINT",
    "SalesTermRef": {
      "value": "3"
    },
    "TotalAmt": 0,
    "Line": [
      {
        "Description": "Sod",
        "DetailType": "SALES_ITEM_LINE_DETAIL",
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "TAX"
          },
          "Qty": 0,
          "ItemRef": {
            "name": "Sod",
            "value": "14"
          }
        },
        "LineNum": 1,
        "Amount": 0,
        "Id": "1"
      }
    ],
    "DueDate": "2014-12-09",
    "DocNumber": "1036",
    "PrivateNote": "Voided",
    "sparse": false,
    "Deposit": 0,
    "Balance": 0,
    "CustomerRef": {
      "name": "0969 Ocean View Road",
      "value": "8"
    },
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "AllowOnlineCreditCardPayment": false,
    "SyncToken": "1",
    "LinkedTxn": [],
    "Id": "129"
  },
  "time": "2016-03-16T12:27:10.711-07:00"
}
```

## Get an Invoice as PDF

This resource returns the specified object in the response body as an Adobe Portable Document Format (PDF) file. The resulting PDF file is formatted according to custom form styles in the company settings.

### Request

```
GET /v3/company/<realmID>/invoice/<invoiceId>/pdf
Content-Type: application/pdf
```

### Response

Returns binary PDF data.

## Query an Invoice

### Request

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content-Type: application/text
```

### Sample Query

```sql
select * from Invoice where id = '239'
```

### Sample Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "totalCount": 1,
    "maxResults": 1,
    "Invoice": [
      {
        "TxnDate": "2015-07-24",
        "domain": "QBO",
        "PrintStatus": "NeedToPrint",
        "TotalAmt": 150.0,
        "Line": [
          {
            "LineNum": 1,
            "Amount": 150.0,
            "SalesItemLineDetail": {
              "TaxCodeRef": {
                "value": "NON"
              },
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
            "Amount": 150.0,
            "SubTotalLineDetail": {}
          }
        ],
        "DueDate": "2015-08-23",
        "ApplyTaxAfterDiscount": false,
        "DocNumber": "1070",
        "sparse": false,
        "Deposit": 0,
        "Balance": 150.0,
        "CustomerRef": {
          "name": "Amy's Bird Sanctuary",
          "value": "1"
        },
        "TxnTaxDetail": {
          "TotalTax": 0
        },
        "SyncToken": "0",
        "LinkedTxn": [],
        "EmailStatus": "NotSet",
        "Id": "239"
      }
    ]
  },
  "time": "2015-07-24T10:38:50.01-07:00"
}
```

## Read an Invoice

Retrieves the details of an invoice that has been previously created.

### Request

```
GET /v3/company/<realmID>/invoice/<invoiceId>
```

### Sample Response

Returns the full Invoice object as shown in the Sample Object section.

## Send an Invoice

Sends the invoice via email. The Invoice.EmailStatus parameter is set to EmailSent. The Invoice.DeliveryInfo element is populated with sending information. The Invoice.BillEmail.Address parameter is updated to the address specified with the value of the sendTo query parameter, if specified.

### Request

```
POST /v3/company/<realmID>/invoice/<invoiceId>/send
Content-Type: application/octet-stream
```

Or with explicit email address:

```
POST /v3/company/<realmID>/invoice/<invoiceId>/send?sendTo=<emailAddr>
```

### Sample Response

The response includes DeliveryInfo with DeliveryType and DeliveryTime:

```json
{
  "Invoice": {
    "DeliveryInfo": {
      "DeliveryType": "Email",
      "DeliveryTime": "2014-12-17T11:50:52-08:00"
    },
    "EmailStatus": "EmailSent",
    ...
  }
}
```

## Sparse Update an Invoice

Sparse updating provides the ability to update a subset of properties for a given object; only elements specified in the request are updated. Missing elements are left untouched. The ID of the object to update is specified in the request body.

### Request

```
POST /v3/company/<realmID>/invoice
Content-Type: application/json
```

### Sample Request Body

```json
{
  "SyncToken": "0",
  "Id": "238",
  "sparse": true,
  "DueDate": "2015-09-30"
}
```

### Sample Response

Returns the updated Invoice object with the new DueDate and incremented SyncToken.

## Full Update an Invoice

Use this operation to update any of the writable fields of an existing invoice object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL. The ID of the object to update is specified in the request body.

### Request

```
POST /v3/company/<realmID>/invoice
Content-Type: application/json
```

### Required Fields

| Attribute | Type | Description |
|-----------|------|-------------|
| **CustomerRef** | ReferenceType | Reference to a customer or job. *Required* |
| **Line** | Line[] | The minimum line item required is one of: SalesItemLine, GroupLine, or DescriptionOnlyLine. *Required* |
| **Id** | String | Unique identifier for this object. *Required for update* |
| **SyncToken** | String | Version number of the object. *Required for update* |

### Sample Request Body

```json
{
  "TxnDate": "2015-07-24",
  "domain": "QBO",
  "PrintStatus": "NeedToPrint",
  "TotalAmt": 150.0,
  "Line": [
    {
      "LineNum": 1,
      "Amount": 150.0,
      "SalesItemLineDetail": {
        "TaxCodeRef": {
          "value": "NON"
        },
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
      "Amount": 150.0,
      "SubTotalLineDetail": {}
    }
  ],
  "DueDate": "2015-08-23",
  "ApplyTaxAfterDiscount": false,
  "DocNumber": "1070",
  "sparse": false,
  "CustomerMemo": {
    "value": "Added customer memo."
  },
  "ProjectRef": {
    "value": "39298045"
  },
  "Balance": 150.0,
  "CustomerRef": {
    "name": "Amy's Bird Sanctuary",
    "value": "1"
  },
  "TxnTaxDetail": {
    "TotalTax": 0
  },
  "SyncToken": "0",
  "LinkedTxn": [],
  "ShipAddr": {
    "City": "Bayshore",
    "Line1": "4581 Finch St.",
    "PostalCode": "94326",
    "Lat": "INVALID",
    "Long": "INVALID",
    "CountrySubDivisionCode": "CA",
    "Id": "109"
  },
  "EmailStatus": "NotSet",
  "BillAddr": {
    "City": "Bayshore",
    "Line1": "4581 Finch St.",
    "PostalCode": "94326",
    "Lat": "INVALID",
    "Long": "INVALID",
    "CountrySubDivisionCode": "CA",
    "Id": "2"
  },
  "MetaData": {
    "CreateTime": "2015-07-24T10:35:08-07:00",
    "LastUpdatedTime": "2015-07-24T10:35:08-07:00"
  },
  "CustomField": [
    {
      "DefinitionId": "1",
      "Type": "StringType",
      "Name": "Crew #"
    }
  ],
  "Id": "239"
}
```

### Sample Response

Returns the updated Invoice object with the new CustomerMemo and incremented SyncToken.
