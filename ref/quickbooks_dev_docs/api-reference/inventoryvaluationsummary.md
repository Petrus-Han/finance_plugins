# InventoryValuationSummary

The information below provides a reference on how to access the Inventory Valuation summary report from the QuickBooks Online Report Service.

## The InventoryValuationSummary Report Object

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
| ReportName | Name of the report |
| Option | Array of options (e.g., report_date, NoReportData) |
| DateMacro | Date macro used (e.g., "today") |
| StartPeriod | Start date of report period |
| EndPeriod | End date of report period |
| Currency | Currency code (e.g., USD) |
| Time | Timestamp of report generation |

### Rows Attributes

| Attribute | Description |
|-----------|-------------|
| Row | Array of row data |
| ColData | Array of column data values for each row |
| id | Item ID reference |
| value | Display value (item name or amount) |
| group | Group type (e.g., "GrandTotal") |

### Columns Attributes

| Attribute | Description |
|-----------|-------------|
| Column | Array of column definitions |
| ColType | Column type (ProductsAndService, Money) |
| ColTitle | Column title (e.g., "SKU", "Qty", "Asset Value", "Avg Cost") |

### Sample Object

```json
{
  "Header": {
    "ReportName": "InventoryValuationSummary", 
    "Option": [
      {
        "Name": "report_date", 
        "Value": "2016-10-06"
      }, 
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "DateMacro": "today", 
    "StartPeriod": "2016-10-06", 
    "Currency": "USD", 
    "EndPeriod": "2016-10-06", 
    "Time": "2016-10-06T09:28:21-07:00"
  }, 
  "Rows": {
    "Row": [
      {
        "ColData": [
          {
            "id": "11", 
            "value": "Pump"
          }, 
          {
            "value": "2890"
          }, 
          {
            "value": "25.00"
          }, 
          {
            "value": "250.00"
          }, 
          {
            "value": "10.00"
          }
        ]
      }, 
      {
        "ColData": [
          {
            "id": "5", 
            "value": "Rock Fountain"
          }, 
          {
            "value": "2345"
          }, 
          {
            "value": "2.00"
          }, 
          {
            "value": "250.00"
          }, 
          {
            "value": "125.00"
          }
        ]
      }, 
      {
        "ColData": [
          {
            "id": "16", 
            "value": "Sprinkler Heads"
          }, 
          {
            "value": "3456"
          }, 
          {
            "value": "25.00"
          }, 
          {
            "value": "18.75"
          }, 
          {
            "value": "0.75"
          }
        ]
      }, 
      {
        "ColData": [
          {
            "id": "17", 
            "value": "Sprinkler Pipes"
          }, 
          {
            "value": "5678"
          }, 
          {
            "value": "31.00"
          }, 
          {
            "value": "77.50"
          }, 
          {
            "value": "2.50"
          }
        ]
      }, 
      {
        "ColData": [
          {
            "value": "TOTAL"
          }, 
          {
            "value": " "
          }, 
          {
            "value": ""
          }, 
          {
            "value": "596.25"
          }, 
          {
            "value": ""
          }
        ], 
        "group": "GrandTotal"
      }
    ]
  }, 
  "Columns": {
    "Column": [
      {
        "ColType": "ProductsAndService", 
        "ColTitle": ""
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "SKU"
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "Qty"
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "Asset Value"
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "Avg Cost"
      }
    ]
  }
}
```

## Query a Report

### Request URL

```
GET /v3/company/<realmID>/reports/InventoryValuationSummary?<name>=<value>[&...]
```

- **Accept type:** application/json
- **Production Base URL:** https://quickbooks.api.intuit.com
- **Sandbox Base URL:** https://sandbox-quickbooks.api.intuit.com

