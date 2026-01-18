# Preferences

The Preferences resource represents a set of company preferences that control application behavior in QuickBooks Online. They are mostly exposed as read-only through the Preferences endpoint with only a very small subset of them available as writable. Preferences are not necessarily honored when making requests via the QuickBooks API because a lot of them control UI behavior in the application and may not be applicable for apps.

## Business Rules

- The create operation is not supported.
- The read request retrieves all preferences. There is no notion of preference objects or object IDs.
- Update operations are supported for a limited subset of preferences, which are not marked as readonly.
- The Delete operation is not supported.
- Query is supported with sorting and filtering enabled for Metadata timestamp attributes. Pagination is not supported.
- OtherPrefs type is used as an extension mechanism to contain additional attributes as Name/Value pairs.

## The Preferences Object

### Core Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String | Required for update, read only, system defined | Unique identifier for this object. Sort order is ASC by default. |
| **SyncToken** | String | Required for update, read only, system defined | Version number of the object. It is used to lock an object for use by one app at a time. |
| **MetaData** | ModificationMetaData | Optional | Descriptive information about the object. |

### Preference Categories

#### AccountingInfoPrefs
Company accounting information preferences.

| Attribute | Type | Description |
|-----------|------|-------------|
| **FirstMonthOfFiscalYear** | MonthEnum | The first month of the fiscal year. |
| **UseAccountNumbers** | Boolean | Specifies whether account numbers are enabled. |
| **TaxYearMonth** | MonthEnum | Tax year starting month. |
| **ClassTrackingPerTxn** | Boolean | Class tracking enabled for transactions. |
| **ClassTrackingPerTxnLine** | Boolean | Class tracking enabled at line item level. |
| **TrackDepartments** | Boolean | Location tracking enabled. |
| **DepartmentTerminology** | String | Term used for department/location. |
| **BookCloseDate** | Date | Date books were closed. |
| **CustomerTerminology** | String | Term used for customers. |

#### ProductAndServicesPrefs
Preferences for products and services.

| Attribute | Type | Description |
|-----------|------|-------------|
| **ForSales** | Boolean | Products/services sold to customers enabled. |
| **ForPurchase** | Boolean | Products/services bought from vendors enabled. |
| **QuantityWithPriceAndRate** | Boolean | Quantity on hand tracking enabled. |
| **QuantityOnHand** | Boolean | Inventory tracking enabled. |

#### SalesFormsPrefs
Sales form preferences.

| Attribute | Type | Description |
|-----------|------|-------------|
| **CustomField** | CustomField[] | Up to 3 custom fields for sales forms. |
| **AllowDeposit** | Boolean | Allow deposits on sales forms. |
| **AllowDiscount** | Boolean | Allow discounts on sales forms. |
| **AllowEstimates** | Boolean | Estimates enabled. |
| **AllowServiceDate** | Boolean | Service date field enabled. |
| **AllowShipping** | Boolean | Shipping enabled. |
| **DefaultTerms** | ReferenceType | Default payment terms. |
| **DefaultCustomerMessage** | String | Default customer message. |
| **DefaultDiscountAccount** | ReferenceType | Default discount account. |
| **DefaultShippingAccount** | ReferenceType | Default shipping account. |
| **ETransactionEnabledStatus** | String | E-transaction status. |
| **ETransactionAttachPDF** | Boolean | Attach PDF to e-transactions. |
| **ETransactionPaymentEnabled** | Boolean | E-payment enabled. |
| **IPNSupportEnabled** | Boolean | IPN support enabled. |
| **CustomTxnNumbers** | Boolean | Custom transaction numbers enabled. |
| **UsingPriceLevels** | Boolean | Price levels enabled. |
| **UsingProgressInvoicing** | Boolean | Progress invoicing enabled. |

#### VendorAndPurchasesPrefs
Vendor and purchase preferences.

| Attribute | Type | Description |
|-----------|------|-------------|
| **BillableExpenseTracking** | Boolean | Billable expense tracking enabled. |
| **DefaultTerms** | ReferenceType | Default payment terms for bills. |
| **DefaultMarkup** | Decimal | Default markup percentage. |
| **TrackingByCustomer** | Boolean | Expense tracking by customer enabled. |
| **POCustomField** | CustomField[] | Up to 3 custom fields for purchase orders. |
| **MsgToVendors** | String | Default message to vendors. |

#### TimeTrackingPrefs
Time tracking preferences.

| Attribute | Type | Description |
|-----------|------|-------------|
| **UseServices** | Boolean | Time tracking enabled. |
| **BillCustomers** | Boolean | Bill customers for time enabled. |
| **ShowBillRateToAll** | Boolean | Show bill rate to all users. |
| **WorkWeekStartDate** | WeekEnum | Work week start day. |
| **MarkTimeEntriesBillable** | Boolean | Auto-mark time entries as billable. |

#### TaxPrefs
Tax preferences.

| Attribute | Type | Description |
|-----------|------|-------------|
| **UsingSalesTax** | Boolean | Sales tax enabled. |
| **TaxGroupCodeRef** | ReferenceType | Default tax code. |
| **PartnerTaxEnabled** | Boolean | Partner tax enabled. |

#### CurrencyPrefs
Multi-currency preferences.

| Attribute | Type | Description |
|-----------|------|-------------|
| **MultiCurrencyEnabled** | Boolean | Multi-currency enabled. |
| **HomeCurrency** | ReferenceType | Home currency code. |

#### ReportPrefs
Report preferences.

| Attribute | Type | Description |
|-----------|------|-------------|
| **ReportBasis** | ReportBasisEnum | Default report basis (Cash/Accrual). |
| **CalcAgingReportFromTxnDate** | Boolean | Calculate aging from transaction date. |

