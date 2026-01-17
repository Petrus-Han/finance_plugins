# TaxRate

A TaxRate object represents rate applied to calculate tax liability. Use the TaxService entity to create a taxrate.

## Create a TaxRate

Use the **TaxService** resource to create a tax rate.

## The TaxRate Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Optional, read only, system defined | Unique identifier for this object. Sort order is ASC by default. |
| **SyncToken** | String | Required for update, read only, system defined | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. |
| **RateValue** | String | Optional, read only | Value of the tax rate. |
| **Name** | String, filterable, sortable | Optional, read only | User recognizable name for the tax rate. Maximum of 100 chars. |
| **AgencyRef** | ReferenceType, filterable, sortable | Optional, read only | Reference to the tax agency associated with this object. |
| **SpecialTaxType** | String | Optional, read only | Special tax type to handle zero rate taxes. Used with VAT registered Businesses who receive goods/services (acquisitions) from other EU countries, will need to calculate the VAT due, but not paid, on these acquisitions. |
| **EffectiveTaxRate** | EffectiveTaxRateData | Optional, read only | List of EffectiveTaxRate. An EffectiveTaxRate is used to know which taxrate is applicable on any date. |
| **DisplayType** | String | Optional, read only | TaxRate DisplayType enum which acts as display config. |
| **TaxReturnLineRef** | ReferenceType, filterable, sortable | Optional, read only | Reference to the tax return line associated with this object. |
| **Active** | Boolean, filterable, sortable | Optional, read only | If true, this object is currently enabled for use by QuickBooks. |
| **MetaData** | ModificationMetaData | Optional | Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications. |
| **OriginalTaxRate** | String (minorVersion: 62) | Optional, read only | ID of the original tax rate from which the new tax rate is derived. Helps to understand the relationship between corresponding tax rate entities. |
| **Description** | String, filterable, sortable | Optional, read only | User entered description for the tax rate. Maximum of 100 chars. |

### Sample Object

```json
{
  "TaxRate": {
    "RateValue": 2,
    "AgencyRef": {
      "value": "1"
    },
    "domain": "QBO",
    "Name": "Tucson City",
    "SyncToken": "0",
    "SpecialTaxType": "NONE",
    "DisplayType": "ReadOnly",
    "sparse": false,
    "Active": true,
    "MetaData": {
      "CreateTime": "2014-09-18T12:17:04-07:00",
      "LastUpdatedTime": "2014-09-18T12:17:04-07:00"
    },
    "Id": "2",
    "Description": "Sales Tax"
  },
  "time": "2015-07-27T13:29:41.836-07:00"
}
```

## Query a TaxRate

### Returns

Returns the results of the query.

### Request URL

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content type: text/plain
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Sample Query

```sql
Select * From TaxRate
```

### Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "totalCount": 3,
    "TaxRate": [
      {
        "RateValue": 7.1,
        "AgencyRef": {
          "value": "1"
        },
        "domain": "QBO",
        "Name": "AZ State tax",
        "SyncToken": "0",
        "SpecialTaxType": "NONE",
        "DisplayType": "ReadOnly",
        "sparse": false,
        "Active": true,
        "MetaData": {
          "CreateTime": "2014-09-18T12:17:04-07:00",
          "LastUpdatedTime": "2014-09-18T12:17:04-07:00"
        },
        "Id": "1",
        "Description": "Sales Tax"
      },
      {
        "RateValue": 8,
        "AgencyRef": {
          "value": "2"
        },
        "domain": "QBO",
        "Name": "California",
        "SyncToken": "0",
        "SpecialTaxType": "NONE",
        "DisplayType": "ReadOnly",
        "sparse": false,
        "Active": true,
        "MetaData": {
          "CreateTime": "2014-09-18T12:17:04-07:00",
          "LastUpdatedTime": "2014-09-18T12:17:04-07:00"
        },
        "Id": "3",
        "Description": "Sales Tax"
      },
      {
        "RateValue": 2,
        "AgencyRef": {
          "value": "1"
        },
        "domain": "QBO",
        "Name": "Tucson City",
        "SyncToken": "0",
        "SpecialTaxType": "NONE",
        "DisplayType": "ReadOnly",
        "sparse": false,
        "Active": true,
        "MetaData": {
          "CreateTime": "2014-09-18T12:17:04-07:00",
          "LastUpdatedTime": "2014-09-18T12:17:04-07:00"
        },
        "Id": "2",
        "Description": "Sales Tax"
      }
    ],
    "maxResults": 3
  },
  "time": "2015-07-27T13:32:06.76-07:00"
}
```

## Read a TaxRate

Retrieves the details of a TaxRate object.

### Returns

Returns the TaxRate object.

### Request URL

```
GET /v3/company/<realmID>/taxrate/<taxrateId>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "TaxRate": {
    "RateValue": 2,
    "AgencyRef": {
      "value": "1"
    },
    "domain": "QBO",
    "Name": "Tucson City",
    "SyncToken": "0",
    "SpecialTaxType": "NONE",
    "DisplayType": "ReadOnly",
    "sparse": false,
    "Active": true,
    "MetaData": {
      "CreateTime": "2014-09-18T12:17:04-07:00",
      "LastUpdatedTime": "2014-09-18T12:17:04-07:00"
    },
    "Id": "2",
    "Description": "Sales Tax"
  },
  "time": "2015-07-27T13:29:41.836-07:00"
}
```
