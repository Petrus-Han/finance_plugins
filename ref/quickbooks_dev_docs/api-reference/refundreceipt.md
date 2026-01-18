# RefundReceipt

A RefundReceipt object represents a refund to the customer for a product or service that was provided.

## The RefundReceipt Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Required for update | Unique identifier for this object. Sort order is ASC by default. Read only, system defined. |
| **DepositToAccountRef** | ReferenceType | Required | Account from which payment money is refunded. Query the Account name list resource to determine the appropriate Account object for this reference, where Account.AccountType is Other Current Asset or Bank. Use Account.Id and Account.Name from that object for DepositToAccountRef.value and DepositToAccountRef.name, respectively. |
| **Line** | Line | Required | Individual line items of a transaction. Valid Line types include: SalesItemLine, GroupLine, DescriptionOnlyLine, DiscountLine and SubTotalLine (read-only). |
| **SyncToken** | String | Required for update | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. Read only, system defined. |
| **CurrencyRef** | CurrencyRefType | Conditionally required | Reference to the currency in which all amounts on the associated transaction are expressed. This must be defined if multicurrency is enabled for the company. Multicurrency is enabled for the company if Preferences.MultiCurrencyEnabled is set to true. Required if multicurrency is enabled for the company. |
| **PaymentRefNum** | String (max 100 chars) | Conditionally required | The reference number for the payment received. For example, check # for a check, envelope # for a cash donation. Provide when DepositToAccountRef references an Account object where Account.AccountType=Bank. Required when PrintStatus is set to PrintComplete. If PrintStatus is set to NeedToPrint, the system sets PaymentRefNum to "To Print". |
| **GlobalTaxCalculation** | GlobalTaxCalculationEnum | Conditionally required | Method in which tax is applied. Allowed values are: TaxExcluded, TaxInclusive, and NotApplicable. Not applicable to US companies; required for non-US companies. |
| **ProjectRef** | ReferenceType, filterable | Conditionally required | Reference to the Project ID associated with this transaction. Available with Minor Version 69 and above. |
| **BillEmail** | EmailAddress | Conditionally required | Identifies the e-mail address where the invoice is sent. If EmailStatus=NeedToSend, BillEmail is a required input. |
| **TxnDate** | Date, filterable, sortable | Optional | The date entered by the user when this transaction occurred. For posting transactions, this is the posting date that affects the financial statements. If the date is not supplied, the current date on the server is used. Sort order is ASC by default. |
| **CustomField** | CustomField | Optional | One of, up to three custom fields for the transaction. Available for custom fields so configured for the company. Check Preferences.SalesFormsPrefs.CustomField and Preferences.VendorAndPurchasesPrefs.POCustomField for custom fields currently configured. |
| **ClassRef** | ReferenceType | Optional | Reference to the Class associated with the transaction. Available if Preferences.AccountingInfoPrefs.ClassTrackingPerTxn is set to true. Query the Class name list resource to determine the appropriate Class object for this reference. Use Class.Id and Class.Name from that object for ClassRef.value and ClassRef.name, respectively. |
| **PrintStatus** | String | Optional | Printing status of the invoice. Valid values: NotSet, NeedToPrint, PrintComplete. |
| **CheckPayment** | CheckPayment, filterable, sortable | Optional | Information about a check payment for the transaction. Used when PaymentType is Check. Max 21 characters. |
| **TxnSource** | String | Optional | The originating source of the credit card transaction. Used in eCommerce apps where credit card transactions are processed by a merchant account. When set to IntuitPayment, this transaction is inserted into a list of pending deposits to be automatically matched and reconciled with the merchant's account when the transactions made via QuickBooks Payments settle. Currently, the only supported value is IntuitPayment. |
| **TransactionLocationType** | String | Optional | The account location. Valid values include: WithinFrance, FranceOverseas, OutsideFranceWithEU, OutsideEU. For France locales, only. Minor version 4. |
| **MetaData** | ModificationMetaData | Optional | Descriptive information about the entity. The MetaData values are set by Data Services and are read only for all applications. |
| **DocNumber** | String, filterable, sortable (max 21 chars) | Optional | Reference number for the transaction. If not explicitly provided at create time, this field is populated based on the setting of Preferences:CustomTxnNumber. If Preferences:CustomTxnNumber is true a custom value can be provided. If no value is supplied, the resulting DocNumber is null. If Preferences:CustomTxnNumber is false, resulting DocNumber is system generated by incrementing the last number by 1. Note: DocNumber is an optional field for all locales except France. For France locale if Preferences:CustomTxnNumber is enabled it will not be automatically generated and is a required field. Sort order is ASC by default. |
| **PrivateNote** | String (max 4000 chars) | Optional | User entered, organization-private note about the transaction. This note does not appear on the refund receipt to the customer. This field maps to the Memo field on the refund receipt form. |
| **CustomerMemo** | MemoRef | Optional | User-entered message to the customer; this message is visible to end user on their transaction. |
| **CreditCardPayment** | CreditCardPayment, filterable, sortable | Optional | Information about a credit card payment for the transaction. Used when PaymentType is CreditCard. Inject with data only if the payment was transacted through Intuit Payments API. Max 21 characters. |
| **CustomerRef** | ReferenceType, filterable | Optional | Reference to a customer or job. Query the Customer name list resource to determine the appropriate Customer object for this reference. Use Customer.Id and Customer.DisplayName from that object for CustomerRef.value and CustomerRef.name, respectively. |
| **TxnTaxDetail** | TxnTaxDetail | Optional | This data type provides information for taxes charged on the transaction as a whole. It captures the details sales taxes calculated for the transaction based on the tax codes referenced by the transaction. This can be calculated by QuickBooks business logic or you may supply it when adding a transaction. If sales tax is disabled (Preferences.TaxPrefs.UsingSalesTax is set to false) then TxnTaxDetail is ignored and not stored. |
| **PaymentMethodRef** | ReferenceType | Optional | Reference to a PaymentMethod associated with this transaction. Query the PaymentMethod name list resource to determine the appropriate PaymentMethod object for this reference. Use PaymentMethod.Id and PaymentMethod.Name from that object for PaymentMethodRef.value and PaymentMethodRef.name, respectively. |
| **ExchangeRate** | Decimal | Optional | The number of home currency units it takes to equal one unit of currency specified by CurrencyRef. Applicable if multicurrency is enabled for the company. |
| **ShipAddr** | PhysicalAddress | Optional | Identifies the address where the goods must be shipped. If ShipAddr is not specified, and a default Customer:ShippingAddr is specified in QuickBooks for this customer, the default ship-to address will be used by QuickBooks. For international addresses - countries should be passed as 3 ISO alpha-3 characters or the full name of the country. |
| **DepartmentRef** | ReferenceType | Optional | A reference to a Department object specifying the location of the transaction. Available if Preferences.AccountingInfoPrefs.TrackDepartments is set to true. Query the Department name list resource to determine the appropriate department object for this reference. Use Department.Id and Department.Name from that object for DepartmentRef.value and DepartmentRef.name, respectively. |
| **PaymentType** | PaymentTypeEnum, filterable, sortable | Optional | Valid values are Cash, Check, CreditCard, or Other. Max 21 characters. |
| **BillAddr** | PhysicalAddress | Optional | Bill-to address of the Invoice. If BillAddr is not specified, and a default Customer:BillingAddr is specified in QuickBooks for this customer, the default bill-to address is used by QuickBooks. For international addresses - countries should be passed as 3 ISO alpha-3 characters or the full name of the country. |
| **ApplyTaxAfterDiscount** | Boolean | Optional | If false or null, calculate the sales tax first, and then apply the discount. If true, subtract the discount first and then calculate the sales tax. Default Value: false. Constraints: US versions of QuickBooks only. |
| **HomeBalance** | Decimal | Read only | Convenience field containing the amount in Balance expressed in terms of the home currency. Calculated by QuickBooks business logic. Available when endpoint is evoked with the minorversion=3 query parameter. Applicable if multicurrency is enabled for the company. Minor version 3. |
| **RecurDataRef** | ReferenceType | Read only | A reference to the Recurring Transaction. It captures what recurring transaction template the RefundReceipt was created from. Minor version 52. |
| **TotalAmt** | BigDecimal | Read only | Indicates the total amount of the transaction. This includes the total of all the charges, allowances, and taxes. Calculated by QuickBooks business logic; any value you supply is over-written by QuickBooks. System defined. |
| **TaxExemptionRef** | ReferenceType | Read only | Reference to the TaxExemption ID associated with this object. Available for companies that have automated sales tax enabled. TaxExemptionRef.Name: The Tax Exemption Id for the customer to which this object is associated. This Id is typically issued by the state. TaxExemptionRef.value: The system-generated Id of the exemption type. For internal use only. Minor version 21, system defined. |
| **Balance** | Decimal, filterable, sortable | Read only | The balance reflecting any payments made against the transaction. Initially set to the value of TotalAmt. Calculated by QuickBooks business logic; any value you supply is over-written by QuickBooks. |
| **HomeTotalAmt** | Decimal | Read only | Total amount of the transaction in the home currency. Includes the total of all the charges, allowances and taxes. Calculated by QuickBooks business logic. Value is valid only when CurrencyRef is specified. Applicable if multicurrency is enabled for the company. System defined. |

