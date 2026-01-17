# Budget

The Budget endpoint allows you to retrieve the current state of budgets already set up in the user's company file. A budget allows for an amount to be assigned on a monthly, quarterly, or annual basis for a specific account or customer and are created to give a business measurable expense goals. This amount represents how much should be spent against that account or customer in the give time period.

## The Budget Object

### Attributes

| Name | Type | Description |
| --- | --- | --- |
| Id | String | Unique identifier for this object. Sort order is ASC by default. (Required for update, read only, system defined, filterable, sortable) |
| EndDate | DateTime | Budget end date. (Required) |
| StartDate | DateTime | Budget begin date. (Required) |
| SyncToken | String | Version number of the object. It is used to lock an object for use by one app at a time. (Required for update, read only, system defined) |
| BudgetEntryType | BudgetEntryTypeEnum | Period that this budget detail covers. Valid values include: Monthly, Quarterly, Annually. (Optional, read only) |
| Name | String | User recognizable name for the Account. (Optional, read only, filterable, sortable) |
| BudgetDetail [0..n] | BudgetDetail | Container for the budget items. (Optional) |
| BudgetType | BudgetTypeEnum | Budget types. The only value currently supported is ProfitAndLoss. (Optional, read only, filterable, sortable) |
| Active | Boolean | Whether or not active inactive accounts may be hidden from most display purposes and may not be posted to. (Optional, filterable) |
| MetaData | ModificationMetaData | Descriptive information about the object. (Optional) |

### Sample Object (JSON)

```json
{
  "QueryResponse": {
    "startPosition": 1, 
    "totalCount": 1, 
    "Budget": [
      {
        "StartDate": "2014-01-01", 
        "BudgetEntryType": "Monthly", 
        "EndDate": "2014-12-31", 
        "Name": "Sandbox Budget", 
        "SyncToken": "1", 
        "BudgetType": "ProfitAndLoss", 
        "domain": "QBO", 
        "sparse": false, 
        "Active": true, 
        "BudgetDetail": [
          {
            "Amount": 0, 
            "AccountRef": {
              "name": "Services", 
              "value": "1"
            }, 
            "BudgetDate": "2014-01-01"
          }, 
          {
            "Amount": 0, 
            "AccountRef": {
              "name": "Services", 
              "value": "1"
            }, 
            "BudgetDate": "2014-02-01"
          }, 
          {
            "Amount": 71.0, 
            "AccountRef": {
              "name": "Unapplied Cash Payment Income", 
              "value": "87"
            }, 
            "BudgetDate": "2014-12-01"
          }
        ], 
        "Id": "1", 
        "MetaData": {
          "CreateTime": "2015-07-14T13:59:45-07:00", 
          "LastUpdatedTime": "2015-07-14T13:59:59-07:00"
        }
      }
    ], 
    "maxResults": 1
  }, 
  "time": "2015-07-14T14:14:07.394-07:00"
}
```

## Create a budget

### Request Body

| Name | Type | Description |
| --- | --- | --- |
| EndDate | DateTime | Budget end date. (Required) |
| StartDate | DateTime | Budget begin date. (Required) |
| BudgetDetail [0..n] | BudgetDetail | Container for the budget items. (Optional) |
| BudgetEntryType | BudgetEntryTypeEnum | Period that this budget detail covers. Valid values include: Monthly, Quarterly, Annually. (Optional, read only) |
| Name | String | User recognizable name for the Account. (Optional, read only, filterable, sortable) |
| BudgetType | BudgetTypeEnum | Budget types. The only value currently supported is ProfitAndLoss. (Optional, read only, filterable, sortable) |

### Request URL
`POST /v3/company/<realmID>/budget`

### Sample Request
```json
{
  "StartDate": "2024-01-01", 
  "BudgetEntryType": "Quarterly", 
  "EndDate": "2024-12-31", 
  "Name": "MyBudget", 
  "BudgetType": "ProfitAndLoss", 
  "BudgetDetail": [
    {
      "Amount": 12.0, 
      "CustomerRef": {
        "value": "2"
      }, 
      "AccountRef": {
        "value": "5"
      }, 
      "BudgetDate": "2024-01-01"
    }
  ]
}
```

