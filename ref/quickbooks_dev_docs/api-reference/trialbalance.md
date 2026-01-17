# TrialBalance

The information below provides a reference on how to access the Trial Balance report from the QuickBooks Online Report Service. For France-based companies, use TrialBalanceFR as the endpoint.

## The TrialBalance Report Object

The table below lists all possible attributes that can be returned in the report response. Values are not localized unless indicated.

### Attributes

| Attribute | Description |
|-----------|-------------|
| Header | The report header |
| Rows | Top level container holding information for trial balance report rows |
| Columns | Top level container holding information for report columns or subcolumns |

### Header Attributes

| Attribute | Description |
|-----------|-------------|
| ReportName | Name of the report |
| Option | Array of options (e.g., NoReportData) |
| DateMacro | Date macro used (e.g., "this month-to-date") |
| ReportBasis | Accounting basis (Accrual or Cash) |
| StartPeriod | Start date of report period |
| EndPeriod | End date of report period |
| Currency | Currency code (e.g., USD) |
| Time | Timestamp of report generation |

### Rows Attributes

| Attribute | Description |
|-----------|-------------|
| Row | Array of row data |
| ColData | Array of column data values for each row |
| id | Account ID reference |
| value | Display value (account name or amount) |
| group | Group type (e.g., "GrandTotal") |
| type | Section type (e.g., "Section") |
| Summary | Summary row data for sections |

### Columns Attributes

| Attribute | Description |
|-----------|-------------|
| Column | Array of column definitions |
| ColType | Column type (Account, Money) |
| ColTitle | Column title (e.g., "Debit", "Credit") |

### Sample Object

```json
{
  "Header": {
    "ReportName": "TrialBalance", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "DateMacro": "this month-to-date", 
    "ReportBasis": "Accrual", 
    "StartPeriod": "2016-03-01", 
    "Currency": "USD", 
    "EndPeriod": "2016-03-14", 
    "Time": "2016-03-14T10:11:07-07:00"
  }, 
  "Rows": {
    "Row": [
      {
        "ColData": [
          {
            "id": "35", 
            "value": "Checking"
          }, 
          {
            "value": "4151.74"
          }, 
          {
            "value": ""
          }
        ]
      }, 
      {
        "ColData": [
          {
            "id": "13", 
            "value": "Meals and Entertainment"
          }, 
          {
            "value": ""
          }, 
          {
            "value": "46.00"
          }
        ]
      }, 
      {
        "ColData": [
          {
            "id": "93", 
            "value": "QuickBooks Payments Fees"
          }, 
          {
            "value": "0.44"
          }, 
          {
            "value": ""
          }
        ]
      }, 
      {
        "group": "GrandTotal", 
        "type": "Section", 
        "Summary": {
          "ColData": [
            {
              "value": "TOTAL"
            }, 
            {
              "value": "36587.47"
            }, 
            {
              "value": "36587.47"
            }
          ]
        }
      }
    ]
  }, 
  "Columns": {
    "Column": [
      {
        "ColType": "Account", 
        "ColTitle": ""
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "Debit"
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "Credit"
      }
    ]
  }
}
```

## Query a Report

### Request URL

**FR locale:**
```
GET /v3/company/<realmID>/reports/TrialBalanceFR?minorversion=4&<name>=<value>[&...]
```

**Non-FR locales:**
```
GET /v3/company/<realmID>/reports/TrialBalance?<name>=<value>[&...]
```

- **Accept type:** application/json
- **Production Base URL:** https://quickbooks.api.intuit.com
- **Sandbox Base URL:** https://sandbox-quickbooks.api.intuit.com

### Query Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| accounting_method | Optional | String | The accounting method used in the report. Supported Values: Cash, Accrual |
| end_date | Optional | String | The end date of the report, in the format YYYY-MM-DD. start_date must be less than end_date. Use if you want the report to cover an explicit date range; otherwise, use date_macro to cover a standard report date range. If not specified value of date_macro is used |
| date_macro | Optional | String | Predefined date range. Use if you want the report to cover a standard report date range; otherwise, use the start_date and end_date to cover an explicit report date range. Supported Values: Today, Yesterday, This Week, Last Week, This Week-to-date, Last Week-to-date, Next Week, Next 4 Weeks, This Month, Last Month, This Month-to-date, Last Month-to-date, Next Month, This Fiscal Quarter, Last Fiscal Quarter, This Fiscal Quarter-to-date, Last Fiscal Quarter-to-date, Next Fiscal Quarter, This Fiscal Year, Last Fiscal Year, This Fiscal Year-to-date, Last Fiscal Year-to-date, Next Fiscal Year |
| sort_order | Optional | String | The sort order. Supported Values: ascend, descend |
| summarize_column_by | Optional | String | The criteria by which to group the report results. Supported Values: Total, Month, Week, Days, Quarter, Year, Customers, Vendors, Classes, Departments, Employees, ProductsAndServices |
| start_date | Optional | String | The start date of the report, in the format YYYY-MM-DD. start_date must be less than end_date. Use if you want the report to cover an explicit date range; otherwise, use date_macro to cover a standard report date range. If not specified value of date_macro is used |

### Sample Query

**For non-FR locales:**
```
GET https://quickbooks.api.intuit.com/v3/company/1386066315/reports/TrialBalance
```

**For FR locale:**
```
GET https://quickbooks.api.intuit.com/v3/company/1386066315/reports/TrialBalanceFR?minorversion=4
```

### Sample Response

```json
{
  "Header": {
    "ReportName": "TrialBalance", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "DateMacro": "this month-to-date", 
    "ReportBasis": "Accrual", 
    "StartPeriod": "2016-03-01", 
    "Currency": "USD", 
    "EndPeriod": "2016-03-14", 
    "Time": "2016-03-14T10:11:07-07:00"
  }, 
  "Rows": {
    "Row": [
      {
        "ColData": [
          {
            "id": "35", 
            "value": "Checking"
          }, 
          {
            "value": "4151.74"
          }, 
          {
            "value": ""
          }
        ]
      }, 
      {
        "ColData": [
          {
            "id": "13", 
            "value": "Meals and Entertainment"
          }, 
          {
            "value": ""
          }, 
          {
            "value": "46.00"
          }
        ]
      }, 
      {
        "ColData": [
          {
            "id": "93", 
            "value": "QuickBooks Payments Fees"
          }, 
          {
            "value": "0.44"
          }, 
          {
            "value": ""
          }
        ]
      }, 
      {
        "group": "GrandTotal", 
        "type": "Section", 
        "Summary": {
          "ColData": [
            {
              "value": "TOTAL"
            }, 
            {
              "value": "36587.47"
            }, 
            {
              "value": "36587.47"
            }
          ]
        }
      }
    ]
  }, 
  "Columns": {
    "Column": [
      {
        "ColType": "Account", 
        "ColTitle": ""
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "Debit"
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "Credit"
      }
    ]
  }
}
```

## Report Columns

| Column | Description |
|--------|-------------|
| Account | Account name (with ID reference) |
| Debit | Debit balance amount |
| Credit | Credit balance amount |
