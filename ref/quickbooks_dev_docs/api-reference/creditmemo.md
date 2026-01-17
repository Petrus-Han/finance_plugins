# CreditMemo

The CreditMemo object is a financial transaction representing a refund or credit of payment or part of a payment for goods or services that have been sold.

## The CreditMemo Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Required for update | Unique identifier for this object. Sort order is ASC by default. Read only, system defined. |
| **Line** | Line [0..n] | Required | Individual line items of a transaction. Valid Line types include: SalesItemLine, GroupLine, DescriptionOnlyLine, DiscountLine and SubTotalLine |
| **CustomerRef** | ReferenceType, filterable | Required | Reference to a customer or job. Query the Customer name list resource to determine the appropriate Customer object for this reference. Use Customer.Id and Customer.DisplayName from that object for CustomerRef.value and CustomerRef.name, respectively. |
| **SyncToken** | String | Required for update | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. Read only, system defined. |
| **CurrencyRef** | CurrencyRefType | Conditionally required | Reference to the currency in which all amounts on the associated transaction are expressed. This must be defined if multicurrency is enabled for the company. Multicurrency is enabled for the company if Preferences.MultiCurrencyEnabled is set to true. Required if multicurrency is enabled for the company. |
| **GlobalTaxCalculation** | GlobalTaxCalculationEnum | Conditionally required | Method in which tax is applied. Allowed values are: TaxExcluded, TaxInclusive, and NotApplicable. Not applicable to US companies; required for non-US companies. |
| **ProjectRef** | ReferenceType, filterable | Conditionally required | Reference to the Project ID associated with this transaction. Available with Minor Version 69 and above. |
| **BillEmail** | EmailAddress | Conditionally required | Identifies the e-mail address where the credit-memo is sent. If EmailStatus=NeedToSend, BillEmail is a required input. |
| **TxnDate** | Date, filterable, sortable | Optional | The date entered by the user when this transaction occurred. For posting transactions, this is the posting date that affects the financial statements. If the date is not supplied, the current date on the server is used. Sort order is ASC by default. |
| **CustomField** | CustomField | Optional | One of, up to three custom fields for the transaction. Available for custom fields so configured for the company. Check Preferences.SalesFormsPrefs.CustomField and Preferences.VendorAndPurchasesPrefs.POCustomField for custom fields currently configured. |
| **ClassRef** | ReferenceType | Optional | Reference to the Class associated with the transaction. Available if Preferences.AccountingInfoPrefs.ClassTrackingPerLine is set to true. Query the Class name list resource to determine the appropriate Class object for this reference. Use Class.Id and Class.Name from that object for ClassRef.value and ClassRef.name, respectively. |
| **PrintStatus** | String | Optional | Printing status of the credit-memo. Valid values: NotSet, NeedToPrint, PrintComplete. |
| **SalesTermRef** | ReferenceType, filterable | Optional | Reference to the sales term associated with the transaction. Query the Term name list resource to determine the appropriate Term object for this reference. Use Term.Id and Term.Name from that object for SalesTermRef.value and SalesTermRef.name, respectively. |
| **TotalAmt** | BigDecimal | Optional | Indicates the total amount of the transaction. This includes the total of all the charges, allowances, and taxes. Calculated by QuickBooks business logic; any value you supply is over-written by QuickBooks. |
| **InvoiceRef** | ReferenceType | Optional | Reference to the Invoice for which Credit memo is issued. Needed for GST compliance. Use Invoice.Id and Invoice.Name from that object for InvoiceRef.value and InvoiceRef.name, respectively. Available with minorVersion 37. |
| **TransactionLocationType** | String | Optional | The account location. Valid values include: WithinFrance, FranceOverseas, OutsideFranceWithEU, OutsideEU. For France locales, only. Available with minorVersion 4. |
| **ApplyTaxAfterDiscount** | Boolean | Optional | If false or null, calculate the sales tax first, and then apply the discount. If true, subtract the discount first and then calculate the sales tax. US versions of QuickBooks only. |
| **DocNumber** | String, filterable, sortable | Optional | Reference number for the transaction. Maximum of 21 chars. If not explicitly provided at create time, this field is populated based on the setting of Preferences:CustomTxnNumber. Note: DocNumber is an optional field for all locales except France. For France locale if Preferences:CustomTxnNumber is enabled it will not be automatically generated and is a required field. |
| **PrivateNote** | String | Optional | User entered, organization-private note about the transaction. This note does not appear on the deposit form. Max of 4000 chars. |
| **CustomerMemo** | MemoRef | Optional | User-entered message to the customer; this message is visible to end user on their transactions. |
| **TxnTaxDetail** | TxnTaxDetail | Optional | This data type provides information for taxes charged on the transaction as a whole. It captures the details sales taxes calculated for the transaction based on the tax codes referenced by the transaction. This can be calculated by QuickBooks business logic or you may supply it when adding a transaction. If sales tax is disabled (Preferences.TaxPrefs.UsingSalesTax is set to false) then TxnTaxDetail is ignored and not stored. |
| **PaymentMethodRef** | ReferenceType | Optional, read only | Reference to a PaymentMethod associated with this transaction. Query the PaymentMethod name list resource to determine the appropriate PaymentMethod object for this reference. Use PaymentMethod.Id and PaymentMethod.Name from that object for PaymentMethodRef.value and PaymentMethodRef.name, respectively. |
| **ExchangeRate** | Decimal | Optional | The number of home currency units it takes to equal one unit of currency specified by CurrencyRef. Applicable if multicurrency is enabled for the company. |
| **ShipAddr** | PhysicalAddress | Optional | Identifies the address where the goods must be shipped. If ShipAddr is not specified, and a default Customer:ShippingAddr is specified in QuickBooks for this customer, the default ship-to address will be used by QuickBooks. For international addresses - countries should be passed as 3 ISO alpha-3 characters or the full name of the country. |
| **DepartmentRef** | ReferenceType | Optional | A reference to a Department object specifying the location of the transaction. Available if Preferences.AccountingInfoPrefs.TrackDepartments is set to true. Query the Department name list resource to determine the appropriate department object for this reference. Use Department.Id and Department.Name from that object for DepartmentRef.value and DepartmentRef.name, respectively. |
| **EmailStatus** | String | Optional | Email status of the credit-memo. Valid values: NotSet, NeedToSend, EmailSent |
| **BillAddr** | PhysicalAddress | Optional | Bill-to address of the credit memo. If BillAddr is not specified, and a default Customer:BillingAddr is specified in QuickBooks for this customer, the default bill-to address is used by QuickBooks. For international addresses - countries should be passed as 3 ISO alpha-3 characters or the full name of the country. |
| **MetaData** | ModificationMetaData | Optional | Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications. |
| **HomeBalance** | Decimal | Read only | Convenience field containing the amount in Balance expressed in terms of the home currency. Calculated by QuickBooks business logic. Value is valid only when CurrencyRef is specified and available when endpoint is evoked with the minorversion=3 query parameter. Applicable if multicurrency is enabled for the company. |
| **RemainingCredit** | Decimal | Read only | Indicates the total credit amount still available to apply towards the payment. |
| **RecurDataRef** | ReferenceType | Read only | A reference to the Recurring Transaction. It captures what recurring transaction template the CreditMemo was created from. Available with minorVersion 52. |
| **TaxExemptionRef** | ReferenceType | Read only, system defined | Reference to the TaxExemption ID associated with this object. Available for companies that have automated sales tax enabled. For internal use only. Available with minorVersion 21. |
| **Balance** | Decimal, filterable, sortable | Read only | The balance reflecting any payments made against the transaction. Initially set to the value of TotalAmt. A Balance of 0 indicates the invoice is fully paid. Calculated by QuickBooks business logic; any value you supply is over-written by QuickBooks. |
| **HomeTotalAmt** | Decimal | Read only, system defined | Total amount of the transaction in the home currency. Includes the total of all the charges, allowances and taxes. Calculated by QuickBooks business logic. Value is valid only when CurrencyRef is specified. Applicable if multicurrency is enabled for the company. |

