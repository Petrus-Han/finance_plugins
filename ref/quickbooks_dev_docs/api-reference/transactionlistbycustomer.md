# TransactionListByCustomer

The information below provides a reference on how to access the Transaction List By Customer report from the QuickBooks Online Report Service.

## The TransactionListByCustomer Report Object

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
| ReportName | Name of the report (TransactionListByCustomer) |
| Option | Array of options (e.g., NoReportData) |
| StartPeriod | Start date of report period |
| EndPeriod | End date of report period |
| Currency | Currency code (e.g., USD) |
| Time | Timestamp of report generation |

### Default Columns

| ColTitle | ColKey | Description |
|----------|--------|-------------|
| Date | tx_date | Transaction date |
| Transaction Type | txn_type | Type of transaction |
| Num | doc_num | Document/reference number |
| Posting | is_no_post | Whether the transaction posts |
| Memo/Description | memo | Transaction memo |
| Account | account_name | Account name |
| Amount | amount | Transaction amount |

### Sample Object

```json
{
  "Header": {
    "ReportName": "TransactionListByCustomer", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "true"
      }
    ], 
    "StartPeriod": "2016-06-01", 
    "Currency": "USD", 
    "EndPeriod": "2016-07-31", 
    "Time": "2020-09-29T14:20:06-07:00"
  }, 
  "Rows": {}, 
  "Columns": {
    "Column": [
      {
        "ColTitle": "Date", 
        "MetaData": [{"Name": "ColKey", "Value": "tx_date"}]
      }, 
      {
        "ColTitle": "Transaction Type", 
        "MetaData": [{"Name": "ColKey", "Value": "txn_type"}]
      }, 
      {
        "ColTitle": "Num", 
        "MetaData": [{"Name": "ColKey", "Value": "doc_num"}]
      }, 
      {
        "ColTitle": "Posting", 
        "MetaData": [{"Name": "ColKey", "Value": "is_no_post"}]
      }, 
      {
        "ColTitle": "Memo/Description", 
        "MetaData": [{"Name": "ColKey", "Value": "memo"}]
      }, 
      {
        "ColTitle": "Account", 
        "MetaData": [{"Name": "ColKey", "Value": "account_name"}]
      }, 
      {
        "ColTitle": "Amount ", 
        "MetaData": [{"Name": "ColKey", "Value": "amount"}]
      }
    ]
  }
}
```

## Query a Report

### Request URL

```
GET /v3/company/<realmID>/reports/TransactionListByCustomer?<name>=<value>[&...]
```

- **Accept type:** application/json
- **Production Base URL:** https://quickbooks.api.intuit.com
- **Sandbox Base URL:** https://sandbox-quickbooks.api.intuit.com

