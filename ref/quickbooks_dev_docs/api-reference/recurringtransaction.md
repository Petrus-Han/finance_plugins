# RecurringTransaction

A RecurringTransaction object refers to scheduling the creation of transactions, setting up reminders, and creating transaction templates for later use. This feature is available in QuickBooks Online Essentials and Plus SKUs.

## The RecurringTransaction Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Optional | Unique identifier for this object. Sort order is ASC by default. System defined. |
| **RecurringInfo** | RecurringInfo | Required | Describes the recurring schedules for transactions. |
| **SyncToken** | String | Required for update | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. System defined. |
| **RecurDataRef** | ReferenceType, filterable, sortable | Optional | Reference to the recur template associated with the transaction. |
| **MetaData** | ModificationMetaData, filterable | Optional | Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications. |
| **Type** | String, filterable | - | Specifies the list of entities that are supported for recurring transactions: Bill, Purchase, CreditMemo, Deposit, Estimate, Invoice, JournalEntry, RefundReceipt, SalesReceipt, Transfer, VendorCredit or PurchaseOrder. |

### RecurringInfo Object

| Attribute | Type | Description |
|-----------|------|-------------|
| **Active** | Boolean | Whether the recurring transaction is active. |
| **RecurType** | String | Type of recurring transaction: "Automated", "Reminder", or "Unscheduled". |
| **Name** | String | Name of the recurring transaction template. |
| **ScheduleInfo** | Object | Contains scheduling details. |

### ScheduleInfo Object

| Attribute | Type | Description |
|-----------|------|-------------|
| **StartDate** | Date | Start date for the recurring transaction. |
| **EndDate** | Date | End date for the recurring transaction (optional). |
| **MaxOccurrences** | Integer | Maximum number of occurrences (optional). |
| **IntervalType** | String | Interval type: "Daily", "Weekly", "Monthly", "Yearly". |
| **NumInterval** | Integer | Number of intervals between occurrences. |
| **DayOfMonth** | Integer | Day of the month for monthly recurrence. |
| **DayOfWeek** | String | Day of the week for weekly recurrence. |
| **DaysBefore** | Integer | Days before to create the transaction. |
| **NextDate** | Date | Next scheduled date. |
| **PreviousDate** | Date | Previous occurrence date. |

### Sample Object

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "maxResults": 1,
    "RecurringTransaction": [
      {
        "Bill": {
          "SyncToken": "0",
          "domain": "QBO",
          "RecurringInfo": {
            "Active": true,
            "RecurType": "Automated",
            "ScheduleInfo": {
              "NumInterval": 1,
              "NextDate": "2020-08-01",
              "DayOfMonth": 1,
              "PreviousDate": "2020-07-01",
              "IntervalType": "Monthly"
            },
            "Name": "Telephone Bill"
          },
          "RecurDataRef": {
            "value": "2"
          },
          "CurrencyRef": {
            "name": "United States Dollar",
            "value": "USD"
          },
          "TotalAmt": 74.36,
          "APAccountRef": {
            "name": "Name_01ff6",
            "value": "33"
          },
          "Id": "20",
          "sparse": false,
          "VendorRef": {
            "name": "Cal Telephone",
            "value": "32"
          },
          "Line": [
            {
              "Description": "Monthly Phone Bill",
              "DetailType": "AccountBasedExpenseLineDetail",
              "LineNum": 1,
              "Amount": 74.36,
              "Id": "1",
              "AccountBasedExpenseLineDetail": {
                "TaxCodeRef": {
                  "value": "NON"
                },
                "AccountRef": {
                  "name": "Utilities:Telephone",
                  "value": "77"
                },
                "BillableStatus": "NotBillable"
              }
            }
          ],
          "Balance": 74.36,
          "SalesTermRef": {
            "value": "3"
          },
          "MetaData": {
            "CreateTime": "2019-02-17T15:27:25-08:00",
            "LastUpdatedTime": "2020-07-05T01:19:13-07:00"
          }
        }
      }
    ]
  },
  "time": "2020-07-09T10:18:02.049-07:00"
}
```

## Supported Transaction Types

The following transaction types can be used with RecurringTransaction:

- Bill
- Purchase
- CreditMemo
- Deposit
- Estimate
- Invoice
- JournalEntry
- RefundReceipt
- SalesReceipt
- Transfer
- VendorCredit
- PurchaseOrder

## Create a RecurringTransaction

A RecurringTransaction object must have at least one line that describes an item.

A RecurringTransaction object must have a DepositToAccountRef (for applicable transaction types).

If the billing address is not provided, the customer address is used to fill those values.

TaxCode.CustomSalesTax cannot be used as TxnTaxCodeRef. This taxcode is reserved to mark the transaction as created using old sales tax model with no predefined tax rates. You cannot create or update a transaction that implements TaxCode.CustomSalesTax.

### Request

```
POST /v3/company/<realmID>/recurringtransaction
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Minimum Required Elements

