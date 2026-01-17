# TransactionList

The information below provides a reference on how to access the Transaction List report from the QuickBooks Online Report Service.

## The TransactionList Report Object

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
| ReportName | Name of the report (TransactionList) |
| Option | Array of options (e.g., NoReportData) |
| StartPeriod | Start date of report period |
| EndPeriod | End date of report period |
| Currency | Currency code (e.g., USD) |
| Time | Timestamp of report generation |

### Rows Attributes

| Attribute | Description |
|-----------|-------------|
| Row | Array of row data |
| Header | Section header with customer/vendor name |
| Rows | Nested rows for transaction details |
| ColData | Array of column data values for each row |
| id | Entity ID reference (transaction, customer, account) |
| value | Display value |
| type | Row type (e.g., "Section", "Data") |
| Summary | Summary row data for sections |

### Columns Attributes

| Attribute | Description |
|-----------|-------------|
| Column | Array of column definitions |
| ColType | Column type identifier |
| ColTitle | Column display title |

### Default Columns

| ColType | ColTitle | Description |
|---------|----------|-------------|
| tx_date | Date | Transaction date |
| txn_type | Transaction Type | Type of transaction (Invoice, Payment, etc.) |
| doc_num | Num | Document/reference number |
| is_no_post | Posting | Whether the transaction posts to financials |
| name | Name | Customer/Vendor name |
| dept_name | Department | Department (if location tracking enabled) |
| memo | Memo/Description | Transaction memo or description |
| account_name | Account | Primary account affected |
| other_account | Split | Split account (or "-Split-" for multiple) |
| subt_nat_home_amount | Amount | Transaction amount |

## Query a Report

### Request URL

```
GET /v3/company/<realmID>/reports/TransactionList?<name>=<value>[&...]
```

- **Accept type:** application/json
- **Production Base URL:** https://quickbooks.api.intuit.com
- **Sandbox Base URL:** https://sandbox-quickbooks.api.intuit.com

### Query Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| date_macro | Optional | String | Predefined date range. Supported Values: Today, Yesterday, This Week, Last Week, This Week-to-date, Last Week-to-date, Next Week, Next 4 Weeks, This Month, Last Month, This Month-to-date, Last Month-to-date, Next Month, This Fiscal Quarter, Last Fiscal Quarter, This Fiscal Quarter-to-date, Last Fiscal Quarter-to-date, Next Fiscal Quarter, This Fiscal Year, Last Fiscal Year, This Fiscal Year-to-date, Last Fiscal Year-to-date, Next Fiscal Year, This Calendar Quarter, This Calendar Quarter-to-date, Last Calendar Quarter, Last Calendar Quarter-to-date, Next Calendar Quarter, This Calendar Year, This Calendar Year-to-date, Last Calendar Year, Last Calendar Year-to-date, Next Calendar Year |
| start_date | Optional | String | Start date in YYYY-MM-DD format. Must be less than end_date |
| end_date | Optional | String | End date in YYYY-MM-DD format |
| payment_method | Optional | String | Filter by payment method. Supported Values: Cash, Check, Dinners Club, American Express, Discover, MasterCard, Visa, Credit Card |
| duedate_macro | Optional | String | Predefined due date range. Same values as date_macro |
| start_duedate | Optional | String | Start due date in YYYY-MM-DD format |
| end_duedate | Optional | String | End due date in YYYY-MM-DD format |
| arpaid | Optional | String | AR payment status. Supported Values: All, Paid, Unpaid |
| appaid | Optional | String | AP payment status. Supported Values: Paid, Unpaid, All |
| bothamount | Optional | String | Filter by specific transaction amount (e.g., bothamount=1233.45) |
| transaction_type | Optional | String | Filter by transaction type. Supported Values: CreditCardCharge, Check, Invoice, ReceivePayment, JournalEntry, Bill, CreditCardCredit, VendorCredit, Credit, BillPaymentCheck, BillPaymentCreditCard, Charge, Transfer, Deposit, Statement, BillableCharge, TimeActivity, CashPurchase, SalesReceipt, CreditMemo, CreditRefund, Estimate, InventoryQuantityAdjustment, PurchaseOrder, GlobalTaxPayment, GlobalTaxAdjustment, Service Tax Refund, Service Tax Gross Adjustment, Service Tax Reversal, Service Tax Defer, Service Tax Partial Utilisation |
| docnum | Optional | String | Filter by document number |
| start_moddate | Optional | String | Start modification date in YYYY-MM-DD format |
| end_moddate | Optional | String | End modification date in YYYY-MM-DD format |
| moddate_macro | Optional | String | Predefined modification date range. Same values as date_macro |
| start_createdate | Optional | String | Start create date in YYYY-MM-DD format |
| end_createdate | Optional | String | End create date in YYYY-MM-DD format |
| createdate_macro | Optional | String | Predefined create date range. Same values as date_macro |
| source_account_type | Optional | String | Filter by account type. Supported Values: AccountsPayable, AccountsReceivable, Bank, CostOfGoodsSold, CreditCard, Equity, Expense, FixedAsset, Income, LongTermLiability, NonPosting, OtherAsset, OtherCurrentAsset, OtherCurrentLiability, OtherExpense, OtherIncome |
| group_by | Optional | String | Group results by field. Supported Values: Name, Account, Transaction Type, Customer, Vendor, Employee, Location, Payment Method, Day, Week, Month, Quarter, Year, Fiscal Year, Fiscal Quarter, None |
| department | Optional | String | Filter by department IDs (comma separated) |
| customer | Optional | String | Filter by customer IDs (comma separated) |
| vendor | Optional | String | Filter by vendor IDs (comma separated) |
| name | Optional | String | Filter by name list IDs (customer, vendor, or employee) |
| memo | Optional | String | Filter by memo IDs (comma separated) |
| term | Optional | String | Filter by term IDs (comma separated) |
| printed | Optional | String | Filter by print status. Supported Values: Printed, To_be_printed |
| cleared | Optional | String | Filter by cleared status. Supported Values: Cleared, Uncleared, Reconciled, Deposited |
| columns | Optional | String | Specify columns to include. See Available Columns section |
| qzurl | Optional | String | Generate Quick Zoom URLs. Supported Values: true, false |
| sort_by | Optional | String | Column type to sort by |
| sort_order | Optional | String | Sort order. Supported Values: ascend, descend |

