# BalanceSheet

The information below provides a reference on how to query the Balance Sheet report from the QuickBooks Online Report Service.

## The BalanceSheet Report Object

The table below lists all possible attributes that can be returned in the report response.

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **Header** | Object | The report header containing report metadata. |
| **Rows** | Object | Top level container holding information for Balance Sheet report rows. |
| **Columns** | Object | Top level container holding information for report columns or subcolumns. |

### Header Child Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **Time** | DateTime | Time the report was generated. |
| **ReportName** | String | Name of the report. |
| **DateMacro** | String | Date macro used (e.g., "This Fiscal Year-to-date"). |
| **StartPeriod** | Date | Start date of report period. |
| **EndPeriod** | Date | End date of report period. |
| **ReportBasis** | String | Accounting basis (Cash or Accrual). |
| **Currency** | String | Currency code (e.g., "USD"). |
| **Option** | Array | Report options that were used. |

### Rows Child Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **Row** | Array | Array of row objects. |
| **Row.type** | String | Type of row: "Section", "Data", "Summary". |
| **Row.group** | String | Grouping category (e.g., "Asset", "Liability", "Equity"). |
| **Row.Header** | Object | Header for section rows. |
| **Row.Rows** | Object | Nested rows within a section. |
| **Row.Summary** | Object | Summary data for the section. |
| **Row.ColData** | Array | Column data values for data rows. |

### Columns Child Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **Column** | Array | Array of column definitions. |
| **Column.ColTitle** | String | Column title. |
| **Column.ColType** | String | Column type (e.g., "Account", "Money"). |
| **Column.MetaData** | Array | Column metadata. |

## Query a Report

### Request URL

```
GET /v3/company/<realmID>/reports/BalanceSheet
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| **start_date** | Date | Start date for the report (YYYY-MM-DD). |
| **end_date** | Date | End date for the report (YYYY-MM-DD). |
| **accounting_method** | String | Accounting method: "Cash" or "Accrual". |
| **date_macro** | String | Predefined date range: "Today", "Yesterday", "This Week", "This Month", "This Fiscal Quarter", "This Fiscal Year", "This Fiscal Year-to-date", "Last Week", "Last Month", "Last Fiscal Quarter", "Last Fiscal Year", etc. |
| **summarize_column_by** | String | Summarize by: "Total", "Month", "Week", "Days", "Quarter", "Year", "Customers", "Vendors", "Classes", "Departments", "Employees", "ProductsAndServices". |
| **customer** | String | Filter by customer ID. |
| **vendor** | String | Filter by vendor ID. |
| **item** | String | Filter by item ID. |
| **class** | String | Filter by class ID. |
| **department** | String | Filter by department/location ID. |
| **minorversion** | Integer | Minor version for the API (e.g., 65). |

### Sample Request

```
GET /v3/company/1234567890/reports/BalanceSheet?date_macro=This%20Fiscal%20Year-to-date&minorversion=65
```

### Sample Response

```json
{
  "Header": {
    "Time": "2024-01-15T10:30:00-08:00",
    "ReportName": "BalanceSheet",
    "DateMacro": "This Fiscal Year-to-date",
    "StartPeriod": "2024-01-01",
    "EndPeriod": "2024-01-15",
    "ReportBasis": "Accrual",
    "Currency": "USD",
    "Option": [
      {
        "Name": "AccountingStandard",
        "Value": "GAAP"
      },
      {
        "Name": "NoReportData",
        "Value": "false"
      }
    ]
  },
  "Columns": {
    "Column": [
      {
        "ColTitle": "",
        "ColType": "Account",
        "MetaData": [
          {
            "Name": "ColKey",
            "Value": "account"
          }
        ]
      },
      {
        "ColTitle": "Total",
        "ColType": "Money",
        "MetaData": [
          {
            "Name": "ColKey",
            "Value": "total"
          }
        ]
      }
    ]
  },
  "Rows": {
    "Row": [
      {
        "Header": {
          "ColData": [
            {
              "value": "ASSETS"
            },
            {
              "value": ""
            }
          ]
        },
        "Rows": {
          "Row": [
            {
              "Header": {
                "ColData": [
                  {
                    "value": "Current Assets"
                  },
                  {
                    "value": ""
                  }
                ]
              },
              "Rows": {
                "Row": [
                  {
                    "Header": {
                      "ColData": [
                        {
                          "value": "Bank Accounts"
                        },
                        {
                          "value": ""
                        }
                      ]
                    },
                    "Rows": {
                      "Row": [
                        {
                          "ColData": [
                            {
                              "value": "Checking",
                              "id": "35"
                            },
                            {
                              "value": "1350.55"
                            }
                          ],
                          "type": "Data"
                        },
                        {
                          "ColData": [
                            {
                              "value": "Savings",
                              "id": "36"
                            },
                            {
                              "value": "800.00"
                            }
                          ],
                          "type": "Data"
                        }
                      ]
                    },
                    "Summary": {
                      "ColData": [
                        {
                          "value": "Total Bank Accounts"
                        },
                        {
                          "value": "2150.55"
                        }
                      ]
                    },
                    "type": "Section",
                    "group": "BankAccounts"
                  }
                ]
              },
              "Summary": {
                "ColData": [
                  {
                    "value": "Total Current Assets"
                  },
                  {
                    "value": "2150.55"
                  }
                ]
              },
              "type": "Section",
              "group": "CurrentAssets"
            }
          ]
        },
        "Summary": {
          "ColData": [
            {
              "value": "TOTAL ASSETS"
            },
            {
              "value": "2150.55"
            }
          ]
        },
        "type": "Section",
        "group": "TotalAssets"
      },
      {
        "Header": {
          "ColData": [
            {
              "value": "LIABILITIES AND EQUITY"
            },
            {
              "value": ""
            }
          ]
        },
        "Rows": {
          "Row": []
        },
        "Summary": {
          "ColData": [
            {
              "value": "TOTAL LIABILITIES AND EQUITY"
            },
            {
              "value": "2150.55"
            }
          ]
        },
        "type": "Section",
        "group": "TotalLiabilitiesAndEquity"
      }
    ]
  }
}
```

## Report Sections

The Balance Sheet report contains the following main sections:

| Section | Description |
|---------|-------------|
| **ASSETS** | Total assets owned by the company. |
| **Current Assets** | Short-term assets (cash, accounts receivable, inventory). |
| **Bank Accounts** | Cash in bank accounts. |
| **Accounts Receivable** | Money owed to the company. |
| **Other Current Assets** | Other short-term assets. |
| **Fixed Assets** | Long-term assets (property, equipment). |
| **Other Assets** | Non-current assets. |
| **LIABILITIES AND EQUITY** | Obligations and ownership equity. |
| **Liabilities** | Amounts owed to creditors. |
| **Current Liabilities** | Short-term obligations. |
| **Long-Term Liabilities** | Long-term debt. |
| **Equity** | Owner's equity and retained earnings. |