#### EmailMessagesPrefs
Email message preferences.

| Attribute | Type | Description |
|-----------|------|-------------|
| **InvoiceMessage** | EmailMessage | Default invoice email message. |
| **EstimateMessage** | EmailMessage | Default estimate email message. |
| **SalesReceiptMessage** | EmailMessage | Default sales receipt email message. |
| **StatementMessage** | EmailMessage | Default statement email message. |

#### OtherPrefs
Extension mechanism for additional preferences as Name/Value pairs.

| Attribute | Type | Description |
|-----------|------|-------------|
| **NameValue** | NameValue[] | Array of name-value pairs for other preferences. |

## Query Preferences

### Returns

Returns the results of the query.

### Request URL

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content type: text/plain
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Sample Query

```sql
select * from Preferences
```

## Read Preferences

Retrieves the Preferences object for the company.

### Returns

Returns the Preferences object.

### Request URL

```
GET /v3/company/<realmID>/preferences
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Sample Response

```json
{
  "Preferences": {
    "AccountingInfoPrefs": {
      "FirstMonthOfFiscalYear": "January",
      "UseAccountNumbers": true,
      "TaxYearMonth": "January",
      "ClassTrackingPerTxn": false,
      "ClassTrackingPerTxnLine": true,
      "TrackDepartments": true,
      "DepartmentTerminology": "Location",
      "BookCloseDate": "2015-12-31",
      "CustomerTerminology": "Customers"
    },
    "ProductAndServicesPrefs": {
      "ForSales": true,
      "ForPurchase": true,
      "QuantityWithPriceAndRate": true,
      "QuantityOnHand": true
    },
    "SalesFormsPrefs": {
      "AllowDeposit": true,
      "AllowDiscount": true,
      "AllowEstimates": true,
      "AllowServiceDate": false,
      "AllowShipping": false,
      "CustomTxnNumbers": false,
      "ETransactionEnabledStatus": "Enabled",
      "ETransactionAttachPDF": false,
      "ETransactionPaymentEnabled": false,
      "IPNSupportEnabled": false,
      "UsingPriceLevels": false,
      "UsingProgressInvoicing": false
    },
    "VendorAndPurchasesPrefs": {
      "BillableExpenseTracking": true,
      "TrackingByCustomer": true
    },
    "TimeTrackingPrefs": {
      "UseServices": true,
      "BillCustomers": true,
      "ShowBillRateToAll": false,
      "WorkWeekStartDate": "Monday",
      "MarkTimeEntriesBillable": true
    },
    "TaxPrefs": {
      "UsingSalesTax": true
    },
    "CurrencyPrefs": {
      "MultiCurrencyEnabled": false,
      "HomeCurrency": {
        "value": "USD"
      }
    },
    "ReportPrefs": {
      "ReportBasis": "Accrual",
      "CalcAgingReportFromTxnDate": false
    },
    "OtherPrefs": {
      "NameValue": [
        {
          "Name": "SalesFormsPrefs.DefaultCustomerMessage",
          "Value": "Thank you for your business!"
        }
      ]
    },
    "Id": "1",
    "SyncToken": "5",
    "MetaData": {
      "CreateTime": "2015-07-24T10:35:08-07:00",
      "LastUpdatedTime": "2015-07-24T10:35:08-07:00"
    }
  },
  "time": "2015-07-24T10:35:08.982-07:00"
}
```

## Full Update Preferences

Use this operation to update the writable preferences. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL.

### Request URL

```
POST /v3/company/<realmID>/preferences
Content type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Writable Fields

The following preferences can be updated:

- **AccountingInfoPrefs**: FirstMonthOfFiscalYear, TaxYearMonth, ClassTrackingPerTxn, ClassTrackingPerTxnLine, TrackDepartments, DepartmentTerminology, BookCloseDate, CustomerTerminology
- **ProductAndServicesPrefs**: ForSales, ForPurchase, QuantityWithPriceAndRate, QuantityOnHand
- **SalesFormsPrefs**: CustomField (limited), AllowDeposit, AllowDiscount, AllowEstimates, AllowServiceDate, AllowShipping, DefaultTerms, DefaultCustomerMessage, CustomTxnNumbers, ETransactionAttachPDF, ETransactionPaymentEnabled
- **VendorAndPurchasesPrefs**: BillableExpenseTracking, DefaultTerms, DefaultMarkup, TrackingByCustomer, POCustomField (limited), MsgToVendors
- **TimeTrackingPrefs**: UseServices, BillCustomers, ShowBillRateToAll, WorkWeekStartDate, MarkTimeEntriesBillable
- **TaxPrefs**: UsingSalesTax, TaxGroupCodeRef, PartnerTaxEnabled
- **EmailMessagesPrefs**: InvoiceMessage, EstimateMessage, SalesReceiptMessage, StatementMessage
- **OtherPrefs**: NameValue (for certain keys)

### Request Body Example

```json
{
  "SyncToken": "5",
  "Id": "1",
  "AccountingInfoPrefs": {
    "FirstMonthOfFiscalYear": "January",
    "ClassTrackingPerTxnLine": true,
    "TrackDepartments": true,
    "DepartmentTerminology": "Location"
  },
  "SalesFormsPrefs": {
    "AllowDeposit": true,
    "AllowDiscount": true,
    "AllowEstimates": true,
    "CustomTxnNumbers": false
  },
  "VendorAndPurchasesPrefs": {
    "BillableExpenseTracking": true,
    "TrackingByCustomer": true
  },
  "TimeTrackingPrefs": {
    "UseServices": true,
    "BillCustomers": true,
    "ShowBillRateToAll": false,
    "WorkWeekStartDate": "Monday"
  }
}
```

### Response

Returns the updated Preferences object.
