# TaxCode

A TaxCode object is used to track the taxable or non-taxable status of products, services, and customers. You can assign a sales tax code to each of your products, services, and customers based on their taxable or non-taxable status. You can then use these codes to generate reports that provide information to the tax agencies about the taxable or non-taxable status of certain sales.

## Create a TaxCode

Use the **TaxService** resource to create a tax code.

## The TaxCode Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Required for update, read only, system defined | Unique identifier for this object. Sort order is ASC by default. |
| **Name** | String, filterable, sortable | Required | User recognizable name for the tax sales code. Maximum of 100 chars. |
| **SyncToken** | String | Required for update, read only, system defined | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. |
| **PurchaseTaxRateList** | TaxRateList | Conditionally required | List of references to tax rates that apply for purchase transactions when this tax code represents a group of tax rates. Required when TaxGroup is set to true. |
| **SalesTaxRateList** | TaxRateList | Conditionally required | List of references to tax rates that apply for sales transactions when this tax code represents a group of tax rates. Required when TaxGroup is set to true. |
| **TaxGroup** | Boolean | Optional, read only | true—this object represents a group of one or more tax rates. false—this object represents pseudo-tax codes TAX and NON. |
| **Taxable** | Boolean | Optional, read only | False or null means non-taxable. True means taxable. Always true, except for the pseudo taxcode NON. |
| **Active** | Boolean, filterable | Optional | False if inactive. Inactive sales tax codes may be hidden from display and may not be used on financial transactions. |
| **Description** | String, filterable, sortable | Optional | User entered description for the sales tax code. Maximum of 100 chars. |
| **Hidden** | Boolean (minorVersion: 21) | Optional, read only | Denotes whether active tax codes are displayed on transactions. true—This tax code is hidden on transactions. false—This tax code is displayed on transactions. |
| **MetaData** | ModificationMetaData | Optional | Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications. |
| **TaxCodeConfigType** | String (minorVersion: 51) | read only | Flag to identify whether the TaxCode is system defined by Automated Sales Tax engine or user generated. Valid values include USER_DEFINED, SYSTEM_GENERATED. |

### TaxRateList Child Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **TaxRateDetail** | Array | Array of tax rate details. |
| **TaxRateDetail.TaxTypeApplicable** | String | Type of tax applicable (e.g., TaxOnAmount). |
| **TaxRateDetail.TaxRateRef** | ReferenceType | Reference to the tax rate. |
| **TaxRateDetail.TaxOrder** | Integer | Order in which tax is applied. |

### Sample Object

```json
{
  "TaxCode": {
    "SyncToken": "0",
    "domain": "QBO",
    "TaxGroup": true,
    "Name": "California",
    "Taxable": true,
    "PurchaseTaxRateList": {
      "TaxRateDetail": []
    },
    "sparse": false,
    "Active": true,
    "Description": "California",
    "MetaData": {
      "CreateTime": "2014-09-18T12:17:04-07:00",
      "LastUpdatedTime": "2014-09-18T12:17:04-07:00"
    },
    "Id": "2",
    "SalesTaxRateList": {
      "TaxRateDetail": [
        {
          "TaxTypeApplicable": "TaxOnAmount",
          "TaxRateRef": {
            "name": "California",
            "value": "3"
          },
          "TaxOrder": 0
        }
      ]
    }
  },
  "time": "2015-07-27T12:37:22.733-07:00"
}
```

## Query a TaxCode

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
select * From TaxCode
```

### Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "totalCount": 5,
    "TaxCode": [
      {
        "TaxGroup": false,
        "Name": "TAX",
        "Taxable": true,
        "Description": "TAX",
        "Id": "TAX",
        "MetaData": {
          "CreateTime": "2014-10-15T11:28:33-07:00",
          "LastUpdatedTime": "2014-10-15T11:28:33-07:00"
        }
      },
      {
        "TaxGroup": false,
        "Name": "NON",
        "Taxable": false,
        "Description": "NON",
        "Id": "NON",
        "MetaData": {
          "CreateTime": "2014-10-15T11:28:33-07:00",
          "LastUpdatedTime": "2014-10-15T11:28:33-07:00"
        }
      },
      {
        "SyncToken": "0",
        "domain": "QBO",
        "TaxGroup": true,
        "Name": "California",
        "Taxable": true,
        "PurchaseTaxRateList": {
          "TaxRateDetail": []
        },
        "sparse": false,
        "Active": true,
        "Description": "California",
        "MetaData": {
          "CreateTime": "2014-09-18T12:17:04-07:00",
          "LastUpdatedTime": "2014-09-18T12:17:04-07:00"
        },
        "Id": "2",
        "SalesTaxRateList": {
          "TaxRateDetail": [
            {
              "TaxTypeApplicable": "TaxOnAmount",
              "TaxRateRef": {
                "name": "California",
                "value": "3"
              },
              "TaxOrder": 0
            }
          ]
        }
      },
      {
        "SyncToken": "0",
        "domain": "QBO",
        "TaxGroup": true,
        "Name": "Tucson",
        "Taxable": true,
        "PurchaseTaxRateList": {
          "TaxRateDetail": []
        },
        "sparse": false,
        "Active": true,
        "Description": "Tucson",
        "MetaData": {
          "CreateTime": "2014-09-18T12:17:04-07:00",
          "LastUpdatedTime": "2014-09-18T12:17:04-07:00"
        },
        "Id": "3",
        "SalesTaxRateList": {
          "TaxRateDetail": [
            {
              "TaxTypeApplicable": "TaxOnAmount",
              "TaxRateRef": {
                "name": "AZ State tax",
                "value": "1"
              },
              "TaxOrder": 0
            },
            {
              "TaxTypeApplicable": "TaxOnAmount",
              "TaxRateRef": {
                "name": "Tucson City",
                "value": "2"
              },
              "TaxOrder": 0
            }
          ]
        }
      }
    ],
    "maxResults": 5
  },
  "time": "2015-07-27T11:44:00.125-07:00"
}
```

## Read a TaxCode

Retrieves the details of a TaxCode object that has been previously created.

### Returns

Returns the TaxCode object.

### Request URL

```
GET /v3/company/<realmID>/taxcode/<taxcodeId>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "TaxCode": {
    "SyncToken": "0",
    "domain": "QBO",
    "TaxGroup": true,
    "Name": "California",
    "Taxable": true,
    "PurchaseTaxRateList": {
      "TaxRateDetail": []
    },
    "sparse": false,
    "Active": true,
    "Description": "California",
    "MetaData": {
      "CreateTime": "2014-09-18T12:17:04-07:00",
      "LastUpdatedTime": "2014-09-18T12:17:04-07:00"
    },
    "Id": "2",
    "SalesTaxRateList": {
      "TaxRateDetail": [
        {
          "TaxTypeApplicable": "TaxOnAmount",
          "TaxRateRef": {
            "name": "California",
            "value": "3"
          },
          "TaxOrder": 0
        }
      ]
    }
  },
  "time": "2015-07-27T12:37:22.733-07:00"
}
```
