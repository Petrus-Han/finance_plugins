# ARAgingSummary

The information below provides a reference on how to access the AR Aging Summary report from the QuickBooks Online Report Service.

## The AR Aging Summary Report Object

### Attributes

| Name | Description |
| --- | --- |
| Header | The report header. |
| Rows | Top level container holding information for Aged Receivables report rows. |
| Columns | Top level container holding information for report columns or subcolumns. |

### Sample Object (JSON)

```json
{
  "Header": {
    "Customer": "4", 
    "ReportName": "AgedReceivables", 
    "Option": [
      {
        "Name": "report_date", 
        "Value": "2015-12-31"
      }, 
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "DateMacro": "last calendar year", 
    "StartPeriod": "2015-01-01", 
    "Currency": "USD", 
    "EndPeriod": "2015-12-31", 
    "Time": "2016-03-09T09:09:52-08:00"
  }, 
  "Rows": {
    "Row": [
      {
        "ColData": [
          {
            "id": "4", 
            "value": "Jane Litigious"
          }, 
          ...
          {
            "value": "37.50"
          }
        ]
      },
      ...
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
        "ColTitle": "Current"
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "1 - 30"
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "31 - 60"
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "61 - 90"
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "91 and over"
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
`GET /v3/company/<realmID>/reports/AgedReceivables?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| customer | String | Filters report contents to include information for specified customers. (Optional) |
| qzurl | String | Specifies whether Quick Zoom URL information should be generated. (Optional) |
| date_macro | String | Predefined date range. (Optional) |
| aging_method | String | The date upon which aging is determined. Supported Values: Report_Date, Current (Optional) |
| report_date | String | Start date to use for the report, in the format YYYY-MM-DD. (Optional) |
| sort_order | String | The sort order. (Optional) |
| department | String | Filters report contents to include information for specified departments. (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/AgedReceivables?customer=4&date_macro=Last Fiscal Year`

### Sample Response (JSON)
(Same as Sample Object above)
