# Run Reports

> Source: https://developer.intuit.com/app/developer/qbo/docs/workflows/run-reports

The QuickBooks Online API includes a Reports API that is used to query financial reports. This topic provides an overview of the report response by showcasing the profit and loss report.

A **profit and loss report** (also known as the Income Statement) summarizes income and expenses for the company. The report shows subtotals for each income and expense account in the chart of accounts. The report is divided into sub-sections corresponding to the various income and expense groups, and within the groups a row corresponding to each account having data. Accounts with no data are excluded from the report.

> **Best Practice**: Limit the date range specified in a report request to six months.

## Prerequisites

To follow along, you'll need a sandbox or another QuickBooks company populated with:
- A chart of accounts
- Customers
- Items

---

## Summary of Available Reports

### Business Overview

| QuickBooks Report Name | Reports API Endpoint | Java | .NET | PHP |
|------------------------|---------------------|------|------|-----|
| Balance Sheet | `BalanceSheet` | ✓ | ✓ | ✓ |
| Profit and Loss | `ProfitAndLoss` | ✓ | ✓ | ✓ |
| Profit and Loss Detail | `ProfitAndLossDetail` | | ✓ | |
| Trial Balance | `TrialBalance` | ✓ | ✓ | ✓ |
| Statement of Cash Flows | `CashFlow` | ✓ | ✓ | ✓ |
| Inventory Valuation Summary | `InventoryValuationSummary` | ✓ | ✓ | ✓ |
| Inventory Valuation Detail | `InventoryValuationDetail` | ✓ | ✓ | ✓ |

### Review Sales

| QuickBooks Report Name | Reports API Endpoint | Java | .NET | PHP |
|------------------------|---------------------|------|------|-----|
| Sales by Customer Summary | `CustomerSales` | ✓ | ✓ | ✓ |
| Sales by Product/Service Summary | `ItemSales` | ✓ | ✓ | ✓ |
| Sales by Department Summary | `DepartmentSales` | ✓ | ✓ | ✓ |
| Sales by Class Summary | `ClassSales` | ✓ | ✓ | ✓ |
| Income by Customer Summary | `CustomerIncome` | ✓ | ✓ | ✓ |

### Manage Accounts Receivable

| QuickBooks Report Name | Reports API Endpoint | Java | .NET | PHP |
|------------------------|---------------------|------|------|-----|
| Customer Balance Summary | `CustomerBalance` | ✓ | ✓ | ✓ |
| Customer Balance Detail | `CustomerBalanceDetail` | | ✓ | |
| A/R Aging Summary | `AgedReceivables` | ✓ | ✓ | ✓ |
| A/R Aging Detail | `AgedReceivableDetail` | | ✓ | |

### Manage Accounts Payable

| QuickBooks Report Name | Reports API Endpoint | Java | .NET | PHP |
|------------------------|---------------------|------|------|-----|
| Vendor Balance Summary | `VendorBalance` | ✓ | ✓ | ✓ |
| Vendor Balance Detail | `VendorBalanceDetail` | ✓ | ✓ | ✓ |
| A/P Aging Summary | `AgedPayables` | ✓ | ✓ | ✓ |
| A/P Aging Detail | `AgedPayableDetail` | ✓ | ✓ | ✓ |

### Review Expenses and Purchases

| QuickBooks Report Name | Reports API Endpoint | Java | .NET | PHP |
|------------------------|---------------------|------|------|-----|
| Expenses by Vendor | `VendorExpenses` | ✓ | ✓ | ✓ |

### Accountant Reports

| QuickBooks Report Name | Reports API Endpoint | Java | .NET | PHP |
|------------------------|---------------------|------|------|-----|
| Account List | `AccountListDetail` | | ✓ | |
| General Ledger | `GeneralLedgerDetail` | | ✓ | ✓ |
| Tax Summary (France only) | `TaxSummary` | | | |

---

## Overview of the Report Response

The structure of each sub-section echoes that in the chart of accounts. The nesting structure of the chart of accounts is preserved in the report, which can create several nested levels of data. The data returned is subject to filter query parameters submitted with the request.

### Report Response Sections

A report response consists of three sections:

1. **Header** — Overview metadata for the report
2. **Columns** — Column metadata describing each column in the report
3. **Rows** — The report data, with two types:
   - **Section** — Defines a sub-report (can include nested sub-reports, data rows, or both)
   - **Data** — Defines report data (includes only columns)

---

## Transaction Compliance Dates

Reports list **transaction compliance dates** rather than actual transaction dates.

| Non-payment Transaction Date | Due Date | Payment Transaction Date | Compliance Date |
|------------------------------|----------|--------------------------|-----------------|
| February 6, 2017 | February 6, 2017 | February 1, 2017 (prepaid) | February 6, 2017 |
| February 1, 2017 | February 1, 2017 | February 6, 2017 | February 6, 2017 |

