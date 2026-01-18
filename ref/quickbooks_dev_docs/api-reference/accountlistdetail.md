# AccountListDetail

The information below provides a reference on how to access the account list detail report from the QuickBooks Online Report Service.

## The Account List Detail Report Object

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
    "ReportName": "AccountList", 
    "Currency": "USD", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "Time": "2016-03-08T11:56:36-08:00"
  }, 
  "Rows": {
    "Row": [
      {
        "ColData": [
          {
            "value": "Billable Expense Income"
          }, 
          {
            "value": "Income"
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
        "ColType": "account_name", 
        "ColTitle": "Account"
      }, 
      {
        "ColType": "account_type", 
        "ColTitle": "Type"
      }
    ]
  }
}
```

## Query a Report

### Request URL
`GET /v3/company/<realmID>/reports/AccountList?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| account_type | String | Account type from which transactions are included in the report. Supported Values: AccountsPayable, AccountsReceivable, Bank, CostOfGoodsSold, CreditCard, Equity, Expense, FixedAsset, Income, LongTermLiability, NonPosting, OtherAsset, OtherCurrentAsset, OtherCurrentLiability, OtherExpense, OtherIncome (Optional) |
| end_date | String | The start date and end date of the report, in the format YYYY-MM-DD. (Optional) |
| start_moddate | String | Specify an explicit account modification report date range, in the format YYYY-MM-DD. (Optional) |
| sort_by | String | The column type used in sorting report rows. (Optional) |
| sort_order | String | The sort order. Supported Values: ascend, descend (Optional) |
| moddate_macro | String | Predefined report account modification date range. Supported Values: Today, Yesterday, This Week, Last Week, etc. (Optional) |
| end_moddate | String | Specify an explicit account modification report date range, in the format YYYY-MM-DD. (Optional) |
| account_status | String | The account status. Supported values include: Deleted, Not_Deleted (Optional) |
| createdate_macro | String | Predefined report account create date range. (Optional) |
| start_date | String | The start date and end date of the report, in the format YYYY-MM-DD. (Optional) |
| columns | String | Column types to be shown in the report. Supported Values: account_name, account_type, detail_acc_type, create_date, create_by, last_mod_date, last_mod_by, account_desc, account_bal (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/AccountList?columns=account_name,account_type&account_type=Income`

### Sample Response (JSON)
(Same as Sample Object above)
