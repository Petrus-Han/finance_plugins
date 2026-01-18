# SalesByDepartment

The information below provides a reference on how to access the Sales by Department report from the QuickBooks Online Report Service.

## The SalesByDepartment Report Object

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
| ReportName | Name of the report (DepartmentSales) |
| Option | Array of options (e.g., NoReportData) |
| ReportBasis | Accounting basis (Accrual or Cash) |
| StartPeriod | Start date of report period |
| EndPeriod | End date of report period |
| Currency | Currency code (e.g., USD) |
| Time | Timestamp of report generation |
| SummarizeColumnsBy | Column summarization method |

### Rows Attributes

| Attribute | Description |
|-----------|-------------|
| Row | Array of row data |
| ColData | Array of column data values for each row |
| value | Display value (department name or amount) |
| group | Group type (e.g., "GrandTotal", "**" for Not Specified) |
| type | Section type (e.g., "Section") |
| Summary | Summary row data for sections |

### Columns Attributes

| Attribute | Description |
|-----------|-------------|
| Column | Array of column definitions |
| ColType | Column type (Department, Money) |
| ColTitle | Column title (e.g., "Total") |

### Sample Object

```json
{
  "Header": {
    "ReportName": "DepartmentSales", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "ReportBasis": "Accrual", 
    "StartPeriod": "2015-08-01", 
    "Currency": "USD", 
    "EndPeriod": "2015-09-30", 
    "Time": "2016-03-10T15:26:27-08:00", 
    "SummarizeColumnsBy": "Total"
  }, 
  "Rows": {
    "Row": [
      {
        "ColData": [
          {
            "value": "Not Specified"
          }, 
          {
            "value": "1200.00"
          }
        ], 
        "group": "**"
      }, 
      {
        "group": "GrandTotal", 
        "type": "Section", 
        "Summary": {
          "ColData": [
            {
              "value": "Total"
            }, 
            {
              "value": "1200.00"
            }
          ]
        }
      }
    ]
  }, 
  "Columns": {
    "Column": [
      {
        "ColType": "Department", 
        "ColTitle": ""
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "Total"
      }
    ]
  }
}
```

## Query a Report

### Request URL

```
GET /v3/company/<realmID>/reports/DepartmentSales?<name>=<value>[&...]
```

- **Accept type:** application/json
- **Production Base URL:** https://quickbooks.api.intuit.com
- **Sandbox Base URL:** https://sandbox-quickbooks.api.intuit.com

### Query Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| customer | Optional | String | Filters report contents to include information for specified customers. Supported Values: One or more comma separated customer IDs as returned in the attribute, Customer.Id, of the Customer object response code |
| accounting_method | Optional | String | The accounting method used in the report. Supported Values: Cash, Accrual |
| end_date | Optional | String | The end date of the report, in the format YYYY-MM-DD. start_date must be less than end_date. Use if you want the report to cover an explicit date range; otherwise, use date_macro to cover a standard report date range. If not specified value of date_macro is used |
| date_macro | Optional | String | Predefined date range. Use if you want the report to cover a standard report date range; otherwise, use the start_date and end_date to cover an explicit report date range. Supported Values: Today, Yesterday, This Week, Last Week, This Week-to-date, Last Week-to-date, Next Week, Next 4 Weeks, This Month, Last Month, This Month-to-date, Last Month-to-date, Next Month, This Fiscal Quarter, Last Fiscal Quarter, This Fiscal Quarter-to-date, Last Fiscal Quarter-to-date, Next Fiscal Quarter, This Fiscal Year, Last Fiscal Year, This Fiscal Year-to-date, Last Fiscal Year-to-date, Next Fiscal Year |
| class | Optional | String | Filters report contents to include information for specified classes if so configured in the company file. Supported Values: One or more comma separated class IDs as returned in the attribute, Class.Id, of the Class entity response code |
| item | Optional | String | Filters report contents to include information for specified items. Supported Values: One or more comma separated item IDs as returned in the attribute, Item.Id, of the Item entity response code |
| sort_order | Optional | String | The sort order. Supported Values: ascend, descend |
| summarize_column_by | Optional | String | The criteria by which to group the report results. Supported Values: Total, Month, Week, Days, Quarter, Year, Customers, Vendors, Classes, Departments, Employees, ProductsAndServices |
| department | Optional | String | Filters report contents to include information for specified departments if so configured in the company file. Supported Values: One or more comma separated department IDs as returned in the attribute, Department.Id of the Department object response code |
| start_date | Optional | String | The start date of the report, in the format YYYY-MM-DD. start_date must be less than end_date. Use if you want the report to cover an explicit date range; otherwise, use date_macro to cover a standard report date range. If not specified value of date_macro is used |

### Sample Query

```
GET https://quickbooks.api.intuit.com/v3/company/1386066315/reports/DepartmentSales?start_date=2015-08-01&end_date=2015-09-30
```

### Sample Response

```json
{
  "Header": {
    "ReportName": "DepartmentSales", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "ReportBasis": "Accrual", 
    "StartPeriod": "2015-08-01", 
    "Currency": "USD", 
    "EndPeriod": "2015-09-30", 
    "Time": "2016-03-10T15:26:27-08:00", 
    "SummarizeColumnsBy": "Total"
  }, 
  "Rows": {
    "Row": [
      {
        "ColData": [
          {
            "value": "Not Specified"
          }, 
          {
            "value": "1200.00"
          }
        ], 
        "group": "**"
      }, 
      {
        "group": "GrandTotal", 
        "type": "Section", 
        "Summary": {
          "ColData": [
            {
              "value": "Total"
            }, 
            {
              "value": "1200.00"
            }
          ]
        }
      }
    ]
  }, 
  "Columns": {
    "Column": [
      {
        "ColType": "Department", 
        "ColTitle": ""
      }, 
      {
        "ColType": "Money", 
        "ColTitle": "Total"
      }
    ]
  }
}
```

## Report Columns

| Column | Description |
|--------|-------------|
| Department | Department name (or "Not Specified" for unassigned) |
| Total | Total sales amount |