### Line Types

#### SalesItemLine

Line item for sales transactions.

#### GroupLine

Group line for bundled items.

#### DescriptionOnlyLine

Line with description only, no amount.

#### DiscountLine

Line representing a discount.

#### SubTotalLine

Line representing the subtotal.

### Sample Object

```json
{
  "CreditMemo": {
    "TxnDate": "2014-09-02",
    "domain": "QBO",
    "PrintStatus": "NeedToPrint",
    "TotalAmt": 100.0,
    "RemainingCredit": 0,
    "Line": [
      {
        "Description": "Pest Control Services",
        "DetailType": "SalesItemLineDetail",
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
          "Qty": 1,
          "UnitPrice": 100,
          "ItemRef": {
            "name": "Pest Control",
            "value": "10"
          }
        },
        "LineNum": 1,
        "Amount": 100.0,
        "Id": "1"
      },
      {
        "DetailType": "SubTotalLineDetail",
        "Amount": 100.0,
        "SubTotalLineDetail": {}
      }
    ],
    "ApplyTaxAfterDiscount": false,
    "DocNumber": "1026",
    "sparse": false,
    "CustomerMemo": {
      "value": "Updated customer memo."
    },
    "ProjectRef": {
      "value": "39298034"
    },
    "Balance": 0,
    "CustomerRef": {
      "name": "Amy's Bird Sanctuary",
      "value": "1"
    },
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "SyncToken": "3",
    "CustomField": [
      {
        "DefinitionId": "1",
        "Type": "StringType",
        "Name": "Crew #"
      }
    ],
    "ShipAddr": {
      "CountrySubDivisionCode": "CA",
      "City": "Bayshore",
      "PostalCode": "94326",
      "Id": "108",
      "Line1": "4581 Finch St."
    },
    "EmailStatus": "NotSet",
    "BillAddr": {
      "Line4": "Bayshore, CA  94326",
      "Line3": "4581 Finch St.",
      "Id": "79",
      "Line1": "Amy Lauterbach",
      "Line2": "Amy's Bird Sanctuary"
    },
    "MetaData": {
      "CreateTime": "2014-09-18T12:51:27-07:00",
      "LastUpdatedTime": "2015-07-01T09:16:28-07:00"
    },
    "BillEmail": {
      "Address": "Birds@Intuit.com"
    },
    "Id": "73"
  },
  "time": "2015-07-23T09:10:45.624-07:00"
}
```

