# FECReport

The information below provides a reference on how to access the Fichier des Ecritures Comptables (FEC) report from the QuickBooks Online Report Service. This report is available for FR locale only.

## The FEC Report Object

### Attributes

| Name | Description |
| --- | --- |
| Header | The report header. |
| Rows | Top level container holding information for report rows. |
| Columns | Top level container holding information for report columns or subcolumns. |

### Sample Object (JSON)

```json
{
  "Header": {
    "ReportName": "FECReport", 
    "Option": [
      {
        "Name": "NoReportData", 
        "Value": "false"
      }
    ], 
    "ReportBasis": "Accrual", 
    "StartPeriod": "2021-07-01", 
    "Currency": "EUR", 
    "EndPeriod": "2021-07-28", 
    "Time": "2021-07-28T04:37:20-07:00"
  }, 
  "Rows": {
    "Row": [
      {
        "ColData": [
          {
            "value": "VT"
          }, 
          {
            "value": "Sales"
          }, 
          ...
          {
            "value": "Customer"
          }
        ], 
        "type": "Data"
      },
      ...
    ]
  }, 
  "Columns": {
    "Column": [
      {
        "ColType": "String", 
        "ColTitle": "JournalCode", 
        "MetaData": [
          {
            "Name": "ColKey", 
            "Value": "journal_code_name"
          }
        ]
      },
      ...
    ]
  }
}
```

## Query a Report

### Request URL
`GET /v3/company/<realmID>/reports/FECReport?<name>=<value>[&...]`

### Query Parameters

| Name | Type | Description |
| --- | --- | --- |
| attachmentType | String | The parameter attachment type is a string value, and can accept one of the values : TEMPORARY_LINKS or NONE only. (Optional) |
| withQboIdentifier | Boolean | The parameter withQboIdentifier is a boolean value. This parameter can be used to add the columns transaction id and sequence in the response of the query. (Optional) |
| start_date | String | The start date of the report, in the format YYYY-MM-DD. (Optional) |
| end_date | String | The end date of the report, in the format YYYY-MM-DD. (Optional) |
| add_due_date | Boolean | The parameter add_due_date is a boolean value. (Optional) |

### Sample Query
`BaseURL/v3/company/1386066315/reports/FECReport?start_date=2019-11-01&end_date=2021-11-06&attachmentType=TEMPORARY_LINKS&add_due_date=true`

### Sample Response (JSON)
(Same as Sample Object above)
