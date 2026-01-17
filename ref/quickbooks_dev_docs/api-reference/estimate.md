# Estimate

The Estimate represents a proposal for a financial transaction from a business to a customer for goods or services proposed to be sold, including proposed pricing.

## The Estimate Object

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **Id** | String, read only, filterable, sortable | Unique identifier for this object. Sort order is ASC by default. *Required for update* |
| **CustomerRef** | ReferenceType, filterable | Reference to a customer or job. *Required* |
| **SyncToken** | String, read only | Version number of the object. *Required for update* |
| **ShipFromAddr** | PhysicalAddress | Identifies the address where the goods are shipped from. Required if automated sales tax is enabled and automated tax calculations are being used. *Conditionally required, minorVersion: 35* |
| **CurrencyRef** | CurrencyRefType | Reference to the currency. Required if multicurrency is enabled for the company. *Conditionally required* |
| **GlobalTaxCalculation** | GlobalTaxCalculationEnum | Method in which tax is applied. Allowed values: TaxExcluded, TaxInclusive, NotApplicable. Not applicable to US companies; required for non-US companies. *Conditionally required* |
| **ProjectRef** | ReferenceType, filterable | Reference to the Project ID associated with this transaction. *Conditionally required, minorVersion: 69* |
| **BillEmail** | EmailAddress | Identifies the e-mail address where the estimate is sent. If EmailStatus=NeedToSend, BillEmail is a required input. *Conditionally required* |
| **TxnDate** | Date, filterable, sortable | The date when this transaction occurred. |
| **ShipDate** | Date | Date for delivery of goods or services. |
| **ClassRef** | ReferenceType | Reference to the Class associated with the transaction. |
| **PrintStatus** | String | Printing status. Valid values: NotSet, NeedToPrint, PrintComplete. |
| **CustomField** | CustomField[] | One of, up to three custom fields for the transaction. |
| **SalesTermRef** | ReferenceType | Reference to the sales term associated with the transaction. |
| **TxnStatus** | String | Status: Accepted, Closed, Pending, Rejected, Converted. |
| **LinkedTxn** | LinkedTxn[] | Zero or more Invoice objects related to this transaction. |
| **AcceptedDate** | Date | Date estimate was accepted. |
| **ExpirationDate** | Date | Date by which estimate must be accepted before invalidation. |
| **TransactionLocationType** | String | The account location. For France locales only. *minorVersion: 4* |
| **DueDate** | Date, filterable, sortable | Date when the payment of the transaction is due. |
| **MetaData** | ModificationMetaData | Descriptive information about the object. Read only. |
| **DocNumber** | String (max 21 chars), filterable, sortable | Reference number for the transaction. |
| **PrivateNote** | String (max 4000 chars) | User entered, organization-private note about the transaction. |
| **Line** | Line[] | Individual line items of a transaction. Valid Line types include: SalesItemLine, GroupLine, DescriptionOnlyLine, DiscountLine and SubTotalLine. If taxable, limit of 750 lines. |
| **CustomerMemo** | MemoRef | User-entered message to the customer. |
| **EmailStatus** | String | Email status. Valid values: NotSet, NeedToSend, EmailSent. |
| **TxnTaxDetail** | TxnTaxDetail | Information for taxes charged on the transaction. |
| **AcceptedBy** | String | Name of customer who accepted the estimate. |
| **ExchangeRate** | Decimal | Currency exchange rate. Applicable if multicurrency is enabled. |
| **ShipAddr** | PhysicalAddress | Identifies the address where the goods must be shipped. |
| **DepartmentRef** | ReferenceType | Reference to a Department object. |
| **ShipMethodRef** | ReferenceType | Reference to the ShipMethod. |
| **BillAddr** | PhysicalAddress | Bill-to address of the Estimate. |
| **ApplyTaxAfterDiscount** | Boolean | If false, calculate tax first, then apply discount. If true, subtract discount first, then calculate tax. |
| **TotalAmt** | BigDecimal, read only | Total amount of the transaction. |
| **RecurDataRef** | ReferenceType, read only | Reference to the Recurring Transaction. *minorVersion: 52* |
| **TaxExemptionRef** | ReferenceType, read only | Reference to TaxExemption ID. *minorVersion: 21* |
| **HomeTotalAmt** | Decimal, read only | Total amount in home currency. |
| **FreeFormAddress** | Boolean, system defined | Denotes how ShipAddr is stored. |

### Sample Object