### Line Types

#### SalesItemLine

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **DetailType** | String | Required | Set to SalesItemLineDetail for this type of line. |
| **Amount** | Decimal | Required | The amount of the line item. |
| **SalesItemLineDetail** | Object | Required | Contains ItemRef, Qty, UnitPrice, TaxCodeRef, etc. |

#### GroupLine

Used for grouping line items together.

#### DescriptionOnlyLine

Used for adding descriptions without item references.

#### DiscountLine

Used for applying discounts.

#### SubTotalLine (Read-only)

System-calculated subtotal line.

### Sample Object

```json
{
  "RefundReceipt": {
    "DocNumber": "1020",
    "SyncToken": "0",
    "domain": "QBO",
    "Balance": 0,
    "PaymentMethodRef": {
      "name": "Check",
      "value": "2"
    },
    "BillAddr": {
      "Line4": "South Orange, NJ  07079",
      "Line3": "350 Mountain View Dr.",
      "Line2": "Pye's Cakes",
      "Line1": "Karen Pye",
      "Long": "-74.2609903",
      "Lat": "40.7489277",
      "Id": "73"
    },
    "DepositToAccountRef": {
      "name": "Checking",
      "value": "35"
    },
    "TxnDate": "2014-09-17",
    "TotalAmt": 87.5,
    "CustomerRef": {
      "name": "Pye's Cakes",
      "value": "15"
    },
    "CustomerMemo": {
      "value": "Thank you for your business and have a great day!"
    },
    "ShipAddr": {
      "City": "South Orange",
      "Line1": "350 Mountain View Dr.",
      "PostalCode": "07079",
      "Lat": "40.7633073",
      "Long": "-74.2426072",
      "CountrySubDivisionCode": "NJ",
      "Id": "15"
    },
    "PrintStatus": "NotSet",
    "BillEmail": {
      "Address": "pyescakes@intuit.com"
    },
    "sparse": false,
    "Line": [
      {
        "Description": "Refund - Pest control was ineffective",
        "DetailType": "SalesItemLineDetail",
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
          "Qty": 2.5,
          "UnitPrice": 35,
          "ItemRef": {
            "name": "Pest Control",
            "value": "10"
          }
        },
        "LineNum": 1,
        "Amount": 87.5,
        "Id": "1"
      },
      {
        "DetailType": "SubTotalLineDetail",
        "Amount": 87.5,
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
    "Id": "66",
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "MetaData": {
      "CreateTime": "2014-09-17T15:35:07-07:00",
      "LastUpdatedTime": "2014-09-17T15:35:07-07:00"
    }
  },
  "time": "2015-07-29T08:15:49.421-07:00"
}
```

