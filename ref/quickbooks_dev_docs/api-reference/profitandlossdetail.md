# ProfitAndLossDetail

The information below provides a reference on how to access the Profit and Loss Detail report from the QuickBooks Online Report Service.

## The Profit and Loss Detail Report Object

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
    "Customer": "3", 
    "ReportName": "ProfitAndLossDetail", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "ReportBasis": "Accrual", 
    "StartPeriod": "2015-06-01", 
    "Currency": "USD", 
    "EndPeriod": "2015-06-30", 
    "Time": "2016-03-11T14:53:39-08:00"
  }, 
  "Rows": {
    "Row": [
      {
        "Header": {
          "ColData": [
            {
              "value": "Ordinary Income/Expenses"
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }
          ]
        }, 
        "Rows": {
          "Row": [
            {
              "Header": {
                "ColData": [
                  {
                    "value": "Income"
                  }, 
                  {
                    "value": ""
                  }, 
                  {
                    "value": ""
                  }
                ]
              },
              ...
            }
          ]
        }
      }
    ]
  }, 
  "Columns": {
    "Column": [
      {
        "ColType": "tx_date", 
        "ColTitle": "Date"
      }, 
      {
        "ColType": "name", 
        "ColTitle": "Name"
      }, 
      {
        "ColType": "subt_nat_amount", 
        "ColTitle": "Amount"
      }
    ]
  }
}
```

## Query a Report

### Request URL
`GET /v3/company/<realmID>/reports/ProfitAndLossDetail?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| customer | String | Filters report contents to include information for specified customers. (Optional) |
| account | String | Filters report contents to include information for specified accounts. (Optional) |
| accounting_method | String | The accounting method used in the report. Supported Values: Cash, Accrual (Optional) |
| end_date | String | The end date of the report, in the format YYYY-MM-DD. (Optional) |
| date_macro | String | Predefined date range. (Optional) |
| adjusted_gain_loss | String | Specifies whether unrealized gain and losses are included in the report. (Optional) |
| class | String | Filters report contents to include information for specified classes. (Optional) |
| sort_by | String | The column type used in sorting report rows. (Optional) |
| payment_method | String | Filters report contents based on payment method. (Optional) |
| sort_order | String | The sort order. (Optional) |
| employee | String | Filters report contents to include information for specified employees. (Optional) |
| department | String | Filters report contents to include information for specified departments. (Optional) |
| vendor | String | Filters report contents to include information for specified vendors. (Optional) |
| account_type | String | Account type from which transactions are included in the report. (Optional) |
| start_date | String | The start date of the report, in the format YYYY-MM-DD. (Optional) |
| columns | String | Column types to be shown in the report. (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/ProfitAndLossDetail?start_date=2015-06-01&end_date=2015-06-30&customer=3&columns=tx_date%2Cname%2Csubt_nat_amount`

### Sample Response (JSON)
(Same as Sample Object above)
