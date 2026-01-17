# TaxAgency

A TaxAgency object is associated with a tax rate and identifies the agency to which that tax rate applies, that is, the entity that collects those taxes. QuickBooks companies based in the US will only display system-created tax agencies. They also only display the associated tax rates available and visible via the QuickBooks UI.

## The TaxAgency Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Required for update, read only, system defined | Unique identifier for this object. Sort order is ASC by default. |
| **DisplayName** | String, sortable | Required | Name of the agency. Maximum of 100 chars. |
| **SyncToken** | String | Required for update, read only, system defined | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. |
| **TaxTrackedOnSales** | Boolean | Optional, read only | Denotes whether this tax agency is used to track tax on sales. |
| **TaxTrackedOnPurchases** | Boolean | Optional, read only | Denotes whether this tax agency is used to track tax on purchases. |
| **LastFileDate** | Date (minorVersion: 6) | Optional, read only | The last tax filing date for this tax agency. This field is automatically populated by QuickBooks business logic at tax filing time. |
| **TaxRegistrationNumber** | String | Optional, read only | Registration number for the agency. |
| **MetaData** | ModificationMetaData | Optional | Descriptive information about the entity. The MetaData values are set by Data Services and are read only for all applications. |
| **TaxAgencyConfig** | String (minorVersion: 46) | read only | Flag to identify whether the TaxAgency is system defined by Automated Sales Tax engine or user generated. Valid values include USER_DEFINED, SYSTEM_GENERATED. |

### Sample Object

```json
{
  "time": "2015-07-27T14:30:33.478-07:00",
  "TaxAgency": {
    "SyncToken": "0",
    "domain": "QBO",
    "DisplayName": "Arizona Dept. of Revenue",
    "TaxTrackedOnSales": true,
    "TaxTrackedOnPurchases": false,
    "sparse": false,
    "Id": "1",
    "MetaData": {
      "CreateTime": "2014-09-18T12:17:04-07:00",
      "LastUpdatedTime": "2014-09-18T12:17:04-07:00"
    }
  }
}
```

## Create a TaxAgency

A TaxAgency object must have a DisplayName attribute.

### Request Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **DisplayName** | String, sortable | Required | Name of the agency. Maximum of 100 chars. |

### Returns

Returns the newly created taxagency object.

### Request URL

```
POST /v3/company/<realmID>/taxagency
Content type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "DisplayName": "CityTaxAgency"
}
```

### Response

```json
{
  "time": "2015-07-27T14:32:27.116-07:00",
  "TaxAgency": {
    "SyncToken": "0",
    "domain": "QBO",
    "DisplayName": "CityTaxAgency",
    "TaxTrackedOnSales": true,
    "TaxTrackedOnPurchases": false,
    "sparse": false,
    "Id": "3",
    "MetaData": {
      "CreateTime": "2015-07-27T14:32:27-07:00",
      "LastUpdatedTime": "2015-07-27T14:32:27-07:00"
    }
  }
}
```

## Query a TaxAgency

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
select * from TaxAgency
```

### Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "totalCount": 2,
    "maxResults": 2,
    "TaxAgency": [
      {
        "SyncToken": "0",
        "domain": "QBO",
        "DisplayName": "Arizona Dept. of Revenue",
        "TaxTrackedOnSales": true,
        "TaxTrackedOnPurchases": false,
        "sparse": false,
        "Id": "1",
        "MetaData": {
          "CreateTime": "2014-09-18T12:17:04-07:00",
          "LastUpdatedTime": "2014-09-18T12:17:04-07:00"
        }
      },
      {
        "SyncToken": "0",
        "domain": "QBO",
        "DisplayName": "Board of Equalization",
        "TaxTrackedOnSales": true,
        "TaxTrackedOnPurchases": false,
        "sparse": false,
        "Id": "2",
        "MetaData": {
          "CreateTime": "2014-09-18T12:17:04-07:00",
          "LastUpdatedTime": "2014-09-18T12:17:04-07:00"
        }
      }
    ]
  },
  "time": "2015-07-27T14:26:19.454-07:00"
}
```

## Read a TaxAgency

Retrieves the details of a TaxAgency object that has been previously created.

### Returns

Returns the TaxAgency object.

### Request URL

```
GET /v3/company/<realmID>/taxagency/<taxagencyId>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "time": "2015-07-27T14:30:33.478-07:00",
  "TaxAgency": {
    "SyncToken": "0",
    "domain": "QBO",
    "DisplayName": "Arizona Dept. of Revenue",
    "TaxTrackedOnSales": true,
    "TaxTrackedOnPurchases": false,
    "sparse": false,
    "Id": "1",
    "MetaData": {
      "CreateTime": "2014-09-18T12:17:04-07:00",
      "LastUpdatedTime": "2014-09-18T12:17:04-07:00"
    }
  }
}
```