## Create a Credit Memo

Creates a new credit memo.

### Minimum Required Elements

| Attribute | Type | Description |
|-----------|------|-------------|
| **Line** | Line | The minimum line item required for the request is one of the following: Sales item line type or Group item line type. |
| **CustomerRef** | ReferenceType | Reference to a customer or job. |
| **CurrencyRef** | CurrencyRefType | Required if multicurrency is enabled for the company. |
| **ProjectRef** | ReferenceType | Required with Minor Version 69 and above if project tracking is enabled. |

### Request

```
POST /v3/company/<realmID>/creditmemo
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "Line": [
    {
      "DetailType": "SalesItemLineDetail",
      "Amount": 50,
      "SalesItemLineDetail": {
        "ItemRef": {
          "name": "Concrete",
          "value": "3"
        }
      }
    }
  ],
  "CustomerRef": {
    "name": "CoolCars",
    "value": "3"
  }
}
```

### Response

```json
{
  "CreditMemo": {
    "DocNumber": "1039",
    "SyncToken": "0",
    "domain": "QBO",
    "Balance": 50.0,
    "BillAddr": {
      "City": "Half Moon Bay",
      "Line1": "65 Ocean Dr.",
      "PostalCode": "94213",
      "Lat": "37.4300318",
      "Long": "-122.4336537",
      "CountrySubDivisionCode": "CA",
      "Id": "4"
    },
    "TxnDate": "2014-12-31",
    "TotalAmt": 50.0,
    "CustomerRef": {
      "name": "Cool Cars",
      "value": "3"
    },
    "ShipAddr": {
      "City": "Half Moon Bay",
      "Line1": "65 Ocean Dr.",
      "PostalCode": "94213",
      "Lat": "37.4300318",
      "Long": "-122.4336537",
      "CountrySubDivisionCode": "CA",
      "Id": "4"
    },
    "RemainingCredit": 50.0,
    "PrintStatus": "NeedToPrint",
    "ProjectRef": {
      "value": "39298034"
    },
    "EmailStatus": "NotSet",
    "sparse": false,
    "Line": [
      {
        "LineNum": 1,
        "Amount": 50.0,
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
          "ItemRef": {
            "name": "Concrete",
            "value": "3"
          }
        },
        "Id": "1",
        "DetailType": "SalesItemLineDetail"
      },
      {
        "DetailType": "SubTotalLineDetail",
        "Amount": 50.0,
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
    "Id": "150",
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "MetaData": {
      "CreateTime": "2014-12-31T09:44:40-08:00",
      "LastUpdatedTime": "2014-12-31T09:44:40-08:00"
    }
  },
  "time": "2014-12-31T09:44:40.726-08:00"
}
```