## Create a RefundReceipt

A RefundReceipt object must have at least one line that describes an item.

A RefundReceipt object must have a DepositToAccountRef.

If the billing address is not provided, the customer address is used to fill those values.

TaxCode.CustomSalesTax cannot be used as TxnTaxCodeRef. This taxcode is reserved to mark the transaction as created using old sales tax model with no predefined tax rates. You cannot create or update a transaction that implements TaxCode.CustomSalesTax.

### Request

```
POST /v3/company/<realmID>/refundreceipt
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Minimum Required Elements

- **DepositToAccountRef**: Account from which payment money is refunded
- **Line**: At least one SalesItemLine or GroupLine

### Request Body

```json
{
  "Line": [
    {
      "DetailType": "SalesItemLineDetail",
      "Amount": 420.0,
      "SalesItemLineDetail": {
        "ItemRef": {
          "value": "38"
        }
      }
    }
  ],
  "DepositToAccountRef": {
    "name": "Checking",
    "value": "35"
  }
}
```

### Response

```json
{
  "RefundReceipt": {
    "DocNumber": "1072",
    "SyncToken": "0",
    "domain": "QBO",
    "Balance": 0,
    "DepositToAccountRef": {
      "name": "Checking",
      "value": "35"
    },
    "TxnDate": "2015-07-29",
    "TotalAmt": 420.0,
    "PrintStatus": "NeedToPrint",
    "PaymentRefNum": "To Print",
    "sparse": false,
    "Line": [
      {
        "LineNum": 1,
        "Amount": 420.0,
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
          "ItemRef": {
            "name": "Garden Supplies",
            "value": "38"
          }
        },
        "Id": "1",
        "DetailType": "SalesItemLineDetail"
      },
      {
        "DetailType": "SubTotalLineDetail",
        "Amount": 420.0,
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
    "Id": "261",
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "MetaData": {
      "CreateTime": "2015-07-29T08:07:43-07:00",
      "LastUpdatedTime": "2015-07-29T08:07:43-07:00"
    }
  },
  "time": "2015-07-29T08:07:43.749-07:00"
}
```

## Read a RefundReceipt

Retrieves the details of a RefundReceipt that has been previously created.

### Request

```
GET /v3/company/<realmID>/refundreceipt/<refundreceiptId>
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

Returns the RefundReceipt response body.

```json
{
  "RefundReceipt": {
    "DocNumber": "1020",
    "SyncToken": "0",
    "domain": "QBO",
    "Balance": 0,
    "PaymentMethodRef": {
      "name": "Check",
      "value": "2"
    },
    "BillAddr": {
      "Line4": "South Orange, NJ  07079",
      "Line3": "350 Mountain View Dr.",
      "Line2": "Pye's Cakes",
      "Line1": "Karen Pye",
      "Long": "-74.2609903",
      "Lat": "40.7489277",
      "Id": "73"
    },
    "DepositToAccountRef": {
      "name": "Checking",
      "value": "35"
    },
    "TxnDate": "2014-09-17",
    "TotalAmt": 87.5,
    "CustomerRef": {
      "name": "Pye's Cakes",
      "value": "15"
    },
    "CustomerMemo": {
      "value": "Thank you for your business and have a great day!"
    },
    "ShipAddr": {
      "City": "South Orange",
      "Line1": "350 Mountain View Dr.",
      "PostalCode": "07079",
      "Lat": "40.7633073",
      "Long": "-74.2426072",
      "CountrySubDivisionCode": "NJ",
      "Id": "15"
    },
    "PrintStatus": "NotSet",
    "BillEmail": {
      "Address": "pyescakes@intuit.com"
    },
    "sparse": false,
    "Line": [
      {
        "Description": "Refund - Pest control was ineffective",
        "DetailType": "SalesItemLineDetail",
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
          "Qty": 2.5,
          "UnitPrice": 35,
          "ItemRef": {
            "name": "Pest Control",
            "value": "10"
          }
        },
        "LineNum": 1,
        "Amount": 87.5,
        "Id": "1"
      },
      {
        "DetailType": "SubTotalLineDetail",
        "Amount": 87.5,
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
    "Id": "66",
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "MetaData": {
      "CreateTime": "2014-09-17T15:35:07-07:00",
      "LastUpdatedTime": "2014-09-17T15:35:07-07:00"
    }
  },
  "time": "2015-07-29T08:15:49.421-07:00"
}
```

## Query a RefundReceipt

### Request

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content-Type: application/text
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Sample Query

```sql
select * from RefundReceipt where Id='66'
```

### Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "totalCount": 1,
    "RefundReceipt": [
      {
        "DocNumber": "1020",
        "SyncToken": "0",
        "domain": "QBO",
        "Balance": 0,
        "PaymentMethodRef": {
          "name": "Check",
          "value": "2"
        },
        "BillAddr": {
          "Line4": "South Orange, NJ  07079",
          "Line3": "350 Mountain View Dr.",
          "Line2": "Pye's Cakes",
          "Line1": "Karen Pye",
          "Long": "-74.2609903",
          "Lat": "40.7489277",
          "Id": "73"
        },
        "DepositToAccountRef": {
          "name": "Checking",
          "value": "35"
        },
        "TxnDate": "2014-09-17",
        "TotalAmt": 87.5,
        "CustomerRef": {
          "name": "Pye's Cakes",
          "value": "15"
        },
        "CustomerMemo": {
          "value": "Thank you for your business and have a great day!"
        },
        "PrintStatus": "NotSet",
        "BillEmail": {
          "Address": "pyescakes@intuit.com"
        },
        "sparse": false,
        "Line": [
          {
            "Description": "Refund - Pest control was ineffective",
            "DetailType": "SalesItemLineDetail",
            "SalesItemLineDetail": {
              "TaxCodeRef": {
                "value": "NON"
              },
              "Qty": 2.5,
              "UnitPrice": 35,
              "ItemRef": {
                "name": "Pest Control",
                "value": "10"
              }
            },
            "LineNum": 1,
            "Amount": 87.5,
            "Id": "1"
          },
          {
            "DetailType": "SubTotalLineDetail",
            "Amount": 87.5,
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
        "Id": "66",
        "TxnTaxDetail": {
          "TotalTax": 0
        },
        "MetaData": {
          "CreateTime": "2014-09-17T15:35:07-07:00",
          "LastUpdatedTime": "2014-09-17T15:35:07-07:00"
        }
      }
    ],
    "maxResults": 1
  },
  "time": "2015-07-29T08:14:41.415-07:00"
}
```

## Delete a RefundReceipt

This operation deletes the RefundReceipt object specified in the request body. Include a minimum of RefundReceipt.Id and RefundReceipt.SyncToken in the request body. You must unlink any linked transactions associated with the RefundReceipt object before deleting it.

### Request

```
POST /v3/company/<realmID>/refundreceipt?operation=delete
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "SyncToken": "0",
  "Id": "66"
}
```

### Response

```json
{
  "RefundReceipt": {
    "status": "Deleted",
    "domain": "QBO",
    "Id": "66"
  },
  "time": "2015-05-27T10:34:32.031-07:00"
}
```

## Get a RefundReceipt as PDF

This resource returns the specified object in the response body as an Adobe Portable Document Format (PDF) file. The resulting PDF file is formatted according to custom form styles in the company settings.

### Request

```
GET /v3/company/<realmID>/refundreceipt/<refundreceiptId>/pdf
Content-Type: application/pdf
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

