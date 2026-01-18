# Categorize Income and Expenses

> Source: https://developer.intuit.com/app/developer/qbo/docs/workflows/categorize-income-and-expenses

QuickBooks Online provides a way for your app to track different segments of the business apart from a particular client or project. For example, segments of a landscaping business could be: landscaping, maintenance, design, and overhead. Then, as you create sales and expense transactions, consistently designate the class corresponding to the segment to which they belong. The transactions become organized into segments across income and expenses, providing you a segment-wide view of your business.

## Prerequisites

To follow along, you'll need a sandbox or another QuickBooks company populated with:
- A chart of accounts
- Customers
- Items
- A list of business segments you wish to track

The examples in this tutorial use the [sandbox company](https://developer.intuit.com/app/developer/qbo/docs/develop/sandboxes).

---

## Verify Class Tracking Availability

Tracking business segments and class tracking in general is **available with QuickBooks Online Plus only**.

To determine the edition type with the QuickBooks Online API, query the value of the `CustomerInfo.Name` name/value pair, `OfferingSku`. 

The example below is excerpted from the [CompanyInfo](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/companyinfo) object where the value is set to `QuickBooks Online Plus`:

```json
{
   "CompanyInfo": {
      "CompanyName": "Sandbox Company_US_3",
      "LegalName": "Sandbox Company_US_3",
       ...
      "NameValue": [
       ...
        {
           "Name": "OfferingSku",
           "Value": "QuickBooks Online Plus"
        },
       ...
      ],
        ...
      "Id": "1",
      "SyncToken": "7",
      "MetaData": {
        "CreateTime": "2015-05-22T01:37:33-07:00",
        "LastUpdatedTime": "2016-03-21T12:21:13-07:00"
      }
   },
   "time": "2016-03-21T12:36:49.015-07:00"
}
```

---

## Enabling Class Tracking

In order to have class tracking available to transactions, you must first enable it.

### From the QuickBooks Online UI
Under **Categories** in QuickBooks Company Settings, click the checkbox next to **Track classes**.

### From the QuickBooks Online API
With the [Preferences](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/preferences) resource, set either:
- `Preferences.AccountingInfoPrefs.ClassTrackingPerTxn` to `true`, OR
- `Preferences.AccountingInfoPrefs.ClassTrackingPerTxnLine` to `true`

> **Note**
> - For **sales transactions**, class tracking is supported at either the transaction level or line level.
> - For **expense transactions**, class tracking is supported **only at the line level**.

---

## Creating Classes

Once class tracking is enabled, build up the list of classes and sub-classes you wish to track.

### From the QuickBooks Online UI
Add classes via the Classes list page.

### From the QuickBooks Online API
Create classes using the [Class](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/class) resource.

---

## Using Classes in Transactions

You can add class designations to transactions, either at the line level or transaction level, based on the company file configuration. In the QuickBooks Online API, transactions supporting class tracking provide a `ClassRef` attribute.

### Steps to Track Classes

**Step 1: Query available classes**

Query the [Class](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/class) resource to get a list of available classes defined for the company.

```http
GET https://quickbooks.api.intuit.com/v3/company/<CompanyId>/query?query=select * from class
```

**Response:**

```json
{
   "QueryResponse": {
      "Class": [
         {
            "Name": "Landscape",
            "SubClass": false,
            "FullyQualifiedName": "Landscape",
            "Active": true,
            "domain": "QBO",
            "sparse": false,
            "Id": "5000000000000013171",
            "SyncToken": "0",
            "MetaData": {
              "CreateTime": "2016-03-21T14:13:30-07:00",
              "LastUpdatedTime": "2016-03-21T14:13:30-07:00"
            }
         },
         {
            "Name": "Maintenance",
            "SubClass": false,
            "FullyQualifiedName": "Maintenance",
            "Active": true,
            "domain": "QBO",
            "sparse": false,
            "Id": "5000000000000013172",
            "SyncToken": "0",
            "MetaData": {
              "CreateTime": "2016-03-21T14:13:41-07:00",
              "LastUpdatedTime": "2016-03-21T14:13:41-07:00"
            }
         },
         {
            "Name": "Overhead",
            "SubClass": false,
            "FullyQualifiedName": "Overhead",
            "Active": true,
            "domain": "QBO",
            "sparse": false,
            "Id": "5000000000000013174",
            "SyncToken": "0",
            "MetaData": {
              "CreateTime": "2016-03-21T15:57:06-07:00",
              "LastUpdatedTime": "2016-03-21T15:57:06-07:00"
            }
         },
         {
            "Name": "Sales",
            "SubClass": false,
            "FullyQualifiedName": "Sales",
            "Active": true,
            "domain": "QBO",
            "sparse": false,
            "Id": "5000000000000013173",
            "SyncToken": "0",
            "MetaData": {
              "CreateTime": "2016-03-21T14:13:51-07:00",
              "LastUpdatedTime": "2016-03-21T14:13:51-07:00"
            }
         }
      ],
      "startPosition": 1,
      "maxResults": 4,
      "totalCount": 4
   },
   "time": "2016-03-22T09:27:59.236-07:00"
}
```

Note the `Class.Id` and `Class.Name` for the class you wish to use in the transaction.

**Step 2: Use the class in a transaction**

Build up the transaction's `ClassRef` attribute with values from the Class object:
- Set `ClassRef.value` to `Class.Id`
- Set `ClassRef.name` to `Class.Name`

---

## Line-level Classes

Set a line-level class in an Invoice object. Class tracking is configured as follows:
- `Preferences.AccountingInfoPrefs.ClassTrackingPerTxn` set to `false`
- `Preferences.AccountingInfoPrefs.ClassTrackingPerTxnLine` set to `true`

---

## Transaction-level Classes

Set a transaction-level class in an Invoice object. Class tracking is configured as follows:
- `Preferences.AccountingInfoPrefs.ClassTrackingPerTxn` set to `true`
- `Preferences.AccountingInfoPrefs.ClassTrackingPerTxnLine` set to `false`

---

## Reporting on Classes

The QuickBooks Online API provides the [Sales by Class](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/report-entities/salesbyclasssummary) report API, presenting a summary of how class tracking breaks down across all the transactions.

---

## Mercury Sync Application

For Mercury bank transaction sync:

1. **Query existing classes** before creating transactions
2. **Set ClassRef** on Purchase/Deposit line items to categorize Mercury transactions
3. **Use Sales by Class reports** to verify proper categorization

### Example: Categorizing a Mercury Transaction

```python
# When creating a Purchase from Mercury transaction
purchase_data = {
    "PaymentType": "Cash",
    "AccountRef": {"value": "mercury_bank_account_id"},
    "Line": [{
        "DetailType": "AccountBasedExpenseLineDetail",
        "Amount": 100.00,
        "AccountBasedExpenseLineDetail": {
            "AccountRef": {"value": "expense_account_id"},
            "ClassRef": {
                "value": "5000000000000013171",  # Class.Id
                "name": "Landscape"               # Class.Name
            }
        }
    }]
}
```

---

## Learn More

- [Class API Reference](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/class)
- [Preferences API Reference](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/preferences)
- [Sales by Class Report](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/report-entities/salesbyclasssummary)