## Delete a Credit Memo

This operation deletes the creditmemo object specified in the request body. Include a minimum of CreditMemo.Id and CreditMemo.SyncToken in the request body.

### Request

```
POST /v3/company/<realmID>/creditmemo?operation=delete
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "SyncToken": "0",
  "Id": "73"
}
```

### Response

```json
{
  "CreditMemo": {
    "status": "Deleted",
    "domain": "QBO",
    "Id": "73"
  },
  "time": "2015-05-26T13:53:33.118-07:00"
}
```

## Get a Credit Memo as PDF

Returns the specified object in the response body as an Adobe Portable Document Format (PDF) file. The resulting PDF file is formatted according to custom form styles in the company settings.

### Request

```
GET /v3/company/<realmID>/creditmemo/<creditmemoId>/pdf
Content-Type: application/pdf
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

## Query a Credit Memo

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
Select * from CreditMemo where TxnDate > '2014-04-15'
```

### Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "CreditMemo": [
      {
        "TxnDate": "2014-09-02",
        "domain": "QBO",
        "PrintStatus": "NeedToPrint",
        "TotalAmt": 100.0,
        "RemainingCredit": 0,
        "Line": [
          {
            "Description": "Pest Control Services",
            "DetailType": "SalesItemLineDetail",
            "SalesItemLineDetail": {
              "TaxCodeRef": {
                "value": "NON"
              },
              "Qty": 1,
              "UnitPrice": 100,
              "ItemRef": {
                "name": "Pest Control",
                "value": "10"
              }
            },
            "LineNum": 1,
            "Amount": 100.0,
            "Id": "1"
          },
          {
            "DetailType": "SubTotalLineDetail",
            "Amount": 100.0,
            "SubTotalLineDetail": {}
          }
        ],
        "ApplyTaxAfterDiscount": false,
        "DocNumber": "1026",
        "sparse": false,
        "CustomerMemo": {
          "value": "Updated customer memo."
        },
        "ProjectRef": {
          "value": "39298034"
        },
        "Balance": 0,
        "CustomerRef": {
          "name": "Amy's Bird Sanctuary",
          "value": "1"
        },
        "TxnTaxDetail": {
          "TotalTax": 0
        },
        "SyncToken": "3",
        "CustomField": [
          {
            "DefinitionId": "1",
            "Type": "StringType",
            "Name": "Crew #"
          }
        ],
        "ShipAddr": {
          "CountrySubDivisionCode": "CA",
          "City": "Bayshore",
          "PostalCode": "94326",
          "Id": "108",
          "Line1": "4581 Finch St."
        },
        "EmailStatus": "NotSet",
        "BillAddr": {
          "Line4": "Bayshore, CA  94326",
          "Line3": "4581 Finch St.",
          "Id": "79",
          "Line1": "Amy Lauterbach",
          "Line2": "Amy's Bird Sanctuary"
        },
        "MetaData": {
          "CreateTime": "2014-09-18T12:51:27-07:00",
          "LastUpdatedTime": "2015-07-01T09:16:28-07:00"
        },
        "BillEmail": {
          "Address": "Birds@Intuit.com"
        },
        "Id": "73"
      }
    ],
    "maxResults": 2
  },
  "time": "2015-07-23T09:13:36.246-07:00"
}
```

## Read a Credit Memo

Retrieves the details of a creditmemo that has been previously created.

### Request

```
GET /v3/company/<realmID>/creditmemo/<creditmemoId>
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "CreditMemo": {
    "TxnDate": "2014-09-02",
    "domain": "QBO",
    "PrintStatus": "NeedToPrint",
    "TotalAmt": 100.0,
    "RemainingCredit": 0,
    "Line": [
      {
        "Description": "Pest Control Services",
        "DetailType": "SalesItemLineDetail",
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
          "Qty": 1,
          "UnitPrice": 100,
          "ItemRef": {
            "name": "Pest Control",
            "value": "10"
          }
        },
        "LineNum": 1,
        "Amount": 100.0,
        "Id": "1"
      },
      {
        "DetailType": "SubTotalLineDetail",
        "Amount": 100.0,
        "SubTotalLineDetail": {}
      }
    ],
    "ApplyTaxAfterDiscount": false,
    "DocNumber": "1026",
    "sparse": false,
    "CustomerMemo": {
      "value": "Updated customer memo."
    },
    "ProjectRef": {
      "value": "39298034"
    },
    "Balance": 0,
    "CustomerRef": {
      "name": "Amy's Bird Sanctuary",
      "value": "1"
    },
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "SyncToken": "3",
    "CustomField": [
      {
        "DefinitionId": "1",
        "Type": "StringType",
        "Name": "Crew #"
      }
    ],
    "ShipAddr": {
      "CountrySubDivisionCode": "CA",
      "City": "Bayshore",
      "PostalCode": "94326",
      "Id": "108",
      "Line1": "4581 Finch St."
    },
    "EmailStatus": "NotSet",
    "BillAddr": {
      "Line4": "Bayshore, CA  94326",
      "Line3": "4581 Finch St.",
      "Id": "79",
      "Line1": "Amy Lauterbach",
      "Line2": "Amy's Bird Sanctuary"
    },
    "MetaData": {
      "CreateTime": "2014-09-18T12:51:27-07:00",
      "LastUpdatedTime": "2015-07-01T09:16:28-07:00"
    },
    "BillEmail": {
      "Address": "Birds@Intuit.com"
    },
    "Id": "73"
  },
  "time": "2015-07-23T09:10:45.624-07:00"
}
```

## Send a Credit Memo

Sends the credit memo via email to the customer.

The following actions occur:
- The CreditMemo.EmailStatus parameter is set to EmailSent.
- The CreditMemo.DeliveryInfo element is populated with sending information.
- The CreditMemo.BillEmail.Address parameter is updated to the address specified with the value of the sendTo query parameter, if specified.

### Request

```
POST /v3/company/<realmID>/creditmemo/<creditmemoId>/send
Content-Type: application/octet-stream
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

