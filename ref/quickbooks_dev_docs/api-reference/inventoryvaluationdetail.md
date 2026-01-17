# InventoryValuationDetail

The information below provides a reference on how to access the Inventory Valuation Detail report from the QuickBooks Online Report Service.

## The InventoryValuationDetail Report Object

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
| Option | Array of options (e.g., NoReportData) |
| DateMacro | Date macro used (e.g., "this month") |
| StartPeriod | Start date of report period |
| EndPeriod | End date of report period |
| Currency | Currency code (e.g., USD) |
| Time | Timestamp of report generation |

### Rows Attributes

| Attribute | Description |
|-----------|-------------|
| Row | Array of row data |
| Header | Section header with item name |
| Rows | Nested rows for transaction details |
| ColData | Array of column data values for each row |
| id | Item or transaction ID reference |
| value | Display value |
| type | Row type (e.g., "Section", "Data") |
| Summary | Summary row data for sections |

### Columns Attributes

| Attribute | Description |
|-----------|-------------|
| Column | Array of column definitions |
| ColType | Column type (tx_date, txn_type, doc_num, name, quantity, rate, home_amount, qty_on_hand, home_asset_value) |
| ColTitle | Column title |

### Sample Object

```json
{
  "Header": {
    "ReportName": "InventoryValuationDetail", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "DateMacro": "this month", 
    "StartPeriod": "2024-06-01", 
    "Currency": "USD", 
    "EndPeriod": "2024-06-30", 
    "Time": "2024-06-27T08:27:23-07:00"
  }, 
  "Rows": {
    "Row": [
      {
        "Header": {
          "ColData": [
            {
              "id": "1010000081", 
              "value": "Item One"
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
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
                  "value": "2024-06-27"
                }, 
                {
                  "id": "1455000001", 
                  "value": "Inventory Starting Value"
                }, 
                {
                  "value": "START"
                }, 
                {
                  "id": "", 
                  "value": ""
                }, 
                {
                  "value": "10.00"
                }, 
                {
                  "value": "20.00"
                }, 
                {
                  "value": "200.00"
                }, 
                {
                  "value": "10.00"
                }, 
                {
                  "value": "200.00"
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
              "value": "Total for Item One"
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }, 
            {
              "value": "10.00"
            }, 
            {
              "value": ""
            }, 
            {
              "value": "200.00"
            }, 
            {
              "value": "10.00"
            }, 
            {
              "value": "200.00"
            }
          ]
        }
      }
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
        "ColType": "quantity", 
        "ColTitle": "Qty"
      }, 
      {
        "ColType": "rate", 
        "ColTitle": "Rate"
      }, 
      {
        "ColType": "home_amount", 
        "ColTitle": "FIFO Cost"
      }, 
      {
        "ColType": "qty_on_hand", 
        "ColTitle": "Qty On Hand"
      }, 
      {
        "ColType": "home_asset_value", 
        "ColTitle": "Asset Value"
      }
    ]
  }
}
```

## Query a Report

### Request URL

```
GET /v3/company/<realmID>/reports/InventoryValuationDetail?<name>=<value>[&...]
```

- **Accept type:** application/json
- **Production Base URL:** https://quickbooks.api.intuit.com
- **Sandbox Base URL:** https://sandbox-quickbooks.api.intuit.com

