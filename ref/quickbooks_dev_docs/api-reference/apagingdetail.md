# APAgingDetail

The information below provides a reference on how to access the AP Aging Detail report from the QuickBooks Online Report Service.

## The AP Aging Detail Report Object

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
    "ReportName": "AgedPayableDetail", 
    "Currency": "USD", 
    "EndPeriod": "2015-06-30", 
    "Option": [
      {
        "Name": "report_date", 
        "Value": "2015-06-30"
      }, 
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "Time": "2016-03-08T14:34:28-08:00"
  }, 
  "Rows": {
    "Row": [
      {
        "Header": {
          "ColData": [
            {
              "value": "31 - 60 days past due"
            }
          ]
        }, 
        "Rows": {
          "Row": [
            {
              "ColData": [
                {
                  "id": "32", 
                  "value": "Cal Telephone"
                }, 
                {
                  "value": "2015-05-24"
                }
              ], 
              "type": "Data"
            }
          ]
        }, 
        "type": "Section"
      },
      ...
    ]
  }, 
  "Columns": {
    "Column": [
      {
        "ColType": "vend_name", 
        "ColTitle": "Vendor"
      }, 
      {
        "ColType": "due_date", 
        "ColTitle": "Due Date"
      }
    ]
  }
}
```

## Query a Report

### Request URL
`GET /v3/company/<realmID>/reports/AgedPayableDetail?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| shipvia | String | Filter by the shipping method. (Optional) |
| term | String | Filters report contents based on term or terms supplied. (Optional) |
| end_duedate | String | The range of dates over which receivables are due. (Optional) |
| accounting_method | String | The accounting method used in the report. (Optional) |
| start_duedate | String | The range of dates over which receivables are due. (Optional) |
| custom1, custom2, custom3 | String | Filter by specified custom fields. (Optional) |
| report_date | String | Start date to use for the report, in the format YYYY-MM-DD. (Optional) |
| num_periods | Integer | The number of periods to be shown in the report. (Optional) |
| vendor | String | Filters report contents to include information for specified vendors. (Optional) |
| past_due | Integer | Filters report contents based on minimum days past due. (Optional) |
| aging_period | Decimal | The number of days in the aging period. (Optional) |
| columns | String | Column types to be shown in the report. (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/AgedPayableDetail?report_date=2015-06-30&start_duedate=2015-01-01&end_duedate=2015-06-30&columns=due_date,vend_name`

### Sample Response (JSON)
(Same as Sample Object above)
