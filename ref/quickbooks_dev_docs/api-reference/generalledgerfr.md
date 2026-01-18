# GeneralLedgerFR

The information below provides a reference on how to access the General Ledger Detail report from the QuickBooks Report Service. For each specified account, the report shows all the transactions that occurred in that account over a period of time. It includes the beginning balance and total for each account. This endpoint is specialized for France-based companies.

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
    "ReportName": "GeneralLedgerFR", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "StartPeriod": "2021-10-19", 
    "Currency": "EUR", 
    "EndPeriod": "2021-10-19", 
    "Time": "2021-10-19T09:31:18-07:00"
  }, 
  "Rows": {
    "Row": [
      {
        "Header": {
          "ColData": [
            {
              "id": "82", 
              "value": "44566100 TVA déductible"
            }
          ]
        }, 
        "Rows": {
          "Row": [
            {
              "ColData": [
                {
                  "value": "2021-10-19"
                }, 
                ...
              ], 
              "type": "Data"
            }
          ]
        }, 
        "type": "Section", 
        "Summary": {
          "ColData": [
            {
              "value": "Total for 44566100 TVA déductible"
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
              "value": ""
            }, 
            {
              "value": "200.00"
            }, 
            {
              "value": ""
            }, 
            {
              "value": "200.00"
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
        "ColType": "tx_date", 
        "ColTitle": "Date"
      }, 
      {
        "ColType": "journal_code_name", 
        "ColTitle": "Journal Code"
      }, 
      {
        "ColType": "doc_num", 
        "ColTitle": "No."
      }, 
      {
        "ColType": "memo", 
        "ColTitle": "Memo/Description"
      }, 
      {
        "ColType": "lettrage", 
        "ColTitle": "Lettrage"
      }, 
      {
        "ColType": "debt_amt", 
        "ColTitle": "Debit"
      }, 
      {
        "ColType": "credit_amt", 
        "ColTitle": "Credit"
      }, 
      {
        "ColType": "subt_rbal_amount", 
        "ColTitle": "Balance"
      }
    ]
  }
}
```

## Query a Report

### Request URL
`GET /v3/company/<realmID>/reports/GeneralLedgerFR?<name>=<value>[&...]`

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

### Sample Query
`BaseURL/v3/company/1386066315/reports/GeneralLedgerFR?start_date=2021-01-01&end_date=2015-10-18&source_account_type=Bank`

### Sample Response (JSON)
(Same as Sample Object above)