### Sample Response
```json
{
  "Budget": {
    "StartDate": "2024-01-01", 
    "BudgetEntryType": "Quarterly", 
    "EndDate": "2024-12-31", 
    "Name": "MyBudget", 
    "SyncToken": "0", 
    "BudgetType": "ProfitAndLoss", 
    "domain": "QBO", 
    "sparse": false, 
    "Active": true, 
    "BudgetDetail": [
      {
        "Amount": 12.0, 
        "AccountRef": {
          "name": "Fees Billed", 
          "value": "5"
        }, 
        "CustomerRef": {
          "name": "Seabiscuit", 
          "value": "2"
        }, 
        "BudgetDate": "2024-01-01"
      },
      ...
    ], 
    "Id": "2", 
    "MetaData": {
      "CreateTime": "2024-01-09T14:16:19-08:00", 
      "LastUpdatedTime": "2024-01-09T14:19:04-08:00"
    }
  }, 
  "time": "2024-06-19T13:54:58.396-07:00"
}
```

## Delete a budget

### Request Body

| Name | Type | Description |
| --- | --- | --- |
| SyncToken | String | Version number of the object. (Required, read only, system defined) |
| id | String | Unique identifier for this object. (Required, read only, system defined, filterable, sortable) |

### Request URL
`POST /v3/company/<realmID>/budget?operation=delete`

### Sample Request
```json
{
  "SyncToken": "4", 
  "Id": "1"
}
```

### Sample Response
```json
{
  "time": "2021-08-05T15:17:32.161-07:00"
}
```

## Query a budget

### Request URL
`GET /v3/company/<realmID>/query?query=<selectStatement>`

### Sample Query
`Select * from Budget`

### Sample Response
```json
{
  "QueryResponse": {
    "startPosition": 1, 
    "totalCount": 1, 
    "Budget": [
      {
        "StartDate": "2014-01-01", 
        "BudgetEntryType": "Monthly", 
        "EndDate": "2014-12-31", 
        "Name": "Sandbox Budget", 
        "SyncToken": "1", 
        "BudgetType": "ProfitAndLoss", 
        "domain": "QBO", 
        "sparse": false, 
        "Active": true, 
        "BudgetDetail": [
          {
            "Amount": 0, 
            "AccountRef": {
              "name": "Services", 
              "value": "1"
            }, 
            "BudgetDate": "2014-01-01"
          },
          ...
        ], 
        "Id": "1", 
        "MetaData": {
          "CreateTime": "2015-07-14T13:59:45-07:00", 
          "LastUpdatedTime": "2015-07-14T13:59:59-07:00"
        }
      }
    ], 
    "maxResults": 1
  }, 
  "time": "2015-07-14T14:14:07.394-07:00"
}
```

## Read a budget

### Request URL
`GET /v3/company/<realmID>/budget/<budgetId>`

### Sample Response
```json
{
  "Budget": {
    "StartDate": "2014-01-01", 
    "BudgetEntryType": "Quarterly", 
    "EndDate": "2014-12-31", 
    "Name": "MyBudget", 
    "SyncToken": "9", 
    "BudgetType": "ProfitAndLoss", 
    "domain": "QBO", 
    "sparse": false, 
    "Active": true, 
    "BudgetDetail": [
      {
        "Amount": 12.0, 
        "AccountRef": {
          "name": "Fees Billed", 
          "value": "5"
        }, 
        "BudgetDate": "2014-01-01"
      },
      ...
    ], 
    "Id": "2", 
    "MetaData": {
      "CreateTime": "2014-01-09T14:16:19-08:00", 
      "LastUpdatedTime": "2014-01-09T14:19:04-08:00"
    }
  }, 
  "time": "2014-06-19T13:54:58.396-07:00"
}
```

## Full update a budget

### Request Body
The request body must include all writable fields of the existing object. Writable fields omitted are set to NULL.

### Request URL
`POST /v3/company/<realmID>/budget`

### Sample Request
```json
{
  "SyncToken": "3", 
  "BudgetEntryType": "Monthly", 
  "EndDate": "2015-12-31", 
  "Name": "New", 
  "StartDate": "2015-01-01", 
  "BudgetType": "ProfitAndLoss", 
  "Active": "true", 
  "BudgetDetail": [
    {
      "Amount": "7.00", 
      "AccountRef": {
        "type": "String", 
        "name": "Fees Billed", 
        "value": "5"
      }, 
      "CustomerRef": {
        "type": "String", 
        "name": "Fazil", 
        "value": "3"
      }, 
      "BudgetDate": "2015-01-01"
    },
    ...
  ], 
  "Id": "21"
}
```
