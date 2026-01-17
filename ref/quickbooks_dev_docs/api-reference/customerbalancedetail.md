# CustomerBalanceDetail

The information below provides a reference on how to access the Customer Balance Detail report from the QuickBooks Online Report Service.

## The Customer Balance Detail Report Object

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
    "ReportName": "CustomerBalanceDetail", 
    "Option": [
      {
        "Name": "report_date", 
        "Value": "2016-03-11"
      }, 
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "DateMacro": "all", 
    "Currency": "USD", 
    "Time": "2016-03-11T13:41:43-08:00"
  }, 
  "Rows": {
    "Row": [
      {
        "Header": {
          "ColData": [
            {
              "id": "1", 
              "value": "Amy's Bird Sanctuary"
            }
          ]
        }, 
        "Rows": {
          "Row": [
            {
              "ColData": [
                {
                  "value": "2015-05-22"
                }, 
                {
                  "value": "Invoice"
                }, 
                {
                  "value": "1001"
                }, 
                {
                  "value": "2015-06-21"
                }, 
                {
                  "value": "1593.50"
                }, 
                {
                  "value": "1593.50"
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
              "value": "Total for Amy's Bird Sanctuary"
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }, 
            {
              "value": "1593.50"
            }, 
            {
              "value": "1593.50"
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
        "ColType": "txn_type", 
        "ColTitle": "Transaction Type"
      }, 
      {
        "ColType": "doc_num", 
        "ColTitle": "No."
      }, 
      {
        "ColType": "due_date", 
        "ColTitle": "Due Date"
      }, 
      {
        "ColType": "subt_nat_amount", 
        "ColTitle": "Amount"
      }, 
      {
        "ColType": "rbal_nat_amount", 
        "ColTitle": "Balance"
      }
    ]
  }
}
```

## Query a Report

### Request URL
`GET /v3/company/<realmID>/reports/CustomerBalanceDetail?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| customer | String | Filters report contents to include information for specified customers. (Optional) |
| accounting_method | String | The accounting method used in the report. Supported Values: Cash, Accrual (Optional) |
| date_macro | String | Predefined date range. (Optional) |
| arpaid | String | Supported Values: All, Paid, Unpaid (Optional) |
| report_date | String | Start date to use for the report, in the format YYYY-MM-DD. (Optional) |
| sort_order | String | The sort order. (Optional) |
| summarize_column_by | String | The criteria by which to group the report results. (Optional) |
| department | String | Filters report contents to include information for specified departments. (Optional) |
| columns | String | Column types to be shown in the report. (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/CustomerBalanceDetail?customer=1`

### Sample Response (JSON)
(Same as Sample Object above)
