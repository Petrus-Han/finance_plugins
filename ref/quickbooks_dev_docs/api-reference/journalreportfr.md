# JournalReportFR

The information below provides a reference on how to access the journal report from the QuickBooks Online Report Service for FR locales only. This report presents a summary of the journal code ledgers for the FR company. In an FR-locale company, there is a ledger for sales (VT), for purchases (HA), for each bank (BQx), for miscellaneous operations (OD), and so on. VT, HA, BQx, OD are called journal codes. Each transaction has a journal code and therefore its destination ledger.

## The Journal Report Object

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
    "ReportName": "JournalReportFR", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "DateMacro": "this month-to-date", 
    "StartPeriod": "2016-05-01", 
    "Currency": "EUR", 
    "EndPeriod": "2016-05-16", 
    "Time": "2016-05-16T09:25:46+01:00"
  }, 
  "Rows": {
    "Row": [
      {
        "Header": {
          "ColData": [
            {
              "value": "BQ1"
            }
          ]
        }, 
        "Rows": {
          "Row": [
            {
              "ColData": [
                {
                  "id": "", 
                  "value": ""
                }, 
                {
                  "value": "BQ1"
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
              "value": "Total pour BQ1"
            }, 
            {
              "value": ""
            }, 
            {
              "value": "191,50 €"
            }, 
            {
              "value": "191,50 €"
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
        "ColType": "txn_num", 
        "ColTitle": "Numéro d’opération"
      }, 
      {
        "ColType": "journal_code_name", 
        "ColTitle": "Code de journal"
      }, 
      {
        "ColType": "tx_date", 
        "ColTitle": "Date"
      }, 
      ...
    ]
  }
}
```

## Query a Report

### Request URL
`GET /v3/company/<realmID>/reports/JournalReportFR?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| journal_code | String | Filters report contents to include information for specified journal codes. Supported Values: One or more comma separated journal codes. (Optional) |
| end_date | String | The end date of the report, in the format YYYY-MM-DD. (Optional) |
| date_macro | String | Predefined date range. (Optional) |
| sort_by | String | The column type used in sorting report rows. (Optional) |
| sort_order | String | The sort order. Supported Values: ascend, descend (Optional) |
| start_date | String | The start date of the report, in the format YYYY-MM-DD. (Optional) |
| columns | String | Column types to be shown in the report. Supported Values: acct_num_with_extn, account_name, credit_amt, debt_amt, doc_num, due_date, is_ar_paid, is_ap_paid, item_name, journal_code_name, last_mod_by, last_mod_date, memo, name, neg_open_bal, paid_date, pmt_mthd, quantity, rate, tx_date, txn_num, txn_type. (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/JournalReportFR?journal_code=VT`

### Sample Response (JSON)
(Same as Sample Object above)
