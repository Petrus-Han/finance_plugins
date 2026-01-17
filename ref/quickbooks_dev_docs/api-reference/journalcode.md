# JournalCode

Applicable only for France-locale companies (FR locale). Journal Code is a compliance requirement for a France-locale company. A journal code is assigned to each transaction and it depends on whether it is an income or an expense. To access this entity, invoke the endpoints with the minorversion=3 query parameter.

## The JournalCode Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | IdType, filterable, sortable | Required for update, read only, system defined | Unique Identifier for an Intuit entity (object). Required for the update operation. |
| **Name** | String | Required | A name representing the journal code. 2 to 20 characters in length. |
| **SyncToken** | String | Required for update, read only, system defined | Version number of the entity. Required for the update operation. |
| **Description** | String | Optional | A free-form description of the journal code. |
| **CustomField** | CustomField | Optional | One of, up to three custom fields for the transaction. Available for custom fields so configured for the company. Check Preferences.SalesFormsPrefs.CustomField and Preferences.VendorAndPurchasesPrefs.POCustomField for custom fields currently configured. |
| **Type** | String | Optional | The type of this journal code. The value cannot be changed once the object is created. Valid types include: Expenses, Sales, Bank, Nouveaux, Wages, Cash, Others |
| **MetaData** | ModificationMetaData, filterable, sortable | Optional | Descriptive information about the entity. The MetaData values are set by Data Services and are read only for all applications. |

### Sample Object

```json
{
  "JournalCode": {
    "SyncToken": "0",
    "domain": "QBO",
    "Name": "VT",
    "sparse": false,
    "time": "2015-12-16T11:01:37.346-07:00",
    "Active": true,
    "MetaData": {
      "CreateTime": "2015-10-30T11:06:19-07:00",
      "LastUpdatedTime": "2015-10-30T11:06:19-07:00"
    },
    "Type": "Sales",
    "Id": "2",
    "Description": "Sales"
  }
}
```

## Create a JournalCode

### Request Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Name** | String | Required | A name representing the journal code. 2 to 20 characters in length. |

### Returns

Returns the newly created journalcode object.

### Request URL

```
POST /v3/company/<realmID>/journalcode
Content type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "Type": "Sales",
  "Name": "VT"
}
```

### Response

```json
{
  "JournalCode": {
    "SyncToken": "0",
    "domain": "QBO",
    "Name": "VT",
    "sparse": false,
    "time": "2015-12-16T11:01:37.346-07:00",
    "Active": true,
    "MetaData": {
      "CreateTime": "2015-10-30T11:06:19-07:00",
      "LastUpdatedTime": "2015-10-30T11:06:19-07:00"
    },
    "Type": "Sales",
    "Id": "2",
    "Description": "Sales"
  }
}
```

