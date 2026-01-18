# CustomerBalance

The information below provides a reference on how to access the Customer Balance report from the QuickBooks Online Report Service.

## The Customer Balance Report Object

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
    "Customer": "1", 
    "ReportName": "CustomerBalance", 
    "Option": [
      {
        "Name": "report_date", 
        "Value": "2016-03-10"
      }, 
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "DateMacro": "all", 
    "Currency": "USD", 
    "Time": "2016-03-10T08:51:44-08:00"
  }, 
  "Rows": {
    "Row": [
      {
        "ColData": [
          {
            "id": "1", 
            "value": "Amy's Bird Sanctuary"
          }, 
          {
            "value": "1593.50"
          }
        ]
      }, 
      {
        "group": "GrandTotal", 
        "type": "Section", 
        "Summary": {
          "ColData": [
            {
              "value": "TOTAL"
            }, 
            {
              "value": "1593.50"
            }
          ]
        }
      }
    ]
  }, 
  "Columns": {
    "Column": [
      {
        "ColType": "Customer", 
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
`GET /v3/company/<realmID>/reports/CustomerBalance?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| customer | String | Filters report contents to include information for specified customers. (Optional) |
| accounting_method | String | The accounting method used in the report. Supported Values: Cash, Accrual (Optional) |
| date_macro | String | Predefined date range. Supported Values: Today, Yesterday, This Week, etc. (Optional) |
| arpaid | String | Supported Values: All, Paid, Unpaid (Optional) |
| report_date | String | Start date to use for the report, in the format YYYY-MM-DD. (Optional) |
| sort_order | String | The sort order. (Optional) |
| summarize_column_by | String | The criteria by which to group the report results. (Optional) |
| department | String | Filters report contents to include information for specified departments. (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/CustomerBalance?customer=1`

### Sample Response (JSON)
(Same as Sample Object above)