## Send a RefundReceipt

The RefundReceipt.DeliveryInfo element is populated with sending information.

The RefundReceipt.BillEmail.Address parameter is updated to the address specified with the value of the sendTo query parameter, if specified.

### Request

```
# Using email address supplied in RefundReceipt.BillEmail.EmailAddress
POST /v3/company/<realmID>/refundreceipt/<refundreceiptId>/send

# Specifying an explicit email address
POST /v3/company/<realmID>/refundreceipt/<refundreceiptId>/send?sendTo=<emailAddr>

Content-Type: application/octet-stream
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "RefundReceipt": {
    "TxnDate": "2014-09-17",
    "domain": "QBO",
    "PrintStatus": "NotSet",
    "DeliveryInfo": {
      "DeliveryType": "Email",
      "DeliveryTime": "2019-09-19T10:43:46-07:00"
    },
    "TotalAmt": 87.5,
    "Line": [
      {
        "Description": "Refund - Pest control was ineffective",
        "DetailType": "SalesItemLineDetail",
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
          "Qty": 2.5,
          "UnitPrice": 35,
          "ItemRef": {
            "name": "Pest Control",
            "value": "10"
          }
        },
        "LineNum": 1,
        "Amount": 87.5,
        "Id": "1"
      },
      {
        "DetailType": "SubTotalLineDetail",
        "Amount": 87.5,
        "SubTotalLineDetail": {}
      }
    ],
    "ApplyTaxAfterDiscount": false,
    "DocNumber": "1020",
    "sparse": false,
    "DepositToAccountRef": {
      "name": "Checking",
      "value": "35"
    },
    "CustomerMemo": {
      "value": "Thank you for your business and have a great day!"
    },
    "Balance": 0,
    "CustomerRef": {
      "name": "Pye's Cakes",
      "value": "15"
    },
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "SyncToken": "0",
    "PaymentMethodRef": {
      "name": "Check",
      "value": "2"
    },
    "CustomField": [
      {
        "DefinitionId": "1",
        "Type": "StringType",
        "Name": "Crew #"
      }
    ],
    "ShipAddr": {
      "City": "South Orange",
      "Line1": "350 Mountain View Dr.",
      "PostalCode": "07079",
      "Lat": "40.7633073",
      "Long": "-74.2426072",
      "CountrySubDivisionCode": "NJ",
      "Id": "15"
    },
    "BillAddr": {
      "Line4": "South Orange, NJ  07079",
      "Line3": "350 Mountain View Dr.",
      "Line2": "Pye's Cakes",
      "Line1": "Karen Pye",
      "Long": "-74.2609903",
      "Lat": "40.7489277",
      "Id": "73"
    },
    "MetaData": {
      "CreateTime": "2014-09-17T15:35:07-07:00",
      "LastUpdatedTime": "2019-09-19T10:43:46-07:00"
    },
    "BillEmail": {
      "Address": "pyescakes@intuit.com"
    },
    "Id": "66"
  },
  "time": "2019-09-19T10:43:46-07:00"
}
```

