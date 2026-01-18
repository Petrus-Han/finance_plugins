# TimeActivity

The TimeActivity object represents a record of time worked by a vendor or employee.

## The TimeActivity Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Required for update | Unique identifier for this object. Sort order is ASC by default. Read only, system defined. |
| **NameOf** | String | Required | Enumeration of time activity types. Required in conjunction with either EmployeeRef or VendorRef attributes for create operations. Valid values: Vendor or Employee. |
| **SyncToken** | String | Required for update | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. Read only, system defined. |
| **TxnDate** | Date, filterable, sortable | Conditionally required | The date for the time activity. This is the posting date that affects financial statements. If the date is not supplied, the current date on the server is used. Sort order is ASC by default. If you provide the StartTime and EndTime without including the timeZone offset, then you would need to pass the TxnDate for any historical or future dates. |
| **BreakHours / BreakMinutes** | Integer (max 8760 hours 59 minutes) | Conditionally required | Hours and minutes of break taken between StartTime and EndTime. Use when StartTime and EndTime are specified. |
| **EndTime** | DateTime | Conditionally required | Time that work ends. Required if Hours and Minutes not specified. Note: Kindly consider only the Hours without including the timeZone offset as it does not impact time activity hours calculation. |
| **Hours** | Integer (max 8760 hours 59 minutes) | Conditionally required | Hours and minutes worked. Required if StartTime and EndTime not specified. |
| **VendorRef** | ReferenceType | Conditionally required | Specifies the vendor whose time is being recorded. Query the Vendor name list resource to determine the appropriate Vendor object for this reference. Use Vendor.Id and Vendor.Name from that object for VendorRef.value and VendorRef.name, respectively. Required if NameOf is set to Vendor. |
| **ProjectRef** | ReferenceType, filterable | Conditionally required | Reference to the Project ID associated with this transaction. Available with Minor Version 69 and above. |
| **HourlyRate** | Decimal (0 to 99999999999) | Conditionally required | Hourly bill rate of the employee or vendor for this time activity. Required if BillableStatus is set to Billable. |
| **CustomerRef** | ReferenceType | Conditionally required | Reference to a customer or job. Query the Customer name list resource to determine the appropriate Customer object for this reference. Use Customer.Id and Customer.DisplayName from that object for CustomerRef.value and CustomerRef.name, respectively. Required if BillableStatus is set to Billable. |
| **EmployeeRef** | ReferenceType | Conditionally required | Specifies the employee whose time is being recorded. Query the Employee name list resource to determine the appropriate Employee object for this reference. Use Employee.Id and Employee.DisplayName from that object for EmployeeRef.value and EmployeeRef.Name, respectively. Required if NameOf is set to Employee. |
| **StartTime** | DateTime | Conditionally required | Time that work starts. Required if Hours and Minutes not specified. Note: Kindly consider only the Hours without including the timeZone offset as it does not impact time activity hours calculation. |
| **ClassRef** | ReferenceType | Optional | Reference to the Class associated with this object. Available if Preferences.AccountingInfoPrefs.ClassTrackingPerTxn is set to true. Query the Class name list resource to determine the appropriate Class object for this reference. Use Class.Id and Class.Name from that object for ClassRef.value and ClassRef.name, respectively. |
| **Description** | String (max 4000 chars) | Optional | Description of work completed during time activity. |
| **Taxable** | Boolean | Optional | True if the time recorded is both billable and taxable. |
| **TransactionLocationType** | String | Optional | The account location. Valid values include: WithinFrance, FranceOverseas, OutsideFranceWithEU, OutsideEU. For France locales, only. Minor version 4. |
| **MetaData** | ModificationMetaData | Optional | Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications. |
| **CostRate** | BigDecimal | Optional | Pay rate of the employee or vendor for this time activity. |
| **ItemRef** | ReferenceType | Optional | Reference to the service item associated with this object. Query the Item name list resource, where Item.Type is set to Service, to determine the appropriate Item object for this reference. Use Item.Id and Item.Name from that object for ItemRef.value and ItemRef.name, respectively. |
| **PayrollItemRef** | ReferenceType | Optional | Specifies how much the employee should be paid for doing the work specified by the Compensation Id. Query the EmployeeCompensation resource to determine the appropriate PayrollCompensation object for an employee. This field is available only for a closed group of developers. |
| **BillableStatus** | BillableStatusEnum, filterable | Optional | Billable status of the time recorded. This field is not updatable through an API request. The value automatically changes when an invoice is created. Valid values: Billable, NotBillable, HasBeenBilled. You cannot directly update the status to HasBeenBilled. To set the status to HasBeenBilled, create an Invoice object and attach this TimeActivity object as a linked transaction to that Invoice. Read only. |
| **DepartmentRef** | ReferenceType | Optional | A reference to a Department object specifying the location of this object. Available if Preferences.AccountingInfoPrefs.TrackDepartments is set to true. Query the Department name list resource to determine the appropriate department object for this reference. Use Department.Id and Department.Name from that object for DepartmentRef.value and DepartmentRef.name, respectively. |

