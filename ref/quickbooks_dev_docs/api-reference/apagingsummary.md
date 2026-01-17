# APAgingSummary

The information below provides a reference on how to access the AP Aging summary report from the QuickBooks Online Report Service.

## The AP Aging Summary Report Object

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
    "ReportName": "AgedPayables", 
    "Option": [
      {
        "Name": "report_date", 
        "Value": "2016-03-08"
      }, 
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "DateMacro": "today", 
    "StartPeriod": "2016-03-08", 
    "Currency": "USD", 
    "EndPeriod": "2016-03-08", 
    "Time": "2016-03-08T16:11:49-08:00"
  }, 
  "Rows": {
    "Row": [
      {
        "ColData": [
          {
            "id": "56", 
            "value": "Bob's Burger Joint"
          }, 
          ...
          {
            "value": "-46.00"
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
`GET /v3/company/<realmID>/reports/AgedPayables?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| customer | String | Filters report contents to include information for specified customers. (Optional) |
| qzurl | String | Specifies whether Quick Zoom URL information should be generated. (Optional) |
| vendor | String | Filters report contents to include information for specified vendors. (Optional) |
| date_macro | String | Predefined date range. (Optional) |
| department | String | Filters report contents to include information for specified departments. (Optional) |
| report_date | String | Start date to use for the report, in the format YYYY-MM-DD. (Optional) |
| sort_order | String | The sort order. (Optional) |
| aging_method | String | The date upon which aging is determined. Supported Values: Report_Date, Current (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/AgedPayables?date_macro=Today`

### Sample Response (JSON)
(Same as Sample Object above)