- **RecurringInfo**: Contains the recurring schedule information
- The minimum payload for the underlying transaction type

### Request Body (Invoice Example)

```json
{
  "Invoice": {
    "AllowOnlineACHPayment": false,
    "ShipFromAddr": {
      "Id": "713",
      "Line1": "123 Sierra Way, San Pablo, CA, 87999, USA"
    },
    "CurrencyRef": {
      "name": "United States Dollar",
      "value": "USD"
    },
    "HomeBalance": 55,
    "PrintStatus": "NeedToPrint",
    "BillEmail": {
      "Address": "Travis@Waldron.com"
    },
    "DeliveryInfo": {
      "DeliveryType": "Email"
    },
    "TotalAmt": 55,
    "Line": [
      {
        "LineNum": 1,
        "Amount": 55,
        "SalesItemLineDetail": {
          "ItemRef": {
            "name": "Hours",
            "value": "2"
          },
          "Qty": 1,
          "TaxCodeRef": {
            "value": "NON"
          },
          "ItemAccountRef": {
            "name": "Services",
            "value": "1"
          },
          "UnitPrice": 55,
          "TaxClassificationRef": {
            "value": "EUC-99990201-V1-00020000"
          }
        },
        "Id": "1",
        "DetailType": "SalesItemLineDetail"
      },
      {
        "DetailType": "SubTotalLineDetail",
        "Amount": 55,
        "SubTotalLineDetail": {}
      }
    ],
    "ApplyTaxAfterDiscount": false,
    "RecurDataRef": {
      "value": "4"
    },
    "TaxExemptionRef": {},
    "Balance": 55,
    "CustomerRef": {
      "name": "Travis Waldron",
      "value": "26"
    },
    "TxnTaxDetail": {
      "TotalTax": 0
    },
    "AllowOnlineCreditCardPayment": false,
    "LinkedTxn": [],
    "RecurringInfo": {
      "Active": true,
      "RecurType": "Automated",
      "ScheduleInfo": {
        "StartDate": "2020-09-01",
        "MaxOccurrences": 10,
        "IntervalType": "Monthly",
        "DaysBefore": 2,
        "NextDate": "2020-09-01",
        "NumInterval": 1,
        "DayOfMonth": 1
      },
      "Name": "RecurTemplate2"
    },
    "ExchangeRate": 1,
    "ShipAddr": {
      "City": "Monlo Park",
      "Line1": "78 First St.",
      "PostalCode": "94304",
      "Lat": "37.4585825",
      "Long": "-122.1352789",
      "CountrySubDivisionCode": "CA",
      "Id": "27"
    },
    "DepartmentRef": {
      "name": "DeptName100768f890d64",
      "value": "1"
    },
    "EmailStatus": "NeedToSend",
    "BillAddr": {
      "City": "Monlo Park",
      "Line1": "78 First St.",
      "PostalCode": "94304",
      "Lat": "37.4585825",
      "Long": "-122.1352789",
      "CountrySubDivisionCode": "CA",
      "Id": "27"
    },
    "FreeFormAddress": true,
    "CustomField": [
      {
        "DefinitionId": "1",
        "Type": "StringType",
        "Name": "Crew #"
      }
    ],
    "HomeTotalAmt": 55,
    "AllowOnlinePayment": false,
    "AllowIPNPayment": false
  }
}
```

