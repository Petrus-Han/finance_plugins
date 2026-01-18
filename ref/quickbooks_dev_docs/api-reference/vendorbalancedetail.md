# VendorBalanceDetail

The information below provides a reference on how to access the Vendor Balance Detail report from the QuickBooks Online Report Service.

## The Vendor Balance Detail Report Object

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
    "ReportName": "VendorBalanceDetail", 
    "Vendor": "31", 
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
    "Time": "2016-03-14T11:18:40-07:00"
  }, 
  "Rows": {
    "Row": [
      {
        "Header": {
          "ColData": [
            {
              "id": "31", 
              "value": "Brosnahan Insurance Agency"
            }
          ]
        }, 
        "Rows": {
          "Row": [
            {
              "ColData": [
                {
                  "value": "2015-07-02"
                }, 
                {
                  "value": "241.23"
                }, 
                {
                  "value": "241.23"
                }
              ], 
              "type": "Data"
            }
          ]
        }, 
        "type": "Section", 
        "Summary": {
          "ColData": [
            {
              "value": "Total for Brosnahan Insurance Agency"
            }, 
            {
              "value": "241.23"
            }, 
            {
              "value": "241.23"
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
        "ColType": "subt_neg_amount", 
        "ColTitle": "Amount"
      }, 
      {
        "ColType": "subt_neg_open_bal", 
        "ColTitle": "Open Balance"
      }
    ]
  }
}
```

## Query a Report

### Request URL
`GET /v3/company/<realmID>/reports/VendorBalanceDetail?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| term | String | Filters report contents based on term or terms supplied. (Optional) |
| end_duedate | String | The range of dates over which receivables are due, in the format YYYY-MM-DD. (Optional) |
| accounting_method | String | The accounting method used in the report. Supported Values: Cash, Accrual (Optional) |
| date_macro | String | Predefined date range. (Optional) |
| start_duedate | String | The range of dates over which receivables are due, in the format YYYY-MM-DD. (Optional) |
| duedate_macro | String | Predefined date range of due dates. (Optional) |
| sort_by | String | The column type used in sorting report rows. (Optional) |
| report_date | String | Start date to use for the report, in the format YYYY-MM-DD. (Optional) |
| sort_order | String | The sort order. (Optional) |
| appaid | String | Status of the balance. Supported Values: Paid, Unpaid, All (Optional) |
| department | String | Filters report contents to include information for specified departments. (Optional) |
| vendor | String | Filters report contents to include information for specified vendors. (Optional) |
| columns | String | Column types to be shown in the report. (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/VendorBalanceDetail?vendor=31&columns=tx_date,subt_neg_amount,subt_neg_open_bal&date_macro=Last Fiscal Year`

### Sample Response (JSON)
(Same as Sample Object above)
