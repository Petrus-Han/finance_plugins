# TaxSummary

Applicable for non-US locale companies only. The information below provides a reference on how to access the Tax Summary report from the QuickBooks Online Report Service.

## The Tax Summary Report Object

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
    "ReportName": "TaxSummary", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "StartPeriod": "2015-04-26", 
    "Currency": "EUR", 
    "EndPeriod": "2015-04-26", 
    "Time": "2015-04-26T22:23:51-07:00", 
    "SummarizeColumnsBy": "Total"
  }, 
  "Rows": {
    "Row": [
      {
        "ColData": [
          {
            "value": "Case 01 Vente, prestations de services"
          }, 
          {
            "value": ""
          }
        ], 
        "group": "Case 01"
      },
      ...
    ]
  }, 
  "Columns": {
    "Column": [
      {
        "ColType": "String", 
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
`GET /v3/company/<realmID>/reports/TaxSummary?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| agency_id | String | The ID of the Tax Agency for which to generate the report. (Required) |
| accounting_method | String | The accounting method used in the report. Supported Values: Cash, Accrual (Optional) |
| end_date | String | The end date of the report, in the format YYYY-MM-DD. (Optional) |
| date_macro | String | Predefined date range. Supported Values: Today, Yesterday, This Week, etc. (Optional) |
| sort_order | String | The sort order. Supported Values: ascend, descend (Optional) |
| start_date | String | The start date of the report, in the format YYYY-MM-DD. (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/TaxSummary?agency_id=1&start_date=2015-04-26&end_date=2015-04-26`

### Sample Response (JSON)
(Same as Sample Object above)