### Response

```json
{
  "time": "2020-08-13T17:04:57.367-07:00",
  "RecurringTransaction": {
    "Invoice": {
      "AllowOnlineACHPayment": false,
      "domain": "QBO",
      "CurrencyRef": {
        "name": "United States Dollar",
        "value": "USD"
      },
      "PrintStatus": "NeedToPrint",
      "BillEmail": {
        "Address": "Travis@Waldron.com"
      },
      "DeliveryInfo": {
        "DeliveryType": "Email"
      },
      "TotalAmt": 55.0,
      "Line": [
        {
          "LineNum": 1,
          "Amount": 55.0,
          "SalesItemLineDetail": {
            "TaxCodeRef": {
              "value": "NON"
            },
            "Qty": 1,
            "UnitPrice": 55,
            "ItemRef": {
              "name": "Hours",
              "value": "2"
            }
          },
          "Id": "1",
          "DetailType": "SalesItemLineDetail"
        },
        {
          "DetailType": "SubTotalLineDetail",
          "Amount": 55.0,
          "SubTotalLineDetail": {}
        }
      ],
      "DueDate": "2020-08-13",
      "MetaData": {
        "CreateTime": "2020-08-13T17:04:57-07:00",
        "LastUpdatedTime": "2020-08-13T17:04:57-07:00"
      },
      "sparse": false,
      "RecurDataRef": {
        "value": "6"
      },
      "Balance": 55.0,
      "CustomerRef": {
        "name": "Travis Waldron",
        "value": "26"
      },
      "TxnTaxDetail": {
        "TotalTax": 0
      },
      "AllowOnlineCreditCardPayment": false,
      "SyncToken": "0",
      "LinkedTxn": [],
      "RecurringInfo": {
        "Active": true,
        "RecurType": "Automated",
        "ScheduleInfo": {
          "StartDate": "2020-09-01",
          "MaxOccurrences": 10,
          "IntervalType": "Monthly",
          "DaysBefore": 2,
          "NextDate": "2020-09-01",
          "NumInterval": 1,
          "DayOfMonth": 1
        },
        "Name": "RecurTemplate2"
      },
      "ExchangeRate": 1,
      "ShipAddr": {
        "CountrySubDivisionCode": "CA",
        "City": "Monlo Park",
        "PostalCode": "94304",
        "Id": "717",
        "Line1": "78 First St."
      },
      "HomeTotalAmt": 55.0,
      "DepartmentRef": {
        "name": "DeptName100768f890d64",
        "value": "1"
      },
      "EmailStatus": "NeedToSend",
      "BillAddr": {
        "CountrySubDivisionCode": "CA",
        "City": "Monlo Park",
        "PostalCode": "94304",
        "Id": "716",
        "Line1": "78 First St."
      },
      "ApplyTaxAfterDiscount": false,
      "CustomField": [
        {
          "DefinitionId": "1",
          "Type": "StringType",
          "Name": "Crew #"
        }
      ],
      "Id": "1483",
      "AllowOnlinePayment": false,
      "AllowIPNPayment": false
    }
  }
}
```

## Read a RecurringTransaction

Retrieves the details of a RecurringTransaction object.

### Request