To specify an explicit email address:
```
POST /v3/company/<realmID>/creditmemo/<creditmemoId>/send?sendTo=<emailAddress>
```

### Response

```json
{
  "CreditMemo": {
    "TxnDate": "2014-09-02",
    "domain": "QBO",
    "PrintStatus": "NeedToPrint",
    "DeliveryInfo": {
      "DeliveryType": "Email",
      "DeliveryTime": "2019-09-19T10:43:46-07:00"
    },
    "TotalAmt": 100.0,
    "RemainingCredit": 0,
    "Line": [
      {
        "Description": "Pest Control Services",
        "DetailType": "SalesItemLineDetail",
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
          "Qty": 1,
          "UnitPrice": 100,
          "ItemRef": {
            "name": "Pest Control",
            "value": "10"
          }
        },
        "LineNum": 1,
        "Amount": 100.0,
        "Id": "1"
      },
      {
        "DetailType": "SubTotalLineDetail",
        "Amount": 100.0,
        "SubTotalLineDetail": {}
      }
    ],
    "ApplyTaxAfterDiscount": false,
    "DocNumber": "1026",
    "sparse": false,
    "CustomerMemo": {
      "value": "Updated customer memo."
    },
    "ProjectRef": {
      "value": "39298034"
    },
    "Balance": 0,
    "CustomerRef": {
      "name": "Amy's Bird Sanctuary",
      "value": "1"
    },
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "SyncToken": "3",
    "CustomField": [
      {
        "DefinitionId": "1",
        "Type": "StringType",
        "Name": "Crew #"
      }
    ],
    "ShipAddr": {
      "CountrySubDivisionCode": "CA",
      "City": "Bayshore",
      "PostalCode": "94326",
      "Id": "108",
      "Line1": "4581 Finch St."
    },
    "EmailStatus": "EmailSent",
    "BillAddr": {
      "Line4": "Bayshore, CA  94326",
      "Line3": "4581 Finch St.",
      "Id": "79",
      "Line1": "Amy Lauterbach",
      "Line2": "Amy's Bird Sanctuary"
    },
    "MetaData": {
      "CreateTime": "2014-09-18T12:51:27-07:00",
      "LastUpdatedTime": "2019-09-19T10:43:46-07:00"
    },
    "BillEmail": {
      "Address": "Birds@Intuit.com"
    },
    "Id": "73"
  },
  "time": "2019-09-19T10:43:46-07:00"
}
```

## Full Update a Credit Memo

Use this operation to update any of the writable fields of an existing creditmemo object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL. The ID of the object to update is specified in the request body.

### Request