## Sparse Update a RefundReceipt

Sparse updating provides the ability to update a subset of properties for a given object; only elements specified in the request are updated. Missing elements are left untouched. The ID of the object to update is specified in the request body.

### Request

```
POST /v3/company/<realmID>/refundreceipt
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "SyncToken": "2",
  "PrivateNote": "This is a new private note added via sparse update.",
  "Id": "66",
  "sparse": true
}
```

### Response

```json
{
  "RefundReceipt": {
    "TxnDate": "2014-09-17",
    "domain": "QBO",
    "PrintStatus": "NotSet",
    "TotalAmt": 87.5,
    "Line": [
      {
        "Description": "Refund - Pest control was ineffective",
        "DetailType": "SalesItemLineDetail",
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
          "Qty": 2.5,
          "UnitPrice": 35,
          "ItemRef": {
            "name": "Pest Control",
            "value": "10"
          }
        },
        "LineNum": 1,
        "Amount": 87.5,
        "Id": "1"
      },
      {
        "DetailType": "SubTotalLineDetail",
        "Amount": 87.5,
        "SubTotalLineDetail": {}
      }
    ],
    "ApplyTaxAfterDiscount": false,
    "DocNumber": "1020",
    "PrivateNote": "This is a new private note added via sparse update.",
    "sparse": false,
    "DepositToAccountRef": {
      "name": "Checking",
      "value": "35"
    },
    "CustomerMemo": {
      "value": "Thank you for your business and have a great day!"
    },
    "ProjectRef": {
      "value": "39298034"
    },
    "Balance": 0,
    "CustomerRef": {
      "name": "Pye's Cakes",
      "value": "15"
    },
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "SyncToken": "3",
    "PaymentMethodRef": {
      "name": "Check",
      "value": "2"
    },
    "CustomField": [
      {
        "DefinitionId": "1",
        "Type": "StringType",
        "Name": "Crew #"
      }
    ],
    "ShipAddr": {
      "City": "South Orange",
      "Line1": "350 Mountain View Dr.",
      "PostalCode": "07079",
      "Lat": "40.7633073",
      "Long": "-74.2426072",
      "CountrySubDivisionCode": "NJ",
      "Id": "15"
    },
    "BillAddr": {
      "Line4": "South Orange, NJ 07079",
      "Line3": "350 Mountain View Dr.",
      "Id": "73",
      "Line1": "Karen Pye",
      "Line2": "Pye's Cakes"
    },
    "MetaData": {
      "CreateTime": "2014-09-17T15:35:07-07:00",
      "LastUpdatedTime": "2015-07-29T08:59:30-07:00"
    },
    "BillEmail": {
      "Address": "pyescakes@intuit.com"
    },
    "Id": "66"
  },
  "time": "2015-07-29T08:59:32.061-07:00"
}
```

