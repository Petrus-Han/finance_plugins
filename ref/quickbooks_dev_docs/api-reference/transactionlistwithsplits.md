# TransactionListWithSplits

The information below provides a reference on how to access the Transaction List With Splits report from the QuickBooks Online Report Service.

## The TransactionListWithSplits Report Object

The table below lists all possible attributes that can be returned in the report response. Values are not localized unless indicated.

### Attributes

| Attribute | Description |
|-----------|-------------|
| Header | The report header |
| Rows | Top level container holding information for report rows |
| Columns | Top level container holding information for report columns or subcolumns |

### Header Attributes

| Attribute | Description |
|-----------|-------------|
| ReportName | Name of the report (TransactionListWithSplits) |
| Option | Array of options (e.g., NoReportData) |
| StartPeriod | Start date of report period |
| EndPeriod | End date of report period |
| Currency | Currency code (e.g., USD) |
| Time | Timestamp of report generation |

### Default Columns

| ColTitle | ColKey | ColType | Description |
|----------|--------|---------|-------------|
| Date | tx_date | Date | Transaction date |
| Transaction Type | txn_type | String | Type of transaction |
| Num | doc_num | String | Document/reference number |
| Posting | is_no_post | Boolean | Whether the transaction posts |
| Name | name | String | Customer/Vendor name |
| Memo/Description | memo | String | Transaction memo |
| Account | account_name | String | Account name |
| Amount | nat_amount | Money | Transaction amount |

### Sample Object

```json
{
  "Header": {
    "ReportName": "TransactionListWithSplits", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "StartPeriod": "2020-12-01", 
    "Currency": "USD", 
    "EndPeriod": "2021-01-28", 
    "Time": "2021-02-03T22:46:48-08:00"
  }, 
  "Rows": {
    "Row": [
      {
        "Header": {
          "ColData": [
            {"id": "33", "value": "Accounts Payable (A/P)"},
            {"value": ""},
            {"value": ""},
            {"value": ""},
            {"value": ""},
            {"value": ""},
            {"value": ""},
            {"value": ""}
          ]
        }, 
        "Rows": {
          "Row": [
            {
              "ColData": [
                {"value": "2020-12-11"},
                {"id": "257", "value": "Bill"},
                {"value": ""},
                {"value": "Yes"},
                {"id": "56", "value": "Bob's Burger Joint"},
                {"value": ""},
                {"id": "33", "value": "Accounts Payable (A/P)"},
                {"value": "200.00"}
              ], 
              "type": "Data"
            }
          ]
        }, 
        "type": "Section"
      }
    ]
  }, 
  "Columns": {
    "Column": [
      {
        "ColType": "Date", 
        "ColTitle": "Date", 
        "MetaData": [{"Name": "ColKey", "Value": "tx_date"}]
      }, 
      {
        "ColType": "String", 
        "ColTitle": "Transaction Type", 
        "MetaData": [{"Name": "ColKey", "Value": "txn_type"}]
      }, 
      {
        "ColType": "String", 
        "ColTitle": "Num", 
        "MetaData": [{"Name": "ColKey", "Value": "doc_num"}]
      }, 
      {
        "ColType": "Boolean", 
        "ColTitle": "Posting", 
        "MetaData": [{"Name": "ColKey", "Value": "is_no_post"}]
      }, 
      {
        "ColType": "String", 
        "ColTitle": "Name", 
        "MetaData": [{"Name": "ColKey", "Value": "name"}]
      }, 
      {
        "ColType": "String", 
        "ColTitle": "Memo/Description", 
        "MetaData": [{"Name": "ColKey", "Value": "memo"}]
      }, 
      {
        "ColType": "String", 
        "ColTitle": "Account", 
        "MetaData": [{"Name": "ColKey", "Value": "account_name"}]
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "Amount", 
        "MetaData": [{"Name": "ColKey", "Value": "nat_amount"}]
      }
    ]
  }
}
```

## Query a Report

### Request URL

```
GET /v3/company/<realmID>/reports/TransactionListWithSplits?<name>=<value>[&...]
```

- **Accept type:** application/json
- **Production Base URL:** https://quickbooks.api.intuit.com
- **Sandbox Base URL:** https://sandbox-quickbooks.api.intuit.com