### Sample Object

```json
{
  "TimeActivity": {
    "TxnDate": "2014-09-17",
    "domain": "QBO",
    "NameOf": "Employee",
    "Description": "Garden Lighting",
    "ItemRef": {
      "name": "Lighting",
      "value": "8"
    },
    "Minutes": 0,
    "ProjectRef": {
      "value": "39298045"
    },
    "Hours": 3,
    "BillableStatus": "HasBeenBilled",
    "sparse": false,
    "HourlyRate": 15,
    "Taxable": false,
    "EmployeeRef": {
      "name": "Emily Platt",
      "value": "55"
    },
    "SyncToken": "0",
    "CustomerRef": {
      "name": "Rondonuwu Fruit and Vegi",
      "value": "21"
    },
    "Id": "5",
    "MetaData": {
      "CreateTime": "2014-09-17T11:55:25-07:00",
      "LastUpdatedTime": "2014-09-18T13:45:12-07:00"
    }
  },
  "time": "2015-07-28T10:35:07.663-07:00"
}
```

## Create a TimeActivity

### Request

```
POST /v3/company/<realmID>/timeactivity
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Minimum Required Elements

- **NameOf**: Either "Vendor" or "Employee"
- **EmployeeRef** or **VendorRef**: Based on NameOf value
- **Hours** and **Minutes** OR **StartTime** and **EndTime**

### Request Body

```json
{
  "TxnDate": "2021-02-02",
  "EndTime": "17:00:00-08:00",
  "EmployeeRef": {
    "name": "Emily Platt",
    "value": "55"
  },
  "StartTime": "08:00:00-08:00",
  "NameOf": "Employee"
}
```

### Response

```json
{
  "TimeActivity": {
    "TxnDate": "2015-07-28",
    "domain": "QBO",
    "NameOf": "Employee",
    "sparse": false,
    "ItemRef": {
      "name": "Hours",
      "value": "2"
    },
    "ProjectRef": {
      "value": "39298034"
    },
    "BillableStatus": "NotBillable",
    "StartTime": "2015-07-28T09:00:00-07:00",
    "HourlyRate": 0,
    "Taxable": false,
    "EmployeeRef": {
      "name": "Emily Platt",
      "value": "55"
    },
    "EndTime": "2015-07-28T18:00:00-07:00",
    "CustomerRef": {
      "name": "Cool Cars",
      "value": "3"
    },
    "Id": "6",
    "SyncToken": "0",
    "MetaData": {
      "CreateTime": "2015-07-28T10:26:25-07:00",
      "LastUpdatedTime": "2015-07-28T10:26:25-07:00"
    }
  },
  "time": "2015-07-28T10:26:26.952-07:00"
}
```

## Read a TimeActivity

Retrieves the details of a TimeActivity object that has been previously created.

### Request

```
GET /v3/company/<realmID>/timeactivity/<timeactivityId>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

