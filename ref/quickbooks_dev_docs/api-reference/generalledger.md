# GeneralLedger

The information below provides a reference on how to access the General Ledger Detail report from the QuickBooks Report Service. For each specified account, the report shows all the transactions that occurred in that account over a period of time. It includes the beginning balance and total for each account. For France-based companies, use GeneralLedgerFR as the endpoint.

> **Note**: The QuickBooks Reports API response for the General Ledger report hierarchy is broken in certain circumstances when there are sub accounts configured in the QuickBooks Online company. Invoke the report endpoint with the `minorversion=3` query parameter to get a well-formed, correct response.

## The General Ledger Report Object

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
    "ReportName": "GeneralLedger", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "ReportBasis": "Accrual", 
    "StartPeriod": "2015-01-01", 
    "Currency": "USD", 
    "EndPeriod": "2015-06-30", 
    "Time": "2016-03-11T09:11:52-08:00"
  }, 
  "Rows": {
    "Row": [
      {
        "Header": {
          "ColData": [
            {
              "id": "82", 
              "value": "Design income"
            }
          ]
        }, 
        "Rows": {
          "Row": [
            {
              "ColData": [
                {
                  "id": "82", 
                  "value": "Design income"
                }, 
                {
                  "value": "225.0"
                }
              ], 
              "type": "Data"
            },
            ...
          ]
        }, 
        "type": "Section", 
        "Summary": {
          "ColData": [
            {
              "value": "Total for Design income"
            }, 
            {
              "value": "975.0"
            }
          ]
        }
      },
      ...
    ]
  }, 
  "Columns": {
    "Column": [
      {
        "ColType": "account_name", 
        "ColTitle": "Account"
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
`GET /v3/company/<realmID>/reports/GeneralLedger?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| customer | String | Filters report contents to include information for specified customers. (Optional) |
| account | String | Filters report contents to include information for specified accounts. (Optional) |
| accounting_method | String | The accounting method used in the report. Supported Values: Cash, Accrual (Optional) |
| source_account | String | Filters report contents to include information for specified source accounts. (Optional) |
| end_date | String | The end date of the report, in the format YYYY-MM-DD. (Optional) |
| date_macro | String | Predefined date range. (Optional) |
| account_type | String | (source_account_type) Account type from which transactions are included in the report. (Optional) |
| sort_by | String | The column type used in sorting report rows. (Optional) |
| sort_order | String | The sort order. (Optional) |
| start_date | String | The start date of the report, in the format YYYY-MM-DD. (Optional) |
| summarize_column_by | String | The criteria by which to group the report results. (Optional) |
| department | String | Filters report contents to include information for specified departments. (Optional) |
| vendor | String | Filters report contents to include information for specified vendors. (Optional) |
| class | String | Filters report contents to include information for specified classes. (Optional) |
| columns | String | Column types to be shown in the report. Supported Values: account_name, chk_print_state, create_by, create_date, cust_name, doc_num, emp_name, inv_date, is_adj, is_ap_paid, is_ar_paid, is_cleared, item_name, last_mod_by, last_mod_date, memo, name, quantity, rate, split_acc, tx_date, txn_type, vend_name. (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/GeneralLedger?start_date=2015-01-01&end_date=2015-06-30&columns=account_name,subt_nat_amount&source_account_type=Bank`

### Sample Response (JSON)
(Same as Sample Object above)
