# VendorExpenses

The information below provides a reference on how to access the Expenses by Vendor report from the QuickBooks Online Report Service.

## The Expenses by Vendor Report Object

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
    "ReportName": "VendorExpenses", 
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
    "EndPeriod": "2016-03-14", 
    "Time": "2016-03-14T13:22:38-07:00", 
    "SummarizeColumnsBy": "Total"
  }, 
  "Rows": {
    "Row": [
      {
        "ColData": [
          {
            "id": "56", 
            "value": "Bob's Burger Joint"
          }, 
          {
            "value": "-61.91"
          }
        ]
      },
      ...
    ]
  }, 
  "Columns": {
    "Column": [
      {
        "ColType": "Vendor", 
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
`GET /v3/company/<realmID>/reports/VendorExpenses?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| customer | String | Filters report contents to include information for specified customers. (Optional) |
| vendor | String | Filters report contents to include information for specified vendors. (Optional) |
| end_date | String | The end date of the report, in the format YYYY-MM-DD. (Optional) |
| date_macro | String | Predefined date range. (Optional) |
| class | String | Filters report contents to include information for specified classes. (Optional) |
| sort_order | String | The sort order. (Optional) |
| summarize_column_by | String | The criteria by which to group the report results. (Optional) |
| department | String | Filters report contents to include information for specified departments. (Optional) |
| accounting_method | String | The accounting method used in the report. (Optional) |
| start_date | String | The start date of the report, in the format YYYY-MM-DD. (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/VendorExpenses`

### Sample Response (JSON)
(Same as Sample Object above)