Returns the TimeActivity response body.

```json
{
  "TimeActivity": {
    "TxnDate": "2014-09-17",
    "domain": "QBO",
    "NameOf": "Employee",
    "Description": "Garden Lighting",
    "ItemRef": {
      "name": "Lighting",
      "value": "8"
    },
    "Minutes": 0,
    "ProjectRef": {
      "value": "39298045"
    },
    "Hours": 3,
    "BillableStatus": "HasBeenBilled",
    "sparse": false,
    "HourlyRate": 15,
    "Taxable": false,
    "EmployeeRef": {
      "name": "Emily Platt",
      "value": "55"
    },
    "SyncToken": "0",
    "CustomerRef": {
      "name": "Rondonuwu Fruit and Vegi",
      "value": "21"
    },
    "Id": "5",
    "MetaData": {
      "CreateTime": "2014-09-17T11:55:25-07:00",
      "LastUpdatedTime": "2014-09-18T13:45:12-07:00"
    }
  },
  "time": "2015-07-28T10:35:07.663-07:00"
}
```

## Query a TimeActivity

### Request

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content-Type: application/text
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Sample Query

```sql
select * from TimeActivity where TxnDate > '2014-09-14'
```

### Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "TimeActivity": [
      {
        "TxnDate": "2014-09-17",
        "domain": "QBO",
        "NameOf": "Employee",
        "Description": "Garden Lighting",
        "ItemRef": {
          "name": "Lighting",
          "value": "8"
        },
        "Minutes": 0,
        "ProjectRef": {
          "value": "39298045"
        },
        "Hours": 3,
        "BillableStatus": "HasBeenBilled",
        "sparse": false,
        "HourlyRate": 15,
        "Taxable": false,
        "EmployeeRef": {
          "name": "Emily Platt",
          "value": "55"
        },
        "SyncToken": "0",
        "CustomerRef": {
          "name": "Rondonuwu Fruit and Vegi",
          "value": "21"
        },
        "Id": "5",
        "MetaData": {
          "CreateTime": "2014-09-17T11:55:25-07:00",
          "LastUpdatedTime": "2014-09-18T13:45:12-07:00"
        }
      },
      {
        "TxnDate": "2014-09-17",
        "domain": "QBO",
        "NameOf": "Employee",
        "Description": "Tree and Shrub Trimming",
        "ItemRef": {
          "name": "Trimming",
          "value": "18"
        },
        "Minutes": 0,
        "ProjectRef": {
          "value": "39298045"
        },
        "Hours": 2,
        "BillableStatus": "HasBeenBilled",
        "sparse": false,
        "HourlyRate": 15,
        "Taxable": false,
        "EmployeeRef": {
          "name": "Emily Platt",
          "value": "55"
        },
        "SyncToken": "0",
        "CustomerRef": {
          "name": "Rondonuwu Fruit and Vegi",
          "value": "21"
        },
        "Id": "4",
        "MetaData": {
          "CreateTime": "2014-09-17T11:54:02-07:00",
          "LastUpdatedTime": "2014-09-18T13:45:12-07:00"
        }
      },
      {
        "TxnDate": "2014-09-16",
        "domain": "QBO",
        "NameOf": "Employee",
        "Description": "Custom Design",
        "ItemRef": {
          "name": "Design",
          "value": "4"
        },
        "Minutes": 0,
        "ProjectRef": {
          "value": "39298003"
        },
        "Hours": 5,
        "BillableStatus": "Billable",
        "sparse": false,
        "HourlyRate": 75,
        "Taxable": false,
        "EmployeeRef": {
          "name": "John Johnson",
          "value": "54"
        },
        "SyncToken": "0",
        "CustomerRef": {
          "name": "Amy's Bird Sanctuary",
          "value": "1"
        },
        "Id": "3",
        "MetaData": {
          "CreateTime": "2014-09-17T11:53:15-07:00",
          "LastUpdatedTime": "2014-09-17T11:53:15-07:00"
        }
      },
      {
        "TxnDate": "2014-09-17",
        "domain": "QBO",
        "NameOf": "Employee",
        "Description": "Gardening",
        "ItemRef": {
          "name": "Hours",
          "value": "2"
        },
        "Minutes": 0,
        "ProjectRef": {
          "value": "39298003"
        },
        "Hours": 4,
        "BillableStatus": "NotBillable",
        "sparse": false,
        "HourlyRate": 0,
        "Taxable": false,
        "EmployeeRef": {
          "name": "John Johnson",
          "value": "54"
        },
        "SyncToken": "0",
        "CustomerRef": {
          "name": "Amy's Bird Sanctuary",
          "value": "1"
        },
        "Id": "2",
        "MetaData": {
          "CreateTime": "2014-09-17T11:47:12-07:00",
          "LastUpdatedTime": "2014-09-17T11:47:12-07:00"
        }
      }
    ],
    "maxResults": 4
  },
  "time": "2015-07-28T10:01:35.141-07:00"
}
```

## Delete a TimeActivity

This operation deletes the TimeActivity object specified in the request body. Include a minimum of TimeActivity.Id and TimeActivity.SyncToken in the request body.

### Request

```
POST /v3/company/<realmID>/timeactivity?operation=delete
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "SyncToken": "0",
  "Id": "5"
}
```

### Response

```json
{
  "TimeActivity": {
    "status": "Deleted",
    "domain": "QBO",
    "Id": "5"
  },
  "time": "2015-05-27T10:37:58.279-07:00"
}
```

## Full Update a TimeActivity

Use this operation to update any of the writable fields of an existing TimeActivity object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL. The ID of the object to update is specified in the request body.

### Request

```
POST /v3/company/<realmID>/timeactivity
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "TxnDate": "2014-09-16",
  "domain": "QBO",
  "NameOf": "Employee",
  "Description": "Updated descirption",
  "ItemRef": {
    "name": "Design",
    "value": "4"
  },
  "Minutes": 0,
  "ProjectRef": {
    "value": "39298005"
  },
  "Hours": 5,
  "BillableStatus": "Billable",
  "sparse": false,
  "HourlyRate": 75,
  "Taxable": false,
  "EmployeeRef": {
    "name": "John Johnson",
    "value": "54"
  },
  "SyncToken": "0",
  "CustomerRef": {
    "name": "Amy's Bird Sanctuary",
    "value": "1"
  },
  "Id": "3",
  "MetaData": {
    "CreateTime": "2014-09-17T11:53:15-07:00",
    "LastUpdatedTime": "2014-09-17T11:53:15-07:00"
  }
}
```

### Response

```json
{
  "TimeActivity": {
    "TxnDate": "2014-09-16",
    "domain": "QBO",
    "NameOf": "Employee",
    "Description": "Updated descirption",
    "ItemRef": {
      "name": "Design",
      "value": "4"
    },
    "Minutes": 0,
    "ProjectRef": {
      "value": "39298005"
    },
    "Hours": 5,
    "BillableStatus": "Billable",
    "sparse": false,
    "HourlyRate": 75,
    "Taxable": false,
    "EmployeeRef": {
      "name": "John Johnson",
      "value": "54"
    },
    "SyncToken": "1",
    "CustomerRef": {
      "name": "Amy's Bird Sanctuary",
      "value": "1"
    },
    "Id": "3",
    "MetaData": {
      "CreateTime": "2014-09-17T11:53:15-07:00",
      "LastUpdatedTime": "2015-07-28T11:59:41-07:00"
    }
  },
  "time": "2015-07-28T11:59:41.178-07:00"
}
```
