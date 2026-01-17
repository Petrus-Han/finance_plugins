# ProfitAndLoss

The information below provides a reference on how to access the Profit and Loss Summary report from the QuickBooks Online Report Service.

## The ProfitAndLoss Report Object

The table below lists all possible attributes that can be returned in the report response.

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **Header** | Object | The report header containing report metadata. |
| **Rows** | Object | Top level container holding information for profit and loss report rows. |
| **Columns** | Object | Top level container holding information for report columns or subcolumns. |

### Header Child Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **Time** | DateTime | Time the report was generated. |
| **ReportName** | String | Name of the report ("ProfitAndLoss"). |
| **StartPeriod** | Date | Start date of report period. |
| **EndPeriod** | Date | End date of report period. |
| **ReportBasis** | String | Accounting basis (Cash or Accrual). |
| **Currency** | String | Currency code (e.g., "USD"). |
| **SummarizeColumnsBy** | String | How columns are summarized. |
| **Customer** | String | Customer ID if filtered. |
| **Option** | Array | Report options that were used. |

## Query a Report

### Request URL

```
GET /v3/company/<realmID>/reports/ProfitAndLoss?<name>=<value>[&...]
Accept type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **customer** | String | Optional | Filters report contents to include information for specified customers. One or more comma separated customer IDs. |
| **qzurl** | String | Optional | Specifies whether Quick Zoom URL information should be generated for rows in the report. Values: true, false. |
| **accounting_method** | String | Optional | The accounting method used in the report. Values: Cash, Accrual. |
| **end_date** | String | Optional | The end date of the report (YYYY-MM-DD). start_date must be less than end_date. |
| **date_macro** | String | Optional | Predefined date range. Values: Today, Yesterday, This Week, Last Week, This Week-to-date, Last Week-to-date, Next Week, Next 4 Weeks, This Month, Last Month, This Month-to-date, Last Month-to-date, Next Month, This Fiscal Quarter, Last Fiscal Quarter, This Fiscal Quarter-to-date, Last Fiscal Quarter-to-date, Next Fiscal Quarter, This Fiscal Year, Last Fiscal Year, This Fiscal Year-to-date, Last Fiscal Year-to-date, Next Fiscal Year. |
| **adjusted_gain_loss** | String | Optional | Specifies whether unrealized gain and losses are included in the report. Values: true, false. |
| **class** | String | Optional | Filters report contents to include information for specified classes. One or more comma separated class IDs. |
| **item** | String | Optional | Filters report contents to include information for specified items. One or more comma separated item IDs. |
| **sort_order** | String | Optional | The sort order. Values: ascend, descend. |
| **summarize_column_by** | String | Optional | The criteria by which to group the report results. Values: Total, Month, Week, Days, Quarter, Year, Customers, Vendors, Classes, Departments, Employees, ProductsAndServices. |
| **department** | String | Optional | Filters report contents to include information for specified departments. One or more comma separated department IDs. |
| **vendor** | String | Optional | Filters report contents to include information for specified vendors. One or more comma separated vendor IDs. |
| **start_date** | String | Optional | The start date of the report (YYYY-MM-DD). start_date must be less than end_date. |

### Sample Query

```
GET /v3/company/companyId/reports/ProfitAndLoss?start_date=2015-06-01&end_date=2015-06-30&customer=1
```

### Sample Response

```json
{
  "Header": {
    "Customer": "1",
    "ReportName": "ProfitAndLoss",
    "Option": [
      {
        "Name": "AccountingStandard",
        "Value": "GAAP"
      },
      {
        "Name": "NoReportData",
        "Value": "false"
      }
    ],
    "ReportBasis": "Accrual",
    "StartPeriod": "2015-06-01",
    "Currency": "USD",
    "EndPeriod": "2015-06-30",
    "Time": "2016-03-03T13:00:18-08:00",
    "SummarizeColumnsBy": "Total"
  },
  "Rows": {
    "Row": [
      {
        "Header": {
          "ColData": [
            {
              "value": "Income"
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
                    "id": "45",
                    "value": "Landscaping Services"
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
                          "id": "46",
                          "value": "Job Materials"
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
                              "id": "48",
                              "value": "Fountains and Garden Lighting"
                            },
                            {
                              "value": "275.00"
                            }
                          ],
                          "type": "Data"
                        },
                        {
                          "ColData": [
                            {
                              "id": "49",
                              "value": "Plants and Soil"
                            },
                            {
                              "value": "150.00"
                            }
                          ],
                          "type": "Data"
                        }
                      ]
                    },
                    "type": "Section",
                    "Summary": {
                      "ColData": [
                        {
                          "value": "Total Job Materials"
                        },
                        {
                          "value": "425.00"
                        }
                      ]
                    }
                  }
                ]
              },
              "type": "Section",
              "Summary": {
                "ColData": [
                  {
                    "value": "Total Landscaping Services"
                  },
                  {
                    "value": "425.00"
                  }
                ]
              }
            },
            {
              "ColData": [
                {
                  "id": "54",
                  "value": "Pest Control Services"
                },
                {
                  "value": "-100.00"
                }
              ],
              "type": "Data"
            }
          ]
        },
        "type": "Section",
        "group": "Income",
        "Summary": {
          "ColData": [
            {
              "value": "Total Income"
            },
            {
              "value": "325.00"
            }
          ]
        }
      },
      {
        "group": "GrossProfit",
        "type": "Section",
        "Summary": {
          "ColData": [
            {
              "value": "Gross Profit"
            },
            {
              "value": "325.00"
            }
          ]
        }
      },
      {
        "Header": {
          "ColData": [
            {
              "value": "Expenses"
            },
            {
              "value": ""
            }
          ]
        },
        "type": "Section",
        "group": "Expenses",
        "Summary": {
          "ColData": [
            {
              "value": "Total Expenses"
            },
            {
              "value": ""
            }
          ]
        }
      },
      {
        "group": "NetOperatingIncome",
        "type": "Section",
        "Summary": {
          "ColData": [
            {
              "value": "Net Operating Income"
            },
            {
              "value": "325.00"
            }
          ]
        }
      },
      {
        "group": "NetIncome",
        "type": "Section",
        "Summary": {
          "ColData": [
            {
              "value": "Net Income"
            },
            {
              "value": "325.00"
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
        "ColTitle": "",
        "MetaData": [
          {
            "Name": "ColKey",
            "Value": "account"
          }
        ]
      },
      {
        "ColType": "Money",
        "ColTitle": "Total",
        "MetaData": [
          {
            "Name": "ColKey",
            "Value": "total"
          }
        ]
      }
    ]
  }
}
```

## Report Sections

The Profit and Loss report contains the following main sections:

| Section Group | Description |
|---------------|-------------|
| **Income** | Total revenue from sales and services. |
| **Cost of Goods Sold** | Direct costs attributable to goods sold. |
| **GrossProfit** | Income minus Cost of Goods Sold. |
| **Expenses** | Operating expenses. |
| **NetOperatingIncome** | Gross Profit minus Expenses. |
| **Other Income** | Non-operating income. |
| **Other Expenses** | Non-operating expenses. |
| **NetOtherIncome** | Other Income minus Other Expenses. |
| **NetIncome** | Final bottom line (Net Operating Income + Net Other Income). |