## Full Update a RefundReceipt

Use this operation to update any of the writable fields of an existing RefundReceipt object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL. The ID of the object to update is specified in the request body.

### Request

```
POST /v3/company/<realmID>/refundreceipt
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "TxnDate": "2014-09-17",
  "domain": "QBO",
  "PrintStatus": "NotSet",
  "TotalAmt": 87.5,
  "Line": [
    {
      "Description": "Refund - Pest control was ineffective",
      "DetailType": "SalesItemLineDetail",
      "SalesItemLineDetail": {
        "TaxCodeRef": {
          "value": "NON"
        },
        "Qty": 2.5,
        "UnitPrice": 35,
        "ItemRef": {
          "name": "Pest Control",
          "value": "10"
        }
      },
      "LineNum": 1,
      "Amount": 87.5,
      "Id": "1"
    },
    {
      "DetailType": "SubTotalLineDetail",
      "Amount": 87.5,
      "SubTotalLineDetail": {}
    }
  ],
  "ApplyTaxAfterDiscount": false,
  "DocNumber": "1020",
  "sparse": false,
  "DepositToAccountRef": {
    "name": "Checking",
    "value": "35"
  },
  "CustomerMemo": {
    "value": "Updated customer memo"
  },
  "ProjectRef": {
    "value": "39298034"
  },
  "Balance": 0,
  "CustomerRef": {
    "name": "Pye's Cakes",
    "value": "15"
  },
  "TxnTaxDetail": {
    "TotalTax": 0
  },
  "SyncToken": "0",
  "PaymentMethodRef": {
    "name": "Check",
    "value": "2"
  },
  "CustomField": [
    {
      "DefinitionId": "1",
      "Type": "StringType",
      "Name": "Crew #"
    }
  ],
  "ShipAddr": {
    "City": "South Orange",
    "Line1": "350 Mountain View Dr.",
    "PostalCode": "07079",
    "Lat": "40.7633073",
    "Long": "-74.2426072",
    "CountrySubDivisionCode": "NJ",
    "Id": "15"
  },
  "BillAddr": {
    "Line4": "South Orange, NJ  07079",
    "Line3": "350 Mountain View Dr.",
    "Line2": "Pye's Cakes",
    "Line1": "Karen Pye",
    "Long": "-74.2609903",
    "Lat": "40.7489277",
    "Id": "73"
  },
  "MetaData": {
    "CreateTime": "2014-09-17T15:35:07-07:00",
    "LastUpdatedTime": "2014-09-17T15:35:07-07:00"
  },
  "BillEmail": {
    "Address": "pyescakes@intuit.com"
  },
  "Id": "66"
}
```