### Query Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| end_date | Optional | String | The end date of the report, in the format YYYY-MM-DD. start_date must be less than end_date. Use if you want the report to cover an explicit date range; otherwise, use date_macro to cover a standard report date range. If not specified value of date_macro is used |
| end_svcdate | Optional | String | The end service date of the report, in the format YYYY-MM-DD. start_date must be less than end_date. Use if you want the report to cover an explicit date range; otherwise, use date_macro to cover a standard report date range. If not specified value of date_macro is used |
| date_macro | Optional | String | Predefined date range. Use if you want the report to cover a standard report date range; otherwise, use the start_date and end_date to cover an explicit report date range. Supported Values: Today, Yesterday, This Week, Last Week, This Week-to-date, Last Week-to-date, Next Week, Next 4 Weeks, This Month, Last Month, This Month-to-date, Last Month-to-date, Next Month, This Fiscal Quarter, Last Fiscal Quarter, This Fiscal Quarter-to-date, Last Fiscal Quarter-to-date, Next Fiscal Quarter, This Fiscal Year, Last Fiscal Year, This Fiscal Year-to-date, Last Fiscal Year-to-date, Next Fiscal Year |
| svcdate_macro | Optional | String | Predefined date range for service date. Use if you want the report to cover a standard report date range; otherwise, use the start_date and end_date to cover an explicit report date range. Supported Values: Today, Yesterday, This Week, Last Week, This Week-to-date, Last Week-to-date, Next Week, Next 4 Weeks, This Month, Last Month, This Month-to-date, Last Month-to-date, Next Month, This Fiscal Quarter, Last Fiscal Quarter, This Fiscal Quarter-to-date, Last Fiscal Quarter-to-date, Next Fiscal Quarter, This Fiscal Year, Last Fiscal Year, This Fiscal Year-to-date, Last Fiscal Year-to-date, Next Fiscal Year |
| start_svcdate | Optional | String | The start service date of the report, in the format YYYY-MM-DD. start_date must be less than end_date. Use if you want the report to cover an explicit date range; otherwise, use date_macro to cover a standard report date range. If not specified value of date_macro is used |
| group_by | Optional | String | The field in the transaction by which to group results. Supported Values: Name, Account, Transaction Type, Customer, Vendor, Employee, Location, Payment Method, Day, Week, Month, Quarter, Year, None |
| start_date | Optional | String | The start date of the report, in the format YYYY-MM-DD. start_date must be less than end_date. Use if you want the report to cover an explicit date range; otherwise, use date_macro to cover a standard report date range. If not specified value of date_macro is used |
| columns | Optional | String | Column types to show in the report. Supported Values: tx_date, txn_id, txn_type, doc_num, name, quantity, rate, home_amount, qty_on_hand, asset_value, create_date, create_by, last_mod_date, last_mod_by, item_sku, memo, exch_rate, account_name, service_date, rate_inventory, qty_on_hand, asset_value_nt, tracking_num |

### Sample Query

```
GET https://quickbooks.api.intuit.com/v3/company/1386066315/reports/InventoryValuationDetail?date_macro=This Month
```

### Sample Response

```json
{
  "Header": {
    "ReportName": "InventoryValuationDetail", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "DateMacro": "this month", 
    "StartPeriod": "2024-06-01", 
    "Currency": "USD", 
    "EndPeriod": "2024-06-30", 
    "Time": "2024-06-27T08:27:23-07:00"
  }, 
  "Rows": {
    "Row": [
      {
        "Header": {
          "ColData": [
            {
              "id": "1010000081", 
              "value": "Item One"
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
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
                  "value": "2024-06-27"
                }, 
                {
                  "id": "1455000001", 
                  "value": "Inventory Starting Value"
                }, 
                {
                  "value": "START"
                }, 
                {
                  "id": "", 
                  "value": ""
                }, 
                {
                  "value": "10.00"
                }, 
                {
                  "value": "20.00"
                }, 
                {
                  "value": "200.00"
                }, 
                {
                  "value": "10.00"
                }, 
                {
                  "value": "200.00"
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
              "value": "Total for Item One"
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }, 
            {
              "value": ""
            }, 
            {
              "value": "10.00"
            }, 
            {
              "value": ""
            }, 
            {
              "value": "200.00"
            }, 
            {
              "value": "10.00"
            }, 
            {
              "value": "200.00"
            }
          ]
        }
      }
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
        "ColType": "quantity", 
        "ColTitle": "Qty"
      }, 
      {
        "ColType": "rate", 
        "ColTitle": "Rate"
      }, 
      {
        "ColType": "home_amount", 
        "ColTitle": "FIFO Cost"
      }, 
      {
        "ColType": "qty_on_hand", 
        "ColTitle": "Qty On Hand"
      }, 
      {
        "ColType": "home_asset_value", 
        "ColTitle": "Asset Value"
      }
    ]
  }
}
```

## Report Columns

| Column | ColType | Description |
|--------|---------|-------------|
| Date | tx_date | Transaction date |
| Transaction Type | txn_type | Type of transaction (e.g., Inventory Starting Value) |
| Num | doc_num | Document number |
| Name | name | Customer/Vendor name |
| Qty | quantity | Quantity changed |
| Rate | rate | Unit rate |
| FIFO Cost | home_amount | FIFO cost amount |
| Qty On Hand | qty_on_hand | Quantity on hand after transaction |
| Asset Value | home_asset_value | Total asset value |

## Available Columns for Query

The following column types can be specified in the `columns` parameter:

- tx_date, txn_id, txn_type, doc_num, name
- quantity, rate, home_amount, qty_on_hand, asset_value
- create_date, create_by, last_mod_date, last_mod_by
- item_sku, memo, exch_rate, account_name, service_date
- rate_inventory, asset_value_nt, tracking_num