### Query Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| date_macro | Optional | String | Predefined date range. Supported Values: Today, Yesterday, This Week, Last Week, This Week-to-date, Last Week-to-date, Next Week, Next 4 Weeks, This Month, Last Month, This Month-to-date, Last Month-to-date, Next Month, This Fiscal Quarter, Last Fiscal Quarter, This Fiscal Quarter-to-date, Last Fiscal Quarter-to-date, Next Fiscal Quarter, This Fiscal Year, Last Fiscal Year, This Fiscal Year-to-date, Last Fiscal Year-to-date, Next Fiscal Year |
| start_date | Optional | String | Start date in YYYY-MM-DD format |
| end_date | Optional | String | End date in YYYY-MM-DD format |
| payment_method | Optional | String | Filter by payment method. Supported Values: Cash, Check, Dinners Club, American Express, Discover, MasterCard, Visa |
| docnum | Optional | String | Filter by document number |
| name | Optional | String | Filter by name list IDs (customer, vendor, or employee) |
| source_account_type | Optional | String | Filter by account type. Supported Values: AccountsPayable, AccountsReceivable, Bank, CostOfGoodsSold, CreditCard, Equity, Expense, FixedAsset, Income, LongTermLiability, NonPosting, OtherAsset, OtherCurrentAsset, OtherCurrentLiability, OtherExpense, OtherIncome |
| transaction_type | Optional | String | Filter by transaction type. Supported Values: CreditCardCharge, Check, Invoice, ReceivePayment, JournalEntry, Bill, CreditCardCredit, VendorCredit, Credit, BillPaymentCheck, BillPaymentCreditCard, Charge, Transfer, Deposit, Statement, BillableCharge, TimeActivity, CashPurchase, SalesReceipt, CreditMemo, CreditRefund, Estimate, InventoryQuantityAdjustment, PurchaseOrder, GlobalTaxPayment, GlobalTaxAdjustment, Service Tax Refund, Service Tax Gross Adjustment, Service Tax Reversal, Service Tax Defer, Service Tax Partial Utilisation |
| group_by | Optional | String | Group results by field. Supported Values: Name, Account, Transaction Type |
| sort_by | Optional | String | Column type to sort by. Supported Values: account_name, is_adj, create_by, create_date, tx_date, last_mod_date, last_mod_by, name, doc_num, pmt_mthd, is_no_post, txn_type |
| sort_order | Optional | String | Sort order. Supported Values: ascend, descend |
| columns | Optional | String | Specify columns to include |

### Available Columns

**Standard columns:**
- tx_date, txn_type, doc_num, is_no_post, account_name, memo
- amount, is_adj, create_by, create_date, last_mod_date, last_mod_by
- cust_name, vend_name, rate, quantity, item_name, emp_name
- pmt_mthd, nat_open_bal, tax_type, is_billable, debt_amt, credit_amt
- is_cleared, olb_status

**With location tracking enabled:**
- dept_name*

### Sample Query

```
GET https://quickbooks.api.intuit.com/v3/company/1386066315/reports/TransactionListWithSplits?start_date=2020-12-01&end_date=2021-01-28&group_by=Account
```

### Sample Response

```json
{
  "Header": {
    "ReportName": "TransactionListWithSplits", 
    "Option": [{"Name": "NoReportData", "Value": "false"}], 
    "StartPeriod": "2020-12-01", 
    "Currency": "USD", 
    "EndPeriod": "2021-01-28", 
    "Time": "2021-02-03T22:46:48-08:00"
  }, 
  "Rows": {
    "Row": [
      {
        "Header": {
          "ColData": [{"id": "33", "value": "Accounts Payable (A/P)"}]
        }, 
        "Rows": {
          "Row": [
            {
              "ColData": [
                {"value": "2020-12-11"},
                {"id": "257", "value": "Bill"},
                {"value": ""},
                {"value": "Yes"},
                {"id": "56", "value": "Bob's Burger Joint"},
                {"value": ""},
                {"id": "33", "value": "Accounts Payable (A/P)"},
                {"value": "200.00"}
              ], 
              "type": "Data"
            }
          ]
        }, 
        "type": "Section"
      }
    ]
  }, 
  "Columns": {
    "Column": [
      {"ColType": "Date", "ColTitle": "Date"},
      {"ColType": "String", "ColTitle": "Transaction Type"},
      {"ColType": "String", "ColTitle": "Num"},
      {"ColType": "Boolean", "ColTitle": "Posting"},
      {"ColType": "String", "ColTitle": "Name"},
      {"ColType": "String", "ColTitle": "Memo/Description"},
      {"ColType": "String", "ColTitle": "Account"},
      {"ColType": "Money", "ColTitle": "Amount"}
    ]
  }
}
```

## Notes

- **Key difference from TransactionList**: Shows split transactions with each line item as a separate row
- Useful for detailed double-entry bookkeeping analysis
- Each transaction is broken out into its component debit/credit entries
- Group by Account to see all transactions affecting each account
- Includes additional columns for detailed analysis: debt_amt, credit_amt, is_cleared
