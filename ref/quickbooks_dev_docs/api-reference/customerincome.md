# CustomerIncome

The information below provides a reference on how to access the Customer Income report from the QuickBooks Online Report Service.

## The Customer Income Report Object

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
    "ReportName": "CustomerIncome", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "DateMacro": "this calendar year-to-date", 
    "ReportBasis": "Accrual", 
    "StartPeriod": "2016-01-01", 
    "Currency": "USD", 
    "EndPeriod": "2016-03-10", 
    "Time": "2016-03-10T09:28:05-08:00"
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
            "value": "247.66"
          }, 
          {
            "value": "-96.31"
          }, 
          {
            "value": "151.35"
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
              "value": "247.66"
            }, 
            {
              "value": "-96.31"
            }, 
            {
              "value": "151.35"
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
        "ColTitle": "Income"
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "Expenses"
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "Net Income"
      }
    ]
  }
}
```

## Query a Report

### Request URL
`GET /v3/company/<realmID>/reports/CustomerIncome?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| customer | String | Filters report contents to include information for specified customers. (Optional) |
| term | String | Filters report contents based on term or terms supplied. (Optional) |
| accounting_method | String | The accounting method used in the report. Supported Values: Cash, Accrual (Optional) |
| end_date | String | The end date of the report, in the format YYYY-MM-DD. (Optional) |
| date_macro | String | Predefined date range. (Optional) |
| class | String | Filters report contents to include information for specified classes. (Optional) |
| sort_order | String | The sort order. (Optional) |
| summarize_column_by | String | The criteria by which to group the report results. (Optional) |
| department | String | Filters report contents to include information for specified departments. (Optional) |
| vendor | String | Filters report contents to include information for specified vendors. (Optional) |
| start_date | String | The start date of the report, in the format YYYY-MM-DD. (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/CustomerIncome?customer=1`

### Sample Response (JSON)
(Same as Sample Object above)