```
GET /v3/company/<realmID>/recurringtransaction/<recurringtransactionId>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

Returns the RecurringTransaction object.

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "maxResults": 1,
    "RecurringTransaction": [
      {
        "Bill": {
          "SyncToken": "0",
          "domain": "QBO",
          "RecurringInfo": {
            "Active": true,
            "RecurType": "Automated",
            "ScheduleInfo": {
              "NumInterval": 1,
              "NextDate": "2020-08-01",
              "DayOfMonth": 1,
              "PreviousDate": "2020-07-01",
              "IntervalType": "Monthly"
            },
            "Name": "Telephone Bill"
          },
          "RecurDataRef": {
            "value": "2"
          },
          "CurrencyRef": {
            "name": "United States Dollar",
            "value": "USD"
          },
          "TotalAmt": 74.36,
          "APAccountRef": {
            "name": "Name_01ff6",
            "value": "33"
          },
          "Id": "20",
          "sparse": false,
          "VendorRef": {
            "name": "Cal Telephone",
            "value": "32"
          },
          "Line": [
            {
              "Description": "Monthly Phone Bill",
              "DetailType": "AccountBasedExpenseLineDetail",
              "LineNum": 1,
              "Amount": 74.36,
              "Id": "1",
              "AccountBasedExpenseLineDetail": {
                "TaxCodeRef": {
                  "value": "NON"
                },
                "AccountRef": {
                  "name": "Utilities:Telephone",
                  "value": "77"
                },
                "BillableStatus": "NotBillable"
              }
            }
          ],
          "Balance": 74.36,
          "SalesTermRef": {
            "value": "3"
          },
          "MetaData": {
            "CreateTime": "2019-02-17T15:27:25-08:00",
            "LastUpdatedTime": "2020-07-05T01:19:13-07:00"
          }
        }
      }
    ]
  },
  "time": "2020-07-09T10:18:02.049-07:00"
}
```

## Query a RecurringTransaction

### Request

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content-Type: text/plain
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Sample Query

```sql
Select * From RecurringTransaction
```

### Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "maxResults": 3,
    "RecurringTransaction": [
      {
        "Invoice": {
          "AllowOnlineACHPayment": false,
          "domain": "QBO",
          "CurrencyRef": {
            "name": "United States Dollar",
            "value": "USD"
          },
          "PrintStatus": "NeedToPrint",
          "TotalAmt": 11111.0,
          "Line": [
            {
              "LineNum": 1,
              "Amount": 11111.0,
              "SalesItemLineDetail": {
                "TaxCodeRef": {
                  "value": "NON"
                },
                "ItemRef": {
                  "name": "Garden Supplies3223",
                  "value": "211"
                }
              },
              "Id": "1",
              "DetailType": "SalesItemLineDetail"
            },
            {
              "DetailType": "SubTotalLineDetail",
              "Amount": 11111.0,
              "SubTotalLineDetail": {}
            }
          ],
          "ApplyTaxAfterDiscount": false,
          "RecurDataRef": {
            "value": "4"
          },
          "Balance": 11111.0,
          "CustomerRef": {
            "name": "0c9ff29a3c3640cdaf7a",
            "value": "401"
          },
          "TxnTaxDetail": {
            "TotalTax": 0
          },
          "AllowOnlineCreditCardPayment": false,
          "SyncToken": "0",
          "LinkedTxn": [],
          "RecurringInfo": {
            "Active": true,
            "RecurType": "Automated",
            "ScheduleInfo": {
              "NumInterval": 1,
              "NextDate": "2020-08-01",
              "DayOfMonth": 1,
              "IntervalType": "Monthly"
            },
            "Name": "Testing"
          },
          "EmailStatus": "NotSet",
          "sparse": false,
          "MetaData": {
            "CreateTime": "2020-07-06T14:24:00-07:00",
            "LastUpdatedTime": "2020-07-06T14:24:00-07:00"
          },
          "CustomField": [
            {
              "DefinitionId": "1",
              "Type": "StringType",
              "Name": "Crew #"
            },
            {
              "DefinitionId": "2",
              "Type": "StringType",
              "Name": "PO #"
            },
            {
              "DefinitionId": "3",
              "Type": "StringType",
              "Name": "Sales #"
            }
          ],
          "Id": "1537",
          "AllowOnlinePayment": false,
          "AllowIPNPayment": false
        }
      },
      {
        "Bill": {
          "SyncToken": "0",
          "domain": "QBO",
          "RecurringInfo": {
            "Active": true,
            "RecurType": "Automated",
            "ScheduleInfo": {
              "NumInterval": 1,
              "NextDate": "2020-08-01",
              "DayOfMonth": 1,
              "PreviousDate": "2020-07-01",
              "IntervalType": "Monthly"
            },
            "Name": "Telephone Bill"
          },
          "RecurDataRef": {
            "value": "2"
          },
          "CurrencyRef": {
            "name": "United States Dollar",
            "value": "USD"
          },
          "TotalAmt": 74.36,
          "APAccountRef": {
            "name": "Name_01ff6",
            "value": "33"
          },
          "Id": "20",
          "sparse": false,
          "VendorRef": {
            "name": "Cal Telephone",
            "value": "32"
          },
          "Line": [
            {
              "Description": "Monthly Phone Bill",
              "DetailType": "AccountBasedExpenseLineDetail",
              "LineNum": 1,
              "Amount": 74.36,
              "Id": "1",
              "AccountBasedExpenseLineDetail": {
                "TaxCodeRef": {
                  "value": "NON"
                },
                "AccountRef": {
                  "name": "Utilities:Telephone",
                  "value": "77"
                },
                "BillableStatus": "NotBillable"
              }
            }
          ],
          "Balance": 74.36,
          "SalesTermRef": {
            "value": "3"
          },
          "MetaData": {
            "CreateTime": "2019-02-17T15:27:25-08:00",
            "LastUpdatedTime": "2020-07-05T01:19:13-07:00"
          }
        }
      },
      {
        "Bill": {
          "SyncToken": "0",
          "domain": "QBO",
          "RecurringInfo": {
            "Active": true,
            "RecurType": "Automated",
            "ScheduleInfo": {
              "NumInterval": 1,
              "NextDate": "2020-08-01",
              "DayOfMonth": 1,
              "PreviousDate": "2020-07-01",
              "IntervalType": "Monthly"
            },
            "Name": "Monthly Building Lease"
          },
          "RecurDataRef": {
            "value": "3"
          },
          "CurrencyRef": {
            "name": "United States Dollar",
            "value": "USD"
          },
          "TotalAmt": 900.0,
          "APAccountRef": {
            "name": "Name_01ff6",
            "value": "33"
          },
          "Id": "23",
          "sparse": false,
          "VendorRef": {
            "name": "Hall Properties",
            "value": "40"
          },
          "Line": [
            {
              "Description": "Building Lease",
              "DetailType": "AccountBasedExpenseLineDetail",
              "LineNum": 1,
              "Amount": 900.0,
              "Id": "1",
              "AccountBasedExpenseLineDetail": {
                "TaxCodeRef": {
                  "value": "NON"
                },
                "AccountRef": {
                  "name": "Rent or Lease",
                  "value": "17"
                },
                "BillableStatus": "NotBillable"
              }
            }
          ],
          "Balance": 900.0,
          "SalesTermRef": {
            "value": "3"
          },
          "MetaData": {
            "CreateTime": "2019-02-17T15:31:18-08:00",
            "LastUpdatedTime": "2020-07-05T01:19:12-07:00"
          }
        }
      }
    ]
  },
  "time": "2020-07-06T17:33:54.221-07:00"
}
```

## Delete a RecurringTransaction

This operation deletes the RecurringTransaction object specified in the request body. Include a minimum of RecurringTransaction.Id and SyncToken in the request body. You must unlink any linked transactions associated with the RecurringTransaction object before deleting it.

### Request

```
POST /v3/company/<realmID>/recurringtransaction?operation=delete
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body (Invoice Example)

```json
{
  "Invoice": {
    "SyncToken": "0",
    "Id": "1483"
  }
}
```

### Response

```json
{
  "time": "2020-08-13T17:40:08.008-07:00",
  "RecurringTransaction": {
    "status": "Deleted",
    "domain": "QBO",
    "Invoice": {
      "Id": "1483"
    }
  }
}
```
