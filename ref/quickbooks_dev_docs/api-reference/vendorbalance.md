# VendorBalance

The information below provides a reference on how to access the Vendor Balance report from the QuickBooks Online Report Service.

## The Vendor Balance Report Object

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
    "ReportName": "VendorBalance", 
    "DateMacro": "all", 
    "Option": [
      {
        "Name": "report_date", 
        "Value": "2016-03-14"
      }, 
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "Currency": "USD", 
    "Time": "2016-03-14T10:39:07-07:00"
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
        "ColTitle": "Total"
      }
    ]
  }
}
```

## Query a Report

### Request URL
`GET /v3/company/<realmID>/reports/VendorBalance?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| qzurl | String | Specifies whether Quick Zoom URL information should be generated for rows in the report. (Optional) |
| accounting_method | String | The accounting method used in the report. Supported Values: Cash, Accrual (Optional) |
| date_macro | String | Predefined date range. (Optional) |
| appaid | String | Status of the balance. Supported Values: Paid, Unpaid, All (Optional) |
| report_date | String | Start date to use for the report, in the format YYYY-MM-DD. (Optional) |
| sort_order | String | The sort order. (Optional) |
| summarize_column_by | String | The criteria by which to group the report results. (Optional) |
| department | String | Filters report contents to include information for specified departments. (Optional) |
| vendor | String | Filters report contents to include information for specified vendors. (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/VendorBalance`

### Sample Response (JSON)
(Same as Sample Object above)
