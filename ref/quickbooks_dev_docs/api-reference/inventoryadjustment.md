# InventoryAdjustment

InventoryAdjustment provides a way for customers to change the quantity of inventory items for various reasons, such as damage, stock write-off, shrinkage, or expiration. The change in quantity automatically handles the underlying accounting and valuation. Customers can view and verify the inventory quantity and valuation using the Inventory Valuation Report in QuickBooks Online.

This functionality is available for QuickBooks Online Plus and advanced SKUs in the US. To access this entity, invoke the endpoints with a minorversion=70 or higher query parameter.

## The InventoryAdjustment Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **TxnDate** | DateTime | Required | The date entered by the user when this transaction occurred. yyyy/MM/dd is the valid date format. For posting transactions, this is the posting date that affects the financial statements. If the date is not supplied, the current date on the server is used. Sort order is ASC by default. |
| **Line** | Line [0..n] | Required | Individual line items of an inventory adjustment. |
| **AdjustAccountRef** | ReferenceType | Required | Specifies which account is debited. Query the Account name list resource to determine the appropriate Account object for this reference. Use Account.Id and Account.Name from that object for AdjustAccountRef.value and AdjustAccountRef.name, respectively. Read only, system defined. |
| **SyncToken** | String | Required for update | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. Read only, system defined. |
| **Id** | String, filterable, sortable | Required for update | Unique identifier for this object. Read only, system defined. |
| **DocNumber** | String | Optional | Reference number for the transaction. Max 21 chars. If not explicitly provided at creation time, this field is auto populated by incrementing the last number by 1. |
| **PrivateNote** | String | Optional | User entered, organization-private note about the transaction. This note does not appear on the invoice to the customer. This field maps to the Statement Memo field on the Invoice form in the QuickBooks Online UI. Max 4000 chars. |
| **MetaData** | ModificationMetaData | Optional | Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications. |

### Line Item Details (ItemAdjustmentLineDetail)

| Attribute | Type | Description |
|-----------|------|-------------|
| **QtyDiff** | Decimal | The quantity difference (positive for increase, negative for decrease) |
| **ItemRef** | ReferenceType | Reference to the inventory item being adjusted |
| **Id** | String | Line item identifier |

### Sample Object

```json
{
  "InventoryAdjustment": {
    "DocNumber": "27",
    "TxnDate": "2024-05-02",
    "PrivateNote": "",
    "SyncToken": "0",
    "domain": "QBO",
    "AdjustAccountRef": {
      "name": "Inventory Shrinkage",
      "value": "91"
    },
    "sparse": false,
    "Line": [
      {
        "ItemAdjustmentLineDetail": {
          "QtyDiff": -2,
          "ItemRef": {
            "value": "1010000001"
          }
        },
        "Id": "1"
      }
    ],
    "Id": "1455000081",
    "MetaData": {
      "LastUpdatedTime": "2024-05-07"
    }
  },
  "time": "2024-05-07T15:49:02.469-07:00"
}
```

## Create an Inventory Adjustment

Creates a new inventory adjustment.

### Minimum Required Elements

| Attribute | Type | Description |
|-----------|------|-------------|
| **AdjustAccountRef** | ReferenceType | Specifies which account is debited. |
| **Line** | Line [0..n] | Individual line items of an inventory adjustment. |
| **TxnDate** | DateTime | The date the transaction occurred. |

### Optional Elements

| Attribute | Type | Description |
|-----------|------|-------------|
| **DocNumber** | String | Reference number for the transaction. |
| **PrivateNote** | String | User entered, organization-private note about the transaction. |

### Request

```
POST /v3/company/<realmID>/inventoryadjustment
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "AdjustAccountRef": {
    "value": "91"
  },
  "PrivateNote": "Memo 1",
  "Line": [
    {
      "DetailType": "ItemAdjustmentLineDetail",
      "ItemAdjustmentLineDetail": {
        "QtyDiff": -2,
        "ItemRef": {
          "value": "1010000001"
        }
      }
    }
  ],
  "TxnDate": "2024-05-02"
}
```