```
POST /v3/company/<realmID>/creditmemo
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Required Fields for Update

| Attribute | Description |
|-----------|-------------|
| **Id** | The unique identifier of the credit memo to update |
| **SyncToken** | The current sync token value |
| **Line** | All line items |
| **CustomerRef** | Customer reference |

### Request Body

```json
{
  "TxnDate": "2014-09-02",
  "domain": "QBO",
  "PrintStatus": "NeedToPrint",
  "TotalAmt": 100.0,
  "RemainingCredit": 0,
  "Line": [
    {
      "Description": "Pest Control Services",
      "DetailType": "SalesItemLineDetail",
      "SalesItemLineDetail": {
        "TaxCodeRef": {
          "value": "NON"
        },
        "Qty": 1,
        "UnitPrice": 100,
        "ItemRef": {
          "name": "Pest Control",
          "value": "10"
        }
      },
      "LineNum": 1,
      "Amount": 100.0,
      "Id": "1"
    },
    {
      "DetailType": "SubTotalLineDetail",
      "Amount": 100.0,
      "SubTotalLineDetail": {}
    }
  ],
  "ApplyTaxAfterDiscount": false,
  "DocNumber": "1026",
  "sparse": false,
  "CustomerMemo": {
    "value": "Another memo update."
  },
  "ProjectRef": {
    "value": "39298045"
  },
  "Balance": 0,
  "CustomerRef": {
    "name": "Amy's Bird Sanctuary",
    "value": "1"
  },
  "TxnTaxDetail": {
    "TotalTax": 0
  },
  "SyncToken": "4",
  "CustomField": [
    {
      "DefinitionId": "1",
      "Type": "StringType",
      "Name": "Crew #"
    }
  ],
  "ShipAddr": {
    "CountrySubDivisionCode": "CA",
    "City": "Bayshore",
    "PostalCode": "94326",
    "Id": "108",
    "Line1": "4581 Finch St."
  },
  "EmailStatus": "NotSet",
  "BillAddr": {
    "Line4": "Bayshore, CA  94326",
    "Line3": "4581 Finch St.",
    "Id": "79",
    "Line1": "Amy Lauterbach",
    "Line2": "Amy's Bird Sanctuary"
  },
  "MetaData": {
    "CreateTime": "2014-09-18T12:51:27-07:00",
    "LastUpdatedTime": "2015-07-01T09:16:28-07:00"
  },
  "BillEmail": {
    "Address": "Birds@Intuit.com"
  },
  "Id": "73"
}
```

### Response

```json
{
  "CreditMemo": {
    "TxnDate": "2014-09-02",
    "domain": "QBO",
    "PrintStatus": "NeedToPrint",
    "TotalAmt": 100.0,
    "RemainingCredit": 0,
    "Line": [
      {
        "Description": "Pest Control Services",
        "DetailType": "SalesItemLineDetail",
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
          "Qty": 1,
          "UnitPrice": 100,
          "ItemRef": {
            "name": "Pest Control",
            "value": "10"
          }
        },
        "LineNum": 1,
        "Amount": 100.0,
        "Id": "1"
      },
      {
        "DetailType": "SubTotalLineDetail",
        "Amount": 100.0,
        "SubTotalLineDetail": {}
      }
    ],
    "ApplyTaxAfterDiscount": false,
    "DocNumber": "1026",
    "sparse": false,
    "CustomerMemo": {
      "value": "Another memo update."
    },
    "ProjectRef": {
      "value": "39298045"
    },
    "Balance": 0,
    "CustomerRef": {
      "name": "Amy's Bird Sanctuary",
      "value": "1"
    },
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "SyncToken": "5",
    "CustomField": [
      {
        "DefinitionId": "1",
        "Type": "StringType",
        "Name": "Crew #"
      }
    ],
    "ShipAddr": {
      "CountrySubDivisionCode": "CA",
      "City": "Bayshore",
      "PostalCode": "94326",
      "Id": "108",
      "Line1": "4581 Finch St."
    },
    "EmailStatus": "NotSet",
    "BillAddr": {
      "Line4": "Bayshore, CA  94326",
      "Line3": "4581 Finch St.",
      "Id": "79",
      "Line1": "Amy Lauterbach",
      "Line2": "Amy's Bird Sanctuary"
    },
    "MetaData": {
      "CreateTime": "2014-09-18T12:51:27-07:00",
      "LastUpdatedTime": "2015-07-23T09:23:52-07:00"
    },
    "BillEmail": {
      "Address": "Birds@Intuit.com"
    },
    "Id": "73"
  },
  "time": "2015-07-23T09:23:52.115-07:00"
}
```