### Query Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| qzurl | Optional | String | Specifies whether Quick Zoom URL information should be generated for rows in the report. Quick Zoom URL is a hyperlink to another report containing further details about the particular column of data. Supported Values: true, false |
| date_macro | Optional | String | Predefined date range. Use if you want the report to cover a standard report date range; otherwise, use the start_date and end_date to cover an explicit report date range. Supported Values: Today, Yesterday, This Week, Last Week, This Week-to-date, Last Week-to-date, Next Week, Next 4 Weeks, This Month, Last Month, This Month-to-date, Last Month-to-date, Next Month, This Fiscal Quarter, Last Fiscal Quarter, This Fiscal Quarter-to-date, Last Fiscal Quarter-to-date, Next Fiscal Quarter, This Fiscal Year, Last Fiscal Year, This Fiscal Year-to-date, Last Fiscal Year-to-date, Next Fiscal Year |
| item | Optional | String | Filters report contents to include information for specified items. Supported Values: One or more comma separated item IDs as returned in the attribute, Item.Id, of the Item entity response code |
| report_date | Optional | String | Start date to use for the report, in the format YYYY-MM-DD |
| sort_order | Optional | String | The sort order. Supported Values: ascend, descend |
| summarize_column_by | Optional | String | The criteria by which to group the report results. Supported Values: Total, Month, Week, Days, Quarter, Year, Customers, Vendors, Classes, Departments, Employees, ProductsAndServices |

### Sample Query

```
GET https://quickbooks.api.intuit.com/v3/company/1386066315/reports/InventoryValuationSummary?date_macro=This Fiscal Year-to-date
```

### Sample Response

```json
{
  "Header": {
    "ReportName": "InventoryValuationSummary", 
    "Option": [
      {
        "Name": "report_date", 
        "Value": "2016-10-06"
      }, 
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "DateMacro": "today", 
    "StartPeriod": "2016-10-06", 
    "Currency": "USD", 
    "EndPeriod": "2016-10-06", 
    "Time": "2016-10-06T09:28:21-07:00"
  }, 
  "Rows": {
    "Row": [
      {
        "ColData": [
          {
            "id": "11", 
            "value": "Pump"
          }, 
          {
            "value": "2890"
          }, 
          {
            "value": "25.00"
          }, 
          {
            "value": "250.00"
          }, 
          {
            "value": "10.00"
          }
        ]
      }, 
      {
        "ColData": [
          {
            "id": "5", 
            "value": "Rock Fountain"
          }, 
          {
            "value": "2345"
          }, 
          {
            "value": "2.00"
          }, 
          {
            "value": "250.00"
          }, 
          {
            "value": "125.00"
          }
        ]
      }, 
      {
        "ColData": [
          {
            "id": "16", 
            "value": "Sprinkler Heads"
          }, 
          {
            "value": "3456"
          }, 
          {
            "value": "25.00"
          }, 
          {
            "value": "18.75"
          }, 
          {
            "value": "0.75"
          }
        ]
      }, 
      {
        "ColData": [
          {
            "id": "17", 
            "value": "Sprinkler Pipes"
          }, 
          {
            "value": "5678"
          }, 
          {
            "value": "31.00"
          }, 
          {
            "value": "77.50"
          }, 
          {
            "value": "2.50"
          }
        ]
      }, 
      {
        "ColData": [
          {
            "value": "TOTAL"
          }, 
          {
            "value": " "
          }, 
          {
            "value": ""
          }, 
          {
            "value": "596.25"
          }, 
          {
            "value": ""
          }
        ], 
        "group": "GrandTotal"
      }
    ]
  }, 
  "Columns": {
    "Column": [
      {
        "ColType": "ProductsAndService", 
        "ColTitle": ""
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "SKU"
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "Qty"
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "Asset Value"
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "Avg Cost"
      }
    ]
  }
}
```

## Report Columns

| Column | Description |
|--------|-------------|
| (Product/Service) | Product or service name (with ID reference) |
| SKU | Stock keeping unit identifier |
| Qty | Quantity on hand |
| Asset Value | Total value of inventory |
| Avg Cost | Average cost per unit |