For a transaction where the payment date is before the transaction date, the compliance date is the original transaction date. This correctly accounts for the revenue and any tax liabilities within the intended financial period.

---

## Sample Report Requests

### Report with No Data

```http
GET https://quickbooks.api.intuit.com/v3/company/<realmId>/reports/ProfitAndLoss
```

Returns a single column with the default Profit and Loss groups when there is no data for the date range.

### Report with Customer Filtering

```http
GET https://quickbooks.api.intuit.com/v3/company/<realmId>/reports/ProfitAndLoss?start_date=2015-01-01&end_date=2015-07-31&customer=1&summarize_column_by=Customers
```

This requests a P&L report for a specific customer with columns organized by customer.

---

## Report Object Structure

### Header Attributes

| Attribute | Data Type | Description |
|-----------|-----------|-------------|
| `Time` | DateTime | Date and timestamp of the report |
| `ReportName` | String | Name of the report |
| `ReportBasis` | Enum | Accounting method: `Cash` or `Accrual` |
| `StartPeriod` | String | Start date (yyyy-mm-dd) from the `start_date` query parameter |
| `EndPeriod` | String | End date (yyyy-mm-dd) from the `end_date` query parameter |
| `SummarizeColumnsBy` | Enum | Method by which report columns are organized |
| `Currency` | String | Currency code associated with the report |
| `Customer` | String | Customer Ids specified in the filter |
| `Vendor` | String | Vendor Ids specified in the filter |
| `Employee` | String | Employee Ids specified in the filter |
| `Item` | String | Item Ids specified in the filter |
| `Class` | String | Class Ids specified in the filter |
| `Department` | String | Department Ids specified in the filter |

### Option Name/Value Pairs

| Name | Description |
|------|-------------|
| `AccountingStandard` | Indicates the accounting standard (returned with ProfitAndLoss and BalanceSheet) |
| `NoReportData` | `true` if report contains no data, `false` if it contains data |

### Column Attributes

| Attribute | Data Type | Description |
|-----------|-----------|-------------|
| `ColTitle` | String | The column label (localized) |
| `ColType` | Enum | `Account` — represents an account; `Money` — represents an amount |

### Row Attributes

| Attribute | Description |
|-----------|-------------|
| `type` | `Section` for enclosing rows, `Data` for leaf rows |
| `group` | Group name (valid when type=Section): `Income`, `COGS`, `GrossProfit`, `Expenses`, `NetOperatingIncome`, `OtherIncome`, `OtherExpenses`, `NetOtherIncome`, `NetIncome` |

### ColData Attributes

| Attribute | Description |
|-----------|-------------|
| `id` | Reference id of the entity |
| `value` | The value for column (type based on column type) |
| `href` | Link to quick zoom data (when `qzurl` parameter is specified) |

---

## Mercury Sync Application

For Mercury bank transaction sync, reports are useful for:

### 1. Reconciliation Verification

Use the **General Ledger** report to verify Mercury transactions are properly recorded:

```http
GET https://quickbooks.api.intuit.com/v3/company/<realmId>/reports/GeneralLedgerDetail?start_date=2024-01-01&end_date=2024-01-31&account=<mercury_account_id>
```

### 2. Bank Account Balance Verification

Use the **Balance Sheet** report to verify Mercury account balance:

```http
GET https://quickbooks.api.intuit.com/v3/company/<realmId>/reports/BalanceSheet?start_date=2024-01-01&end_date=2024-01-31
```

### 3. Vendor Expense Analysis

Track expenses by vendor after Mercury transaction sync:

```http
GET https://quickbooks.api.intuit.com/v3/company/<realmId>/reports/VendorExpenses?start_date=2024-01-01&end_date=2024-01-31
```

### 4. Profit and Loss Verification

Verify income and expenses are properly categorized:

```http
GET https://quickbooks.api.intuit.com/v3/company/<realmId>/reports/ProfitAndLoss?start_date=2024-01-01&end_date=2024-01-31
```

### Example: Parsing Report Response

```python
def parse_profit_loss_report(report_response):
    """Extract key metrics from P&L report"""
    result = {
        "report_name": report_response.get("Header", {}).get("ReportName"),
        "start_date": report_response.get("Header", {}).get("StartPeriod"),
        "end_date": report_response.get("Header", {}).get("EndPeriod"),
        "sections": {}
    }
    
    rows = report_response.get("Rows", {}).get("Row", [])
    for row in rows:
        if row.get("type") == "Section":
            group = row.get("group")
            summary = row.get("Summary", {})
            col_data = summary.get("ColData", [])
            if len(col_data) > 1:
                result["sections"][group] = col_data[1].get("value")
    
    return result
```

---

## Learn More

- [Reports API Reference](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/report-entities)
- [ProfitAndLoss Report](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/report-entities/profitandloss)
- [BalanceSheet Report](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/report-entities/balancesheet)
- [GeneralLedgerDetail Report](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/report-entities/generalledgerdetail)