### Available Columns

**Standard columns:**
- account_name*, create_by, create_date, cust_msg, due_date, doc_num*
- inv_date, is_ap_paid, is_cleared, is_no_post*, last_mod_by, memo*
- name*, other_account*, pmt_mthd, printed, sales_cust1, sales_cust2
- sales_cust3, term_name, tracking_num, tx_date*, txn_type*, term_name
- is_adj, last_mod_date, ship_via, olb_status, extra_doc_num, is_ar_paid

**With location tracking enabled:**
- dept_name*

**With multicurrency enabled:**
- Additional currency-related columns

(* = default columns)

### Sample Query

```
GET https://quickbooks.api.intuit.com/v3/company/1386066315/reports/TransactionList?start_date=2016-06-01&end_date=2016-07-31&group_by=Customer
```

### Sample Response

```json
{
  "Header": {
    "ReportName": "TransactionList", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "StartPeriod": "2016-06-01", 
    "Currency": "USD", 
    "EndPeriod": "2016-07-31", 
    "Time": "2017-01-10T10:53:41-08:00"
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
                {"value": "2016-06-14"},
                {"id": "151", "value": "Invoice"},
                {"value": "1040"},
                {"value": "Yes"},
                {"id": "1", "value": "Amy's Bird Sanctuary"},
                {"id": "1", "value": "West Coast"},
                {"value": "This is a private note."},
                {"id": "84", "value": "Accounts Receivable (A/R)"},
                {"id": "", "value": "-Split-"},
                {"value": "47.60"}
              ], 
              "type": "Data"
            }
          ]
        }, 
        "type": "Section", 
        "Summary": {
          "ColData": [
            {"value": "Total for Amy's Bird Sanctuary"},
            {"value": "505.95"}
          ]
        }
      }
    ]
  }, 
  "Columns": {
    "Column": [
      {"ColType": "tx_date", "ColTitle": "Date"},
      {"ColType": "txn_type", "ColTitle": "Transaction Type"},
      {"ColType": "doc_num", "ColTitle": "Num"},
      {"ColType": "is_no_post", "ColTitle": "Posting"},
      {"ColType": "name", "ColTitle": "Name"},
      {"ColType": "dept_name", "ColTitle": "Department"},
      {"ColType": "memo", "ColTitle": "Memo/Description"},
      {"ColType": "account_name", "ColTitle": "Account"},
      {"ColType": "other_account", "ColTitle": "Split"},
      {"ColType": "subt_nat_home_amount", "ColTitle": "Amount"}
    ]
  }
}
```

## Transaction Types

The `transaction_type` filter supports the following values:

| Type | Description |
|------|-------------|
| Invoice | Customer invoice |
| ReceivePayment / Payment | Customer payment received |
| SalesReceipt | Direct sales with immediate payment |
| CreditMemo | Customer credit memo |
| CreditRefund | Refund to customer |
| Estimate | Quote/Estimate |
| Bill | Vendor bill |
| BillPaymentCheck | Bill payment by check |
| BillPaymentCreditCard | Bill payment by credit card |
| VendorCredit | Vendor credit |
| Check | Check payment |
| CreditCardCharge | Credit card purchase |
| CreditCardCredit | Credit card credit/return |
| CashPurchase | Cash purchase |
| Transfer | Bank transfer |
| Deposit | Bank deposit |
| JournalEntry | Manual journal entry |
| TimeActivity | Time tracking entry |
| InventoryQuantityAdjustment | Inventory adjustment |
| PurchaseOrder | Purchase order |
| Charge | Delayed charge |
| BillableCharge | Billable expense |

## Cleared Status Values

| Value | Description |
|-------|-------------|
| Cleared | Transaction processed by bank |
| Uncleared | Not yet reconciled with bank |
| Reconciled | Verified against bank statement |
| Deposited | Deposit made to bank account |