### Response

```json
{
  "RefundReceipt": {
    "TxnDate": "2014-09-17",
    "domain": "QBO",
    "PrintStatus": "NotSet",
    "TotalAmt": 87.5,
    "Line": [
      {
        "Description": "Refund - Pest control was ineffective",
        "DetailType": "SalesItemLineDetail",
        "SalesItemLineDetail": {
          "TaxCodeRef": {
            "value": "NON"
          },
          "Qty": 2.5,
          "UnitPrice": 35,
          "ItemRef": {
            "name": "Pest Control",
            "value": "10"
          }
        },
        "LineNum": 1,
        "Amount": 87.5,
        "Id": "1"
      },
      {
        "DetailType": "SubTotalLineDetail",
        "Amount": 87.5,
        "SubTotalLineDetail": {}
      }
    ],
    "ApplyTaxAfterDiscount": false,
    "DocNumber": "1020",
    "sparse": false,
    "DepositToAccountRef": {
      "name": "Checking",
      "value": "35"
    },
    "CustomerMemo": {
      "value": "Updated customer memo"
    },
    "ProjectRef": {
      "value": "39298034"
    },
    "Balance": 0,
    "CustomerRef": {
      "name": "Pye's Cakes",
      "value": "15"
    },
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "SyncToken": "1",
    "PaymentMethodRef": {
      "name": "Check",
      "value": "2"
    },
    "CustomField": [
      {
        "DefinitionId": "1",
        "Type": "StringType",
        "Name": "Crew #"
      }
    ],
    "ShipAddr": {
      "City": "South Orange",
      "Line1": "350 Mountain View Dr.",
      "PostalCode": "07079",
      "Lat": "40.7633073",
      "Long": "-74.2426072",
      "CountrySubDivisionCode": "NJ",
      "Id": "15"
    },
    "BillAddr": {
      "Line4": "South Orange, NJ  07079",
      "Line3": "350 Mountain View Dr.",
      "Id": "73",
      "Line1": "Karen Pye",
      "Line2": "Pye's Cakes"
    },
    "MetaData": {
      "CreateTime": "2014-09-17T15:35:07-07:00",
      "LastUpdatedTime": "2015-07-29T08:18:49-07:00"
    },
    "BillEmail": {
      "Address": "pyescakes@intuit.com"
    },
    "Id": "66"
  },
  "time": "2015-07-29T08:18:48.873-07:00"
}
```
