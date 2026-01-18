# CashFlow

The information below provides a reference on how to access the cash flow report from the QuickBooks Online Report Service.

## The Cash Flow Report Object

### Attributes

| Name | Description |
| --- | --- |
| Header | The report header. |
| Rows | Top level container holding information for report rows. |
| Columns | Top level container holding information for report columns or subcolumns. |

### Sample Object (JSON)

```json
{
  "Header": {
    "ReportName": "CashFlow", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "DateMacro": "last calendar year-to-date", 
    "StartPeriod": "2015-01-01", 
    "Currency": "USD", 
    "EndPeriod": "2015-03-09", 
    "Time": "2016-03-09T11:40:50-08:00", 
    "SummarizeColumnsBy": "Total"
  }, 
  "Rows": {
    "Row": [
      {
        "Header": {
          "ColData": [
            {
              "value": "OPERATING ACTIVITIES"
            }, 
            {
              "value": ""
            }
          ]
        }, 
        "Rows": {
          "Row": [
            {
              "ColData": [
                {
                  "value": "Net Income"
                }, 
                {
                  "value": "-300.00"
                }
              ], 
              "type": "Data", 
              "group": "NetIncome"
            },
            ...
          ]
        }
      }
    ]
  }, 
  "Columns": {
    "Column": [
      {
        "ColType": "Account", 
        "ColTitle": ""
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "Total"
      }
    ]
  }
}
```

## Query a Report

### Request URL
`GET /v3/company/<realmID>/reports/CashFlow?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| customer | String | Filters report contents to include information for specified customers. (Optional) |
| vendor | String | Filters report contents to include information for specified vendors. (Optional) |
| end_date | String | The end date of the report, in the format YYYY-MM-DD. (Optional) |
| date_macro | String | Predefined date range. Supported Values: Today, Yesterday, This Week, etc. (Optional) |
| class | String | Filters report contents to include information for specified classes. (Optional) |
| item | String | Filters report contents to include information for specified items. (Optional) |
| sort_order | String | The sort order. (Optional) |
| summarize_column_by | String | The criteria by which to group the report results. Supported Values: Total, Month, Week, Days, Quarter, Year, Customers, Vendors, Classes, Departments, Employees, ProductsAndServices (Optional) |
| department | String | Filters report contents to include information for specified departments. (Optional) |
| start_date | String | The start date of the report, in the format YYYY-MM-DD. (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/CashFlow`

### Sample Response (JSON)
(Same as Sample Object above)