## Query a JournalCode

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
select * from journalcode
```

### Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "JournalCode": [
      {
        "SyncToken": "5",
        "domain": "QBO",
        "Name": "ABCDEFGHIJKLMNO",
        "sparse": false,
        "Active": true,
        "MetaData": {
          "CreateTime": "2015-10-30T11:06:20-07:00",
          "LastUpdatedTime": "2015-10-30T13:55:24-07:00"
        },
        "Type": "Report A Nouveaux",
        "Id": "3",
        "Description": "Report A Nouveaux"
      },
      {
        "SyncToken": "0",
        "domain": "QBO",
        "Name": "CA",
        "sparse": false,
        "Active": true,
        "MetaData": {
          "CreateTime": "2015-10-30T11:06:20-07:00",
          "LastUpdatedTime": "2015-10-30T11:06:20-07:00"
        },
        "Type": "Cash",
        "Id": "5",
        "Description": "Cash"
      },
      {
        "SyncToken": "0",
        "domain": "QBO",
        "Name": "HA",
        "sparse": false,
        "Active": true,
        "MetaData": {
          "CreateTime": "2015-10-30T11:06:19-07:00",
          "LastUpdatedTime": "2015-10-30T11:06:19-07:00"
        },
        "Type": "Expenses",
        "Id": "1",
        "Description": "Expenses"
      },
      {
        "SyncToken": "1",
        "domain": "QBO",
        "Name": "NO",
        "sparse": false,
        "Active": true,
        "MetaData": {
          "CreateTime": "2015-10-30T11:06:20-07:00",
          "LastUpdatedTime": "2015-10-30T14:26:40-07:00"
        },
        "Type": "Report A Nouveaux",
        "Id": "4",
        "Description": "Report A Nouveaux"
      },
      {
        "SyncToken": "0",
        "domain": "QBO",
        "Name": "OD",
        "sparse": false,
        "Active": true,
        "MetaData": {
          "CreateTime": "2015-10-30T11:06:20-07:00",
          "LastUpdatedTime": "2015-10-30T11:06:20-07:00"
        },
        "Type": "Others",
        "Id": "6",
        "Description": "Others"
      },
      {
        "SyncToken": "0",
        "domain": "QBO",
        "Name": "VT",
        "sparse": false,
        "Active": true,
        "MetaData": {
          "CreateTime": "2015-10-30T11:06:19-07:00",
          "LastUpdatedTime": "2015-10-30T11:06:19-07:00"
        },
        "Type": "Sales",
        "Id": "2",
        "Description": "Sales"
      }
    ],
    "maxResults": 6,
    "totalCount": 6
  },
  "time": "2015-12-16T09:16:15.597-08:00"
}
```

## Read a JournalCode

Retrieves the details of a journalcode object that has been previously created.

### Returns

Returns the journalcode object.

### Request URL

```
GET /v3/company/<realmID>/journalcode/<journalcodeId>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "JournalCode": {
    "SyncToken": "0",
    "domain": "QBO",
    "Name": "VT",
    "sparse": false,
    "time": "2015-12-16T11:01:37.346-07:00",
    "Active": true,
    "MetaData": {
      "CreateTime": "2015-10-30T11:06:19-07:00",
      "LastUpdatedTime": "2015-10-30T11:06:19-07:00"
    },
    "Type": "Sales",
    "Id": "2",
    "Description": "Sales"
  }
}
```

## Update a JournalCode

Use this operation to update an active journalcode object or to deactivate a currently active one, as provided in the request.

### Request Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | IdType, filterable, sortable | Required for update, read only, system defined | Unique Identifier for an Intuit entity (object). |
| **Name** | String | Required | A name representing the journal code. 2 to 20 characters in length. |
| **SyncToken** | String | Required for update, read only, system defined | Version number of the entity. |
| **Description** | String | Optional | A free-form description of the journal code. |
| **CustomField** | CustomField | Optional | One of, up to three custom fields for the transaction. |
| **Type** | String | Optional | The type of this journal code. The value cannot be changed once the object is created. Valid types include: Expenses, Sales, Bank, Nouveaux, Wages, Cash, Others |
| **MetaData** | ModificationMetaData, filterable, sortable | Optional | Descriptive information about the entity. |

### Returns

The journalcode response body.

### Request URL

```
POST /v3/company/<realmID>/journalcode
Content type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "SyncToken": "0",
  "domain": "QBO",
  "Name": "VT",
  "sparse": false,
  "Active": true,
  "MetaData": {
    "CreateTime": "2015-10-30T11:06:19-07:00",
    "LastUpdatedTime": "2015-10-30T11:06:19-07:00"
  },
  "Type": "Sales",
  "Id": "2",
  "Description": "An updated description"
}
```

### Response

```json
{
  "JournalCode": {
    "SyncToken": "1",
    "domain": "QBO",
    "Name": "VT",
    "sparse": false,
    "time": "2015-12-16T11:06:19-07:00",
    "Active": true,
    "MetaData": {
      "CreateTime": "2015-12-16T11:06:19-07:00",
      "LastUpdatedTime": "2015-12-16T11:06:19-07:00"
    },
    "Type": "Sales",
    "Id": "2",
    "Description": "An updated description"
  }
}
```