### Query Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| date_macro | Optional | String | Predefined date range. Supported Values: Today, Yesterday, This Week, Last Week, This Week-to-date, Last Week-to-date, Next Week, Next 4 Weeks, This Month, Last Month, This Month-to-date, Last Month-to-date, Next Month, This Fiscal Quarter, Last Fiscal Quarter, This Fiscal Quarter-to-date, Last Fiscal Quarter-to-date, Next Fiscal Quarter, This Fiscal Year, Last Fiscal Year, This Fiscal Year-to-date, Last Fiscal Year-to-date, Next Fiscal Year, This Calendar Quarter, This Calendar Quarter-to-date, Last Calendar Quarter, Last Calendar Quarter-to-date, Next Calendar Quarter, This Calendar Year, This Calendar Year-to-date, Last Calendar Year, Last Calendar Year-to-date, Next Calendar Year |
| start_date | Optional | String | Start date in YYYY-MM-DD format |
| end_date | Optional | String | End date in YYYY-MM-DD format |
| payment_method | Optional | String | Filter by payment method. Supported Values: Cash, Check, Dinners Club, American Express, Discover, MasterCard, Visa, Credit Card |
| duedate_macro | Optional | String | Predefined due date range |
| start_duedate | Optional | String | Start due date in YYYY-MM-DD format |
| end_duedate | Optional | String | End due date in YYYY-MM-DD format |
| arpaid | Optional | String | AR payment status. Supported Values: All, Paid, Unpaid |
| appaid | Optional | String | AP payment status. Supported Values: Paid, Unpaid, All |
| bothamount | Optional | String | Filter by specific transaction amount |
| transaction_type | Optional | String | Filter by transaction type. Supported Values: CreditCardCharge, Check, Invoice, ReceivePayment, JournalEntry, Bill, CreditCardCredit, VendorCredit, Credit, BillPaymentCheck, BillPaymentCreditCard, Charge, Transfer, Deposit, Statement, BillableCharge, TimeActivity, CashPurchase, SalesReceipt, CreditMemo, CreditRefund, Estimate, InventoryQuantityAdjustment, PurchaseOrder, GlobalTaxPayment, GlobalTaxAdjustment, Service Tax Refund, Service Tax Gross Adjustment, Service Tax Reversal, Service Tax Defer, Service Tax Partial Utilisation |
| docnum | Optional | String | Filter by document number |
| start_moddate | Optional | String | Start modification date in YYYY-MM-DD format |
| end_moddate | Optional | String | End modification date in YYYY-MM-DD format |
| moddate_macro | Optional | String | Predefined modification date range |
| start_createdate | Optional | String | Start create date in YYYY-MM-DD format |
| end_createdate | Optional | String | End create date in YYYY-MM-DD format |
| createdate_macro | Optional | String | Predefined create date range |
| source_account_type | Optional | String | Filter by account type. Supported Values: AccountsPayable, AccountsReceivable, Bank, CostOfGoodsSold, CreditCard, Equity, Expense, FixedAsset, Income, LongTermLiability, NonPosting, OtherAsset, OtherCurrentAsset, OtherCurrentLiability, OtherExpense, OtherIncome |
| group_by | Optional | String | Group results by field. Supported Values: Name, Account, Transaction Type, Customer, Vendor, Employee, Location, Payment Method, Day, Week, Month, Quarter, Year, Fiscal Year, Fiscal Quarter, None |
| department | Optional | String | Filter by department IDs (comma separated) |
| customer | Optional | String | Filter by customer IDs (comma separated) |
| name | Optional | String | Filter by name list IDs (customer, vendor, or employee) |
| memo | Optional | String | Filter by memo IDs (comma separated) |
| term | Optional | String | Filter by term IDs (comma separated) |
| printed | Optional | String | Filter by print status. Supported Values: Printed, To_be_printed |
| cleared | Optional | String | Filter by cleared status. Supported Values: Cleared, Uncleared, Reconciled, Deposited |
| columns | Optional | String | Specify columns to include |
| qzurl | Optional | String | Generate Quick Zoom URLs. Supported Values: true, false |
| sort_by | Optional | String | Column type to sort by |
| sort_order | Optional | String | Sort order. Supported Values: ascend, descend |

### Available Columns

**Standard columns:**
- account_name*, create_by, create_date, cust_msg, due_date, doc_num*
- inv_date, is_ap_paid, is_cleared, is_no_post*, last_mod_by, memo*
- name*, other_account*, pmt_mthd, printed, sales_cust1, sales_cust2
- sales_cust3, term_name, tracking_num, tx_date*, txn_type*, term_name
- last_mod_date, ship_via, olb_status, is_ar_paid, extra_doc_num, cust_name

**With location tracking enabled:**
- dept_name*

(* = default columns)

### Sample Query

```
GET https://quickbooks.api.intuit.com/v3/company/1386066315/reports/TransactionListByCustomer?start_date=2016-06-01&end_date=2016-07-31&group_by=Customer
```

### Sample Response

```json
{
  "Header": {
    "ReportName": "TransactionListByCustomer", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "true"
      }
    ], 
    "StartPeriod": "2016-06-01", 
    "Currency": "USD", 
    "EndPeriod": "2016-07-31", 
    "Time": "2020-09-29T14:20:06-07:00"
  }, 
  "Rows": {}, 
  "Columns": {
    "Column": [
      {"ColTitle": "Date", "MetaData": [{"Name": "ColKey", "Value": "tx_date"}]},
      {"ColTitle": "Transaction Type", "MetaData": [{"Name": "ColKey", "Value": "txn_type"}]},
      {"ColTitle": "Num", "MetaData": [{"Name": "ColKey", "Value": "doc_num"}]},
      {"ColTitle": "Posting", "MetaData": [{"Name": "ColKey", "Value": "is_no_post"}]},
      {"ColTitle": "Memo/Description", "MetaData": [{"Name": "ColKey", "Value": "memo"}]},
      {"ColTitle": "Account", "MetaData": [{"Name": "ColKey", "Value": "account_name"}]},
      {"ColTitle": "Amount ", "MetaData": [{"Name": "ColKey", "Value": "amount"}]}
    ]
  }
}
```

## Notes

- This report is customer-focused, showing all transactions related to customers
- Useful for accounts receivable analysis and customer payment tracking
- Can be grouped by customer to see all transactions per customer
- Supports filtering by AR paid status (Paid, Unpaid, All)
- Includes customer-specific columns like cust_name and is_ar_paid
