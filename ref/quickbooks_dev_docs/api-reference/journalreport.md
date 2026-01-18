# JournalReport

The information below provides a reference on how to access the journal report from the QuickBooks Online Report Service. For FR locales use JournalReportFR instead. This report presents a summary of the journal code ledgers for non-FR companies.

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
    "ReportName": "JournalReport", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "DateMacro": "this month-to-date", 
    "StartPeriod": "2019-05-01", 
    "Currency": "USD", 
    "EndPeriod": "2019-05-22", 
    "Time": "2019-05-22T17:16:03-07:00"
  }, 
  "Rows": {
    "Row": [
      {
        "ColData": [
          {
            "value": "2019-05-07"
          }, 
          {
            "id": "63", 
            "value": "Expense"
          }, 
          ...
          {
            "value": "30.00"
          }
        ], 
        "type": "Data"
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
        "ColType": "txn_type", 
        "ColTitle": "Transaction Type"
      }, 
      {
        "ColType": "doc_num", 
        "ColTitle": "Num"
      }, 
      {
        "ColType": "name", 
        "ColTitle": "Name"
      }, 
      {
        "ColType": "memo", 
        "ColTitle": "Memo/Description"
      }, 
      {
        "ColType": "account_name", 
        "ColTitle": "Account"
      }, 
      {
        "ColType": "debt_amt", 
        "ColTitle": "Debit"
      }, 
      {
        "ColType": "credit_amt", 
        "ColTitle": "Credit"
      }
    ]
  }
}
```

## Query a Report

### Request URL
`GET /v3/company/<realmID>/reports/JournalReport?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| end_date | String | The end date of the report, in the format YYYY-MM-DD. (Optional) |
| date_macro | String | Predefined date range. Supported Values: Today, Yesterday, This Week, Last Week, etc. (Optional) |
| sort_by | String | The column type used in sorting report rows. (Optional) |
| sort_order | String | The sort order. Supported Values: ascend, descend (Optional) |
| start_date | String | The start date of the report, in the format YYYY-MM-DD. (Optional) |
| columns | String | Column types to be shown in the report. Supported Values: acct_num_with_extn, account_name, credit_amt, create_by, create_date, debt_amt, doc_num, due_date, is_ar_paid, is_ap_paid, item_name, journal_code_name, last_mod_by, last_mod_date, memo, name, neg_open_bal, paid_date, pmt_mthd, quantity, rate, tx_date, txn_num, txn_type. (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/JournalReport`

### Sample Response (JSON)
(Same as Sample Object above)

## Notes
- To retrieve the account number (`acct_num_with_extn`) it's also needed to request the account name (`account_name`) in the same request.
- The account number will only be returned if the company has enabled the 'enable account numbers' option in its Chart of Accounts.