```json
{
  "Estimate": {
    "DocNumber": "1001",
    "SyncToken": "0",
    "domain": "QBO",
    "TxnStatus": "Pending",
    "BillEmail": {
      "Address": "Cool_Cars@intuit.com"
    },
    "TxnDate": "2015-03-26",
    "TotalAmt": 31.5,
    "CustomerRef": {
      "name": "Cool Cars",
      "value": "3"
    },
    "CustomerMemo": {
      "value": "Thank you for your business and have a great day!"
    },
    "ShipAddr": {
      "CountrySubDivisionCode": "CA",
      "City": "Half Moon Bay",
      "PostalCode": "94213",
      "Id": "104",
      "Line1": "65 Ocean Dr."
    },
    "ProjectRef": {
      "value": "39298034"
    },
    "PrintStatus": "NeedToPrint",
    "BillAddr": {
      "CountrySubDivisionCode": "CA",
      "City": "Half Moon Bay",
      "PostalCode": "94213",
      "Id": "103",
      "Line1": "65 Ocean Dr."
    },
    "sparse": false,
    "EmailStatus": "NotSet",
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
      },
      {
        "DetailType": "DiscountLineDetail",
        "Amount": 3.5,
        "DiscountLineDetail": {
          "DiscountAccountRef": {
            "name": "Discounts given",
            "value": "86"
          },
          "PercentBased": true,
          "DiscountPercent": 10
        }
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
    "Id": "177",
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "MetaData": {
      "CreateTime": "2015-03-26T13:25:05-07:00",
      "LastUpdatedTime": "2015-03-26T13:25:05-07:00"
    }
  },
  "time": "2015-03-26T13:25:05.473-07:00"
}
```

## Create an Estimate

An Estimate must have at least one line that describes an item and a reference to a customer. If shipping address and billing address are not provided, the address from the referenced Customer object is used.

### Request

```
POST /v3/company/<realmID>/estimate
Content-Type: application/json
```

**Production Base URL:** `https://quickbooks.api.intuit.com`
**Sandbox Base URL:** `https://sandbox-quickbooks.api.intuit.com`

### Required Fields

| Attribute | Type | Description |
|-----------|------|-------------|
| **Line** | Line[] | The minimum line item required is SalesItemLine or GroupLine. *Required* |
| **CustomerRef** | ReferenceType | Reference to a customer or job. *Required* |
| **ProjectRef** | ReferenceType | Reference to the Project ID. *Conditionally required, minorVersion: 69* |
| **CurrencyRef** | CurrencyRefType | Required if multicurrency is enabled. *Conditionally required* |

### Sample Request Body

```json
{
  "TotalAmt": 31.5,
  "BillEmail": {
    "Address": "Cool_Cars@intuit.com"
  },
  "CustomerMemo": {
    "value": "Thank you for your business and have a great day!"
  },
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
  ],
  "CustomerRef": {
    "name": "Cool Cars",
    "value": "3"
  }
}
```

## Delete an Estimate

This operation deletes the estimate object specified in the request body. Include a minimum of Estimate.Id and Estimate.SyncToken.

### Request

```
POST /v3/company/<realmID>/estimate?operation=delete
Content-Type: application/json
```

### Sample Request Body

```json
{
  "SyncToken": "3",
  "Id": "96"
}
```

### Sample Response

```json
{
  "Estimate": {
    "status": "Deleted",
    "domain": "QBO",
    "Id": "96"
  },
  "time": "2013-03-14T15:05:14.981-07:00"
}
```

## Get an Estimate as PDF

Returns the specified object in the response body as an Adobe Portable Document Format (PDF) file.

### Request

```
GET /v3/company/<realmID>/estimate/<estimateId>/pdf
Content-Type: application/pdf
```

## Query an Estimate

### Request

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content-Type: application/text
```

### Sample Query

```sql
select * from estimate where TxnDate < '2014-09-15'
```

## Read an Estimate

Retrieves the details of an estimate that has been previously created.

### Request

```
GET /v3/company/<realmID>/estimate/<estimateId>
```

## Send an Estimate

Sends the estimate via email. The Estimate.EmailStatus parameter is set to EmailSent. The Estimate.DeliveryInfo element is populated with sending information.

### Request

```
POST /v3/company/<realmID>/estimate/<estimateId>/send
Content-Type: application/octet-stream
```

Or with explicit email address:

```
POST /v3/company/<realmID>/estimate/<estimateId>/send?sendTo=<emailAddr>
```

### Sample Response

The response includes DeliveryInfo with DeliveryType and DeliveryTime, and EmailStatus set to "EmailSent".

## Sparse Update an Estimate

Sparse updating provides the ability to update a subset of properties for a given object; only elements specified in the request are updated. Missing elements are left untouched.

### Request

```
POST /v3/company/<realmID>/estimate
Content-Type: application/json
```

### Sample Request Body

```json
{
  "Id": "177",
  "SyncToken": "0",
  "sparse": true,
  "TxnStatus": "Accepted",
  "AcceptedBy": "John Smith",
  "AcceptedDate": "2015-03-27"
}
```

## Full Update an Estimate

Use this operation to update any of the writable fields of an existing estimate object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL.

### Request

```
POST /v3/company/<realmID>/estimate
Content-Type: application/json
```

### Required Fields

| Attribute | Type | Description |
|-----------|------|-------------|
| **Id** | String | Unique identifier. *Required for update* |
| **SyncToken** | String | Version number. *Required for update* |
| **CustomerRef** | ReferenceType | Reference to a customer. *Required* |
