# CompanyCurrency

Applicable only for those companies that enable multicurrency, a CompanyCurrency object defines a currency that is active in the QuickBooks Online company. One or more companycurrency objects are active based on the company's multicurrency business requirements and correspond to the list displayed by the Currency Center in the QuickBooks Online UI.

## Delete a CompanyCurrency

Delete is achieved by setting the Active attribute to false in an entity update request; thus, making it inactive. In this type of delete, the record is not permanently deleted, but is hidden for display purposes. References to inactive objects are left intact.

## The CompanyCurrency Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Required for update, read only, system defined | Unique identifier for this object. Sort order is ASC by default. |
| **Code** | String | Required | A three letter string representing the ISO 4217 code for the currency. For example, USD, AUD, EUR, and so on. Maximum of 100 chars. |
| **SyncToken** | String | Required for update, read only, system defined | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. |
| **Name** | String | Optional, system defined | The full name of the currency. |
| **CustomField** | CustomField | Optional | One of, up to three custom fields for the transaction. Available for custom fields so configured for the company. Check Preferences.SalesFormsPrefs.CustomField and Preferences.VendorAndPurchasesPrefs.POCustomField for custom fields currently configured. |
| **Active** | Boolean, filterable, sortable | Optional | Indicates whether this currency is active in the company or not. true--This currency is active and enabled for use by QuickBooks. false--This currency is inactive, is hidden from most display purposes, and is not available for use with financial transactions. |
| **MetaData** | ModificationMetaData, filterable, sortable | Optional | Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications. |

### Sample Object

```json
{
  "CompanyCurrency": {
    "SyncToken": "0",
    "domain": "QBO",
    "Code": "EUR",
    "Name": "Euro",
    "sparse": false,
    "Active": true,
    "Id": "2",
    "MetaData": {
      "CreateTime": "2015-06-05T13:59:42-07:00",
      "LastUpdatedTime": "2015-06-05T13:59:42-07:00"
    }
  },
  "time": "2015-07-06T13:30:04.123-07:00"
}
```

## Create a CompanyCurrency

### Request Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Code** | String | Required | A three letter string representing the ISO 4217 code for the currency. For example, USD, AUD, EUR, and so on. Maximum of 100 chars. |

### Returns

Returns the newly created companycurrency object.

### Request URL

```
POST /v3/company/<realmID>/companycurrency
Content type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "Code": "GBP"
}
```

### Response

```json
{
  "CompanyCurrency": {
    "SyncToken": "0",
    "domain": "QBO",
    "Code": "GBP",
    "Name": "British Pound Sterling",
    "sparse": false,
    "Active": true,
    "Id": "7",
    "MetaData": {
      "CreateTime": "2015-07-06T13:34:48-07:00",
      "LastUpdatedTime": "2015-07-06T13:34:48-07:00"
    }
  },
  "time": "2015-07-06T13:34:48.569-07:00"
}
```

## Query a CompanyCurrency

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
select * from companycurrency
```

### Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "totalCount": 5,
    "CompanyCurrency": [
      {
        "SyncToken": "0",
        "domain": "QBO",
        "Code": "JPY",
        "Name": "Japanese Yen",
        "sparse": false,
        "Active": true,
        "Id": "5",
        "MetaData": {
          "CreateTime": "2015-06-19T09:20:44-07:00",
          "LastUpdatedTime": "2015-06-19T09:20:44-07:00"
        }
      },
      {
        "SyncToken": "0",
        "domain": "QBO",
        "Code": "ANG",
        "Name": "Dutch Guilder",
        "sparse": false,
        "Active": true,
        "Id": "4",
        "MetaData": {
          "CreateTime": "2015-06-12T14:16:38-07:00",
          "LastUpdatedTime": "2015-06-12T14:16:38-07:00"
        }
      },
      {
        "SyncToken": "0",
        "domain": "QBO",
        "Code": "AUD",
        "Name": "Australian Dollar",
        "sparse": false,
        "Active": true,
        "Id": "3",
        "MetaData": {
          "CreateTime": "2015-06-05T13:59:43-07:00",
          "LastUpdatedTime": "2015-06-05T13:59:43-07:00"
        }
      },
      {
        "SyncToken": "0",
        "domain": "QBO",
        "Code": "EUR",
        "Name": "Euro",
        "sparse": false,
        "Active": true,
        "Id": "2",
        "MetaData": {
          "CreateTime": "2015-06-05T13:59:42-07:00",
          "LastUpdatedTime": "2015-06-05T13:59:42-07:00"
        }
      },
      {
        "SyncToken": "0",
        "domain": "QBO",
        "Code": "CAD",
        "Name": "Canadian Dollar",
        "sparse": false,
        "Active": true,
        "Id": "1",
        "MetaData": {
          "CreateTime": "2015-06-05T13:59:42-07:00",
          "LastUpdatedTime": "2015-06-05T13:59:42-07:00"
        }
      }
    ],
    "maxResults": 5
  },
  "time": "2015-07-06T13:29:01.560-07:00"
}
```

## Read a CompanyCurrency

Retrieves the details of a CompanyCurrency object that has been previously created.

### Returns

Returns the companycurrency object.

### Request URL

```
GET /v3/company/<realmID>/companycurrency/<companycurrencyId>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "CompanyCurrency": {
    "SyncToken": "0",
    "domain": "QBO",
    "Code": "EUR",
    "Name": "Euro",
    "sparse": false,
    "Active": true,
    "Id": "2",
    "MetaData": {
      "CreateTime": "2015-06-05T13:59:42-07:00",
      "LastUpdatedTime": "2015-06-05T13:59:42-07:00"
    }
  },
  "time": "2015-07-06T13:30:04.123-07:00"
}
```

## Update a CompanyCurrency

Use this operation to update any of the writable fields of an existing CompanyCurrency object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL. The ID of the object to update is specified in the request body.

### Request Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Required for update, read only, system defined | Unique identifier for this object. Sort order is ASC by default. |
| **Code** | String | Required | A three letter string representing the ISO 4217 code for the currency. For example, USD, AUD, EUR, and so on. Maximum of 100 chars. |
| **SyncToken** | String | Required for update, read only, system defined | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. |
| **Name** | String | Optional, system defined | The full name of the currency. |
| **CustomField** | CustomField | Optional | One of, up to three custom fields for the transaction. |
| **Active** | Boolean, filterable, sortable | Optional | Indicates whether this currency is active in the company or not. |
| **MetaData** | ModificationMetaData, filterable, sortable | Optional | Descriptive information about the object. |

### Returns

The companycurrency response body.

### Request URL

```
POST /v3/company/<realmID>/companycurrency
Content type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "SyncToken": "0",
  "domain": "QBO",
  "Code": "GBP",
  "Name": "British Pound Sterling",
  "sparse": false,
  "Active": false,
  "Id": "7",
  "MetaData": {
    "CreateTime": "2015-07-06T13:34:48-07:00",
    "LastUpdatedTime": "2015-07-06T13:34:48-07:00"
  }
}
```

### Response

```json
{
  "CompanyCurrency": {
    "SyncToken": "1",
    "domain": "QBO",
    "Code": "GBP",
    "Name": "British Pound Sterling",
    "sparse": false,
    "Active": false,
    "Id": "7",
    "MetaData": {
      "CreateTime": "2015-07-06T13:34:48-07:00",
      "LastUpdatedTime": "2015-07-06T14:03:40-07:00"
    }
  },
  "time": "2015-07-06T14:03:39.891-07:00"
}
```
