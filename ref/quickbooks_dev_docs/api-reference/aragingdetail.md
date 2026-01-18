# ARAgingDetail

The information below provides a reference on how to access the AR Aging Detail report from the QuickBooks Online Report Service.

## The AR Aging Detail Report Object

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
    "ReportName": "AgedReceivableDetail", 
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
    "Time": "2016-03-09T10:16:56-08:00"
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
                  "id": "8", 
                  "value": "Freeman Sporting Goods:0969 Ocean View Road"
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
        "ColType": "cust_name", 
        "ColTitle": "Client"
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
`GET /v3/company/<realmID>/reports/AgedReceivableDetail?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| customer | String | Filters report contents to include information for specified customers. (Optional) |
| shipvia | String | Filter by the shipping method. (Optional) |
| term | String | Filters report contents based on term or terms supplied. (Optional) |
| end_duedate | String | The range of dates over which receivables are due. (Optional) |
| start_duedate | String | The range of dates over which receivables are due. (Optional) |
| custom1, custom2, custom3 | String | Filter by specified custom fields. (Optional) |
| report_date | String | Start date to use for the report, in the format YYYY-MM-DD. (Optional) |
| num_periods | Integer | The number of periods to be shown in the report. (Optional) |
| aging_method | String | The date upon which aging is determined. Supported Values: Report_Date, Current (Optional) |
| past_due | Integer | Filters report contents based on minimum days past due. (Optional) |
| aging_period | Decimal | The number of days in the aging period. (Optional) |
| columns | String | Column types to be shown in the report. (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/AgedReceivableDetail?report_date=2015-06-30&start_duedate=2015-01-01&end_duedate=2015-06-30&columns=due_date,cust_name`

### Sample Response (JSON)
(Same as Sample Object above)