### Response

```json
{
  "InventoryAdjustment": {
    "DocNumber": "27",
    "TxnDate": "2024-05-02",
    "PrivateNote": "",
    "SyncToken": "0",
    "domain": "QBO",
    "AdjustAccountRef": {
      "name": "Inventory Shrinkage",
      "value": "91"
    },
    "sparse": false,
    "Line": [
      {
        "ItemAdjustmentLineDetail": {
          "QtyDiff": -2,
          "ItemRef": {
            "value": "1010000001"
          }
        },
        "Id": "1"
      }
    ],
    "Id": "1455000081",
    "MetaData": {
      "LastUpdatedTime": "2024-05-07"
    }
  },
  "time": "2024-05-07T15:49:02.469-07:00"
}
```

## Delete an Inventory Adjustment

Deletes the inventory adjustment object specified in the request body. Include a minimum of InventoryAdjustment.Id and InventoryAdjustment.SyncToken in the request body.

### Request

```
POST /v3/company/<realmID>/inventoryadjustment?operation=delete
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "SyncToken": "0",
  "Id": "1455000086"
}
```

### Response

```json
{
  "InventoryAdjustment": {
    "status": "Deleted",
    "domain": "QBO",
    "Id": "1455000086"
  },
  "time": "2024-05-08T14:04:46.441-07:00"
}
```

## Read an Inventory Adjustment

Retrieves the details of an inventoryadjustment object that has been previously created.

### Request

```
GET /v3/company/<realmID>/inventoryadjustment/<inventoryadjustmentId>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "InventoryAdjustment": {
    "DocNumber": "3",
    "TxnDate": "2024-05-02",
    "PrivateNote": "",
    "SyncToken": "0",
    "domain": "QBO",
    "AdjustAccountRef": {
      "name": "Inventory Shrinkage",
      "value": "91"
    },
    "sparse": false,
    "Line": [
      {
        "ItemAdjustmentLineDetail": {
          "QtyDiff": -5,
          "ItemRef": {
            "value": "1010000001"
          }
        },
        "Id": "1"
      }
    ],
    "Id": "1455000036",
    "MetaData": {
      "LastUpdatedTime": "2024-05-03"
    }
  },
  "time": "2024-05-08T13:59:23.274-07:00"
}
```

## Update an Inventory Adjustment

This operation updates the inventoryadjustment object specified in the request body. Include a minimum of InventoryAdjustment.Id and InventoryAdjustment.SyncToken in the request body.

**Note:** The sparse attribute must be set to true.

### Request

```
POST /v3/company/<realmID>/inventoryadjustment
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "SyncToken": "0",
  "PrivateNote": "Update 1",
  "TxnDate": "2024-06-17",
  "AdjustAccountRef": {
    "value": "91"
  },
  "sparse": true,
  "Line": [
    {
      "ItemAdjustmentLineDetail": {
        "QtyDiff": -3,
        "ItemRef": {
          "value": "1010000001"
        }
      },
      "Id": "1"
    }
  ],
  "Id": "1455000036"
}
```

### Response

```json
{
  "InventoryAdjustment": {
    "DocNumber": "3",
    "TxnDate": "2024-06-17",
    "PrivateNote": "Update 1",
    "SyncToken": "1",
    "domain": "QBO",
    "AdjustAccountRef": {
      "name": "Inventory Shrinkage",
      "value": "91"
    },
    "sparse": false,
    "Line": [
      {
        "ItemAdjustmentLineDetail": {
          "QtyDiff": -3,
          "ItemRef": {
            "value": "1010000001"
          }
        },
        "Id": "1"
      }
    ],
    "Id": "1455000036",
    "MetaData": {
      "LastUpdatedTime": "2024-06-17"
    }
  },
  "time": "2024-06-17T14:25:11.880-07:00"
}
```
